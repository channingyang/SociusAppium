# -*- coding: utf-8 -*-
#coding=utf-8
import os
import re
import sys
import pytest
import logging
import unittest
import subprocess
import time

from appium import webdriver

import config
from RAT import *

# Returns abs path relative to this file and not cwd
PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)

path1 = "./test_resources/."

# logger
logger = logging.getLogger()
logFormatter = logging.Formatter(
    '[%(asctime)-15s][%(filename)s][%(funcName)s#%(lineno)d] %(message)s')
ch = logging.StreamHandler(sys.stdout)
ch.setFormatter(logFormatter)
logger.addHandler(ch)
logger.setLevel(logging.INFO)


class otherposts(BaseTests):
    def test_other_videopost(self):
        try:
            self.sociushelper.click_login_by_email_link()
            self.sociushelper.login_account(config.EMAIL_ACCOUNT, config.EMAIL_PWD)

            self.sociushelper.click_require_permission_button()

            self.sociushelper.click_onboading_step()
            # click friend
           # self.sociushelper.swipe_navi_menu()
           # self.sociushelper.swipe_to_find_friend()
           # self.sociushelper.swipe_to_friendlist()

            # click searchid
            self.sociushelper.swipe_to_SearchId()
            # click search id user
            self.sociushelper.click_searchid("point4")
            # click videocard
            self.sociushelper.swipe_tofind()

            check_a = self.sociushelper.check_like_num(["like", u"個棒"]) # (a) to get like of number
            self.sociushelper.swipe_like()#click like
            check_b = self.sociushelper.check_like_num(["like", u"個棒"]) # (b) to get like of number
            self.assertTrue(check_b > check_a,u"expect value {}, but return unexpected {}".format(check_b, check_a)) #After click like_bt , compare (a) with (b) count whether +1
            self.sociushelper.swipe_like()#keep like

            # into msg & key in msg
            self.sociushelper.swipe_and_send_message("this is msg testing")#input message to share_EditText ,and click send button
            self.sociushelper.is_message("this is msg testing")
            self.syshelper.press_back_key()

            # share
            share_a = self.sociushelper.check_like_num(["shares", u"個分享"])
            self.sociushelper.swpie_share_posts()#click share posts button
            self.sociushelper.swipe_share_posts_to_soocii()
            self.sociushelper.input_send_share_message("share posts testing")#input message and click send button
            self.sociushelper.swipe_tofind()
            #self.sociushelper.swipe_posts()
            share_b = self.sociushelper.check_like_num(["shares", u"個分享"])
            self.assertTrue(share_b != share_a,u"expect value {}, but return unexpected {}".format(share_b, share_a))
            self.syshelper.wait_transition(5)
        except:
            self.logger.info('caught exception: {}'.format(sys.exc_info()[0]))
            self.syshelper.capture_screen("test_other_videopost")
            raise
