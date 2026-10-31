"""Existing sender factory/target/send/COM cleanup share one owner thread."""
from pathlib import Path
import sys
import threading
import unittest
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'adapters/akasha'))
from uia_dispatch import ThreadedSender,TargetSelectionFailed


class DispatchTests(unittest.TestCase):
    def test_thread_ownership_and_fresh_target_for_each_send(self):
        calls=[]
        class COM:
            def __init__(self):calls.append(('COM',threading.get_ident()))
            def Uninitialize(self):calls.append(('close',threading.get_ident()))
        class Sender:
            _ready=True
            def __init__(self):calls.append(('factory',threading.get_ident()))
            def _switch_contact(self,name):calls.append(('target',threading.get_ident()));return True
            def send_text(self,*args):calls.append(('text',threading.get_ident()));return True
            def send_image(self,*args):calls.append(('image',threading.get_ident()));return True
        sender=ThreadedSender(Sender,initialize=COM)
        try:
            self.assertTrue(sender.send_text('fixture','synthetic'))
            self.assertTrue(sender.send_image('fixture','synthetic.png'))
        finally:sender.close()
        self.assertEqual([x[0] for x in calls],['COM','factory','target','text','target','image','close'])
        self.assertEqual(len({x[1] for x in calls}),1)
        self.assertNotEqual(calls[0][1],threading.get_ident())

    def test_target_refusal_never_submits_and_error_metadata_contains_no_text(self):
        class COM:
            def Uninitialize(self):pass
        class Sender:
            _ready=True
            def _switch_contact(self,name):return False
            def send_text(self,*args):raise AssertionError('must not submit')
        sender=ThreadedSender(Sender,initialize=COM)
        try:
            with self.assertRaises(TargetSelectionFailed):sender.send_text('private target','private text')
            self.assertEqual(sender.failure,dict(stage='target_selection',error_type='TargetSelectionFailed'))
        finally:sender.close()

    def test_bound_window_loss_stops_before_target_or_text(self):
        class COM:
            def Uninitialize(self):pass
        class Sender:
            _ready=True
            def _switch_contact(self,name):raise AssertionError('must not touch another window')
            def send_text(self,*args):raise AssertionError('must not submit')
        from uia_dispatch import BoundWindowUnavailable
        class Binding:
            def __init__(self,*args):pass
            def check(self):raise BoundWindowUnavailable()
        with patch('uia_dispatch.WindowBinding',Binding):
            sender=ThreadedSender(Sender,initialize=COM,binding={'synthetic':True})
            try:
                with self.assertRaises(BoundWindowUnavailable):sender.send_text('fixture','synthetic')
                self.assertEqual(sender.failure['error_type'],'BoundWindowUnavailable')
            finally:sender.close()

if __name__=='__main__':unittest.main()
