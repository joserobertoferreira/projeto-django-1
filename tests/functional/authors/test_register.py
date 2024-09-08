from authors.base import AuthorsBaseTest


class AuthorsRegisterTest(AuthorsBaseTest):
    def test_register_view_success(self):
        self.browser.get(self.live_server_url + '/authors/register/')

        self.waitFor()
