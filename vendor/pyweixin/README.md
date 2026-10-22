# WX-02 固定来源与可选原语锁

返回[能力报告](../../docs/WX-02-CAPABILITY-REPORT.md)。上游 `Hello-Mr-Crab/pywechat` 固定 `8589baa049bb91d3a500602c167f07b2f8397a13`；声明分发名 `pywechat127==1.9.8`，模块 `pyweixin`。相同版本号的PyPI包不视为该commit的等价工件。本任务没有下载/安装pywechat127 wheel，也没有导入任何上游模块。

`source-lock.json`记录11份审阅源文件的Git blob和SHA-256。`upstream/`只保存原始许可/分发元数据；`excerpts.json`保存带原始行号的决定性片段，不在Python导入路径。上游代码没有修改、没有整包复制；本地适配器为独立封装的只读操作接口，选择器依据固定Uielements，禁止导入上游初始化/AutoReply/Monitor/Tools。

`observation-requirements.lock`是未来原语provider可使用的 **Windows x64 / CPython3.12** 可选锁：pywinauto0.6.9、six1.17.0、comtypes1.4.13、pywin32311，全部固定wheel SHA-256。不是Linux/其他Python通用锁；没有加入默认pyproject/uv.lock，没有安装/加载或执行postinstall。当前inspect/mock/注入式只读原语不需要这些包。四份实际wheel只下载到忽略cache核对hash、METADATA及许可；URLs/hash和Requires-Dist见dependencies.json，许可证原文在licenses/。不安装上游声明的PyAutoGUI/pycaw/音视频/Markdown/bs4等整包依赖。

根LICENSE正文LGPL-2.1，pyproject分类器却声明LGPLv3，setup.py只写LGPL；这是实际许可元数据冲突，保留原文，不以分类器替换根许可，也不宣称已取得额外授权。pywinauto为BSD-3-Clause，six/comtypes为MIT风格正文；pywin32元数据PSF，但wheel含多份组件许可，均保留，不将整个wheel简化为单一许可结论。未来分发实际代码前仍需按具体所用文件审阅。

离线复核：`.venv/Scripts/python.exe scripts/check_pyweixin_source.py`。可额外传 `--source-dir cache/wx02/upstream --wheel-dir cache/wx02/wheels` 核对已下载字节和原始行片段，不联网、不安装、不导入上游。重新取源须使用固定commit的raw URL并先核对manifest；更新必须显式重新审阅/改锁/验证，不跟随latest。
