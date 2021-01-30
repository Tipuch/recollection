from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
from selenium.webdriver.firefox.webdriver import WebDriver

from apps.users.models import CustomUser

# This is used to debug tests
import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s -%(filename)s:%(lineno)d - %(message)s')


class ResetPasswordTests(StaticLiveServerTestCase):
    selenium = None

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def setUp(self) -> None:
        self.user = CustomUser.objects.create_user("test@test.com", "12345")

    def test_reset_password(self):
        self.selenium.get(f'{self.live_server_url}{reverse("users:password_reset")}')
        email_input = self.selenium.find_element_by_name("email")
        email_input.send_keys(self.user.email)
        submit_button = self.selenium.find_element_by_xpath("/html/body/form/button")
        submit_button.click()
