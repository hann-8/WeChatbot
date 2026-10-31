"""Keep the unchanged upstream UIA sender and all its Controls on one thread."""
from concurrent.futures import ThreadPoolExecutor
import sys


class TargetSelectionFailed(RuntimeError):
    pass


class BoundWindowUnavailable(RuntimeError):
    pass


class WindowBinding:
    """Identity for the operator-selected robot window; never search another account."""
    def __init__(self,sender,binding):
        import uiautomation as auto
        self.sender=sender;self.binding=binding
        self.control=auto.ControlFromHandle(binding['hwnd'])
        if not self.valid():raise BoundWindowUnavailable()
        sender._window=self.control;sender._ready=True
        sender._find_window=self.restore

    def valid(self):
        import psutil
        try:
            return (abs(psutil.Process(self.binding['pid']).create_time()-self.binding['created'])<.02 and
                    self.control and self.control.Exists(0) and self.control.ProcessId==self.binding['pid'])
        except (psutil.Error,OSError):return False

    def restore(self):
        self.sender._window=self.control if self.valid() else None

    def check(self):
        # Upstream activation/search also uses a global FindWindow. Require that
        # lookup to resolve to this exact bound window before it can type.
        import ctypes
        from ctypes import wintypes
        api=ctypes.WinDLL('user32',use_last_error=True)
        api.FindWindowW.argtypes=[wintypes.LPCWSTR,wintypes.LPCWSTR]
        api.FindWindowW.restype=wintypes.HWND
        target=api.FindWindowW('Qt51514QWindowIcon',None) or api.FindWindowW('WeChatMainWndForPC',None)
        if not self.valid() or target!=self.binding['hwnd']:raise BoundWindowUnavailable()


class ErrorMetadata:
    """Capture only error class/code; upstream messages contain names and text."""
    def __init__(self):self.last={}
    def info(self,*args,**kwargs):pass
    def debug(self,*args,**kwargs):pass
    def warning(self,*args,**kwargs):pass
    def error(self,*args,**kwargs):
        error=sys.exc_info()[1]
        self.last={'error_type':type(error).__name__ if error else 'SenderReportedFailure'}
        code=getattr(error,'hresult',None)
        if isinstance(code,int):self.last['hresult']=code


def initialize_uia():
    import uiautomation as auto
    return auto.UIAutomationInitializerInThread()


class ThreadedSender:
    def __init__(self,factory,initialize=initialize_uia,diagnostics=None,binding=None):
        self.executor=ThreadPoolExecutor(max_workers=1,thread_name_prefix='akasha-uia')
        self.log=diagnostics or ErrorMetadata();self.failure={}
        def create():
            self.com=initialize()
            try:
                sender=factory()
                self.window_binding=WindowBinding(sender,binding) if binding else None
                return sender
            except BaseException:
                self.com.Uninitialize()
                raise
        try:self.sender=self.executor.submit(create).result()
        except BaseException:
            self.executor.shutdown(wait=True,cancel_futures=True)
            raise

    @property
    def _ready(self):return self.sender._ready

    def _send(self,method,contact,payload):
        self.failure={};self.log.last={};stage='target_selection'
        try:
            if self.window_binding:self.window_binding.check()
            # The original sender ignores this bool and caches the last contact.
            # Re-select the explicitly bound conversation before each submission.
            if self.sender._switch_contact(contact) is not True:raise TargetSelectionFailed()
            self.sender._last_contact=contact
            stage=method
            result=getattr(self.sender,method)(contact,payload)
            if result is not True:self.failure=dict(stage=stage,**(self.log.last or {'error_type':'SenderReturnedFalse'}))
            return result
        except Exception as error:
            self.failure=dict(stage=stage,error_type=type(error).__name__)
            code=getattr(error,'hresult',None)
            if isinstance(code,int):self.failure['hresult']=code
            raise

    def send_text(self,contact,text):
        return self.executor.submit(self._send,'send_text',contact,text).result()

    def send_image(self,contact,path):
        return self.executor.submit(self._send,'send_image',contact,path).result()

    def close(self):
        def release():
            self.window_binding=None
            self.sender=None
            self.com.Uninitialize()
        try:self.executor.submit(release).result()
        finally:self.executor.shutdown(wait=True,cancel_futures=True)


def capture_binding(account):
    import psutil,uia_sender
    uia_sender.log=ErrorMetadata()
    sender=ThreadedSender(uia_sender.UiaSender)
    try:
        def capture():
            auto=sender.sender._auto
            windows=[w for w in auto.GetRootControl().GetChildren()
                     if w.ClassName in ('Qt51514QWindowIcon','WeChatMainWndForPC') and
                     any(n in w.Name for n in sender.sender.WECHAT_TITLES)]
            if len(windows)!=1:raise ValueError('Bind requires only the robot WeChat window to be open')
            window=windows[0];process=psutil.Process(window.ProcessId)
            return dict(account=account,hwnd=window.NativeWindowHandle,pid=process.pid,created=process.create_time())
        return sender.executor.submit(capture).result()
    finally:sender.close()


def install_sender(cfg):
    import senders,uia_sender
    original=senders.create_sender
    def create():
        binding=cfg.get('uia_window')
        if not binding or binding.get('account')!=cfg['bridge']['bot_wxid']:
            raise ValueError('UIA robot window binding required; run bind-window')
        diagnostics=ErrorMetadata()
        uia_sender.log=diagnostics
        return ThreadedSender(original,diagnostics=diagnostics,binding=binding)
    senders.create_sender=create
