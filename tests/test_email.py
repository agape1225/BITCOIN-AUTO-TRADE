from pusher.email import Email


class EmailTestCase():
    def test_send_email(self):
        Email().send_mail("test mail document", "scg9268@naver.com")


EmailTestCase().test_send_email()
