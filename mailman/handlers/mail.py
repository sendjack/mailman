"""
    mail
    ----

    Handlers for incoming mail.

"""
import hashlib
import hmac
import re
import json
import requests
import tornado.web

from jutil.errors import OverrideRequiredError, OverrideNotAllowedError
from jutil.base_type import to_integer
from redflag.redflag import MAIL
import settings


class MailHandler(tornado.web.RequestHandler):

    """Receive Mail."""

    def get(self):
        raise OverrideNotAllowedError()


    def post(self):
        token = self.get_argument(MAIL.TOKEN)
        timestamp = self.get_argument(MAIL.TIMESTAMP)
        signature = self.get_argument(MAIL.SIGNATURE)
        if self.verify(settings.MAILGUN_API_KEY, token, timestamp, signature):
            self._get_mail_arguments()
            self._process_request()
        else:
            raise UnverifiedMailRequestError()


    def verify(self, api_key, token, timestamp, signature):
        # hmac requires byte strings
        return True
        return signature == hmac.new(
                key=str(api_key),
                msg='{}{}'.format(timestamp, token),
                digestmod=hashlib.sha256).hexdigest()


    def _get_mail_arguments(self):
        self.sender = self.get_argument(MAIL.SENDER)
        self.recipient = self.get_argument(MAIL.RECIPIENT)
        self.subject = self.get_argument(MAIL.SUBJECT)
        self.body = self.get_argument(MAIL.BODY_TEXT)
        # recent body text; not html; no quoted next; no signature
        self.most_recent_body = self.get_argument(
                MAIL.BODY_TEXT_STRIPPED,
                unicode(""))
        self.stripped_signature = self.get_argument(
                MAIL.STRIPPED_SIGNATURE,
                unicode(""))

        print "\n"
        print "MAIL RECEIVED--------"
        print "sender:", self.sender
        print "recipient:", self.recipient
        print "subject:", self.subject
        print "\n"


    def _process_request(self):
        raise OverrideRequiredError()


class CommentHandler(MailHandler):

    """Handle emailed in Comments from any vendor and send them to
    Jackalope."""

    email_regex = unicode(r"(.+)\-(\d+)@")
    email_pattern = re.compile(email_regex)

    def _process_request(self):
        match = self.email_pattern.match(self.recipient)
        service = match.group(1)
        task_id = to_integer(match.group(2))

        if service and task_id:
            message = unicode("{}:\n{}\n{}").format(
                    self.subject,
                    self.most_recent_body,
                    self.stripped_signature)
            message = message.strip()

            url = unicode("http://{}/{}{}{}").format(
                    settings.JACKALOPE_DOMAIN,
                    service,
                    settings.JACKALOPE_COMMENT_PATH,
                    task_id)

            data_dict = {"message": message}
            requests.post(url, data=json.dumps(data_dict))

        # note: other MIME headers are also posted here...

        # attachments
        #for file in self.request.files:
        #    # do something with the file
        #    pass

        # returned text is ignored but HTTP status code matters. mailgun wants
        # to see 2xx, otherwise it will make another attempt in 5 minutes.
        # tornado finishes requests automatically


class TaskHandler(MailHandler):

    """Handle emailed notification Tasks from any vendor and send them to
    Jackalope."""

    email_regex = unicode(r"(.+)\-(.+)\-(\d+)@")
    email_pattern = re.compile(email_regex)

    def _process_request(self):
        match = self.email_pattern.match(self.recipient)
        service = match.group(1)
        type = match.group(2)
        task_id = to_integer(match.group(3))

        if service and type and task_id:
            url = unicode("http://{}/{}{}{}").format(
                settings.JACKALOPE_DOMAIN,
                service,
                settings.JACKALOPE_TASK_PATH,
                task_id)

            requests.get(url)


class UnverifiedMailRequestError(Exception):

    REASON = "Unverified mail request sent and caught."

    def __init__(self):
        super(UnverifiedMailRequestError, self).__init__(self.REASON)
