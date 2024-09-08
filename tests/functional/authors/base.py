import time

from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from resources.utils.browser import chrome_browser


class AuthorsBaseTest(StaticLiveServerTestCase):
    def setUp(self) -> None:
        self.browser = chrome_browser()  # '--headless')

        return super().setUp()

    def tearDown(self) -> None:
        self.browser.quit()

        return super().tearDown()

    def waitFor(self, timeout) -> None:  # noqa: PLR6301
        time.sleep(timeout)
