#coding=utf-8
import os
import sys
import logging
import pytest
import unittest

from appium import webdriver

import config
from lib.util import Util
from lib.socius import Socius

# Returns abs path relative to this file and not cwd
PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)

# logger
logger = logging.getLogger()
logFormatter = logging.Formatter(
    '[%(asctime)-15s][%(filename)s][%(funcName)s#%(lineno)d] %(message)s')
ch = logging.StreamHandler(sys.stdout)
ch.setFormatter(logFormatter)
logger.addHandler(ch)
logger.setLevel(logging.INFO)

class SociusTests(unittest.TestCase):
    def setUp(self):
        desired_caps = {}
        desired_caps['platformName'] = 'Android'
        desired_caps['platformVersion'] = '5.0'
        desired_caps['deviceName'] = 'Android Emulator'
        #desired_caps['full-reset'] = True
        desired_caps['app'] = PATH(
            'soocii_v0.0.1035_google_2017_0301_1102_staging.apk'
        )

        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
        self.driver.implicitly_wait(config.WAIT_TIME)
        self.window_size = self.driver.get_window_size()

        self.util = Util(self.driver, self.window_size)
        self.socius = Socius(self.driver, self.window_size)

    def tearDown(self):
        # remove app
        self.driver.close_app()

        # end the session
        self.driver.quit()

    @pytest.mark.first
    def test_fresh_install_and_enable_usage_access(self):
        try:
            # Facebook Login button on Soocii
            self.socius.click_facebook_login_button()

            self.util.login_facebook_account("doctorfamily.mobi@gmail.com", "soocii@2016")
            self.util.allow_system_permissions()
            # only need to enable usage access once
            self.util.enable_usage_access()
            self.socius.skip_guide_mark()
            # expect seeing newsfeed page
            self.assertTrue(self.socius.is_newsfeed())
            displayName, soociiId = self.socius.get_personal_info()
            self.assertTrue(u"錢多多"==displayName, u"expect value {}, but return unexpected {}".format(u"錢多多", displayName))
            self.assertTrue("doctorfamily.mobi"==soociiId, u"expect value {}, but return unexpected {}".format("soociidauto1", soociiId))
            # switch to home and back to soocii
            self.util.press_home_key()
            self.util.start_soocii()
            displayName, soociiId = self.socius.get_personal_info()
            self.assertTrue(u"錢多多"==displayName, u"expect value {}, but return unexpected {}".format(u"錢多多", displayName))
            self.assertTrue("doctorfamily.mobi"==soociiId, u"expect value {}, but return unexpected {}".format("soociidauto1", soociiId))
            # don't delete the account
        except:
            self.util.capture_screen("test_fresh_install_and_enable_usage_access")
            raise

    def test_login_new_facebook_account(self):
        try:
            # Facebook Login button on Soocii
            self.socius.click_facebook_login_button()

            self.util.login_facebook_account("soocii.auto1@gmail.com", "drmobile@123456")
            self.socius.create_account("display", "soociidauto1")
            self.socius.add_followers()
            self.util.allow_system_permissions()
            self.socius.skip_guide_mark()
            # expect seeing newsfeed page
            self.assertTrue(self.socius.is_newsfeed())
            displayName, soociiId = self.socius.get_personal_info()
            self.assertTrue("display"==displayName, u"expect value {}, but return unexpected {}".format("display", displayName))
            self.assertTrue("soociidauto1"==soociiId, u"expect value {}, but return unexpected {}".format("soociidauto1", soociiId))
            # switch to home and back to soocii
            self.util.press_home_key()
            self.util.start_soocii()
            displayName, soociiId = self.socius.get_personal_info()
            self.assertTrue("display"==displayName, u"expect value {}, but return unexpected {}".format("display", displayName))
            self.assertTrue("soociidauto1"==soociiId, u"expect value {}, but return unexpected {}".format("soociidauto1", soociiId))
        except:
            self.util.capture_screen("test_login_new_facebook_account")
            raise
        finally:
            # delete the account for next time
            self.socius.click_delete_account_button()

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(SociusTests)
    unittest.TextTestRunner(verbosity=2).run(suite)

