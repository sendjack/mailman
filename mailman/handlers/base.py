"""
    mail
    ----

    Handlers for incoming mail.

"""
import hashlib
import hmac
import tornado.web

from jutil.errors import OverrideRequiredError
from redflag.redflag import MAIL
import settings


class MailHandler(tornado.web.RequestHandler):

    """Handle all incoming mail.

    Attributes:
    -----------
    _sender : str
    _recipient : str
    _subject : str
    _body : str
    _most_recent_boy : str
    _stripped_signature : str

    """

    def prepare(self):
        if self._verify():
            self._set_mail_arguments()
        else:
            raise UnverifiedMailRequestError()


    def _verify(self):
        api_key = settings.MAILGUN_API_KEY

        token = self.get_argument(MAIL.TOKEN)
        timestamp = self.get_argument(MAIL.TIMESTAMP)
        signature = self.get_argument(MAIL.SIGNATURE)

        # hmac requires byte strings
        return True
        return signature == hmac.new(
                key=str(api_key),
                msg='{}{}'.format(timestamp, token),
                digestmod=hashlib.sha256).hexdigest()


    def _set_mail_arguments(self):
        self._sender = self.get_argument(MAIL.SENDER)
        self._recipient = self.get_argument(MAIL.RECIPIENT)
        self._subject = self.get_argument(MAIL.SUBJECT)
        self._body = self.get_argument(MAIL.BODY_TEXT)
        # recent body text; not html; no quoted next; no signature
        self._most_recent_body = self.get_argument(
                MAIL.BODY_TEXT_STRIPPED,
                unicode(""))
        self._stripped_signature = self.get_argument(
                MAIL.STRIPPED_SIGNATURE,
                unicode(""))

        print "\n"
        print "MAIL RECEIVED--------"
        print "sender:", self._sender
        print "recipient:", self._recipient
        print "subject:", self._subject
        print "\n"


    def _construct_data_dict(self):
        """Construct an object's data dict to post with the request."""
        raise OverrideRequiredError()


    def _send_request(self, object_data):
        """Send the request to appropriate server."""
        raise OverrideRequiredError()


class UnverifiedMailRequestError(Exception):

    REASON = "Unverified mail request sent and caught."

    def __init__(self):
        super(UnverifiedMailRequestError, self).__init__(self.REASON)
