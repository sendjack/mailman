"""
    send_jack
    ---------

    Handle incoming mail for Send Jack (web server) from customers.

    Email/Mailgun Prefix: "jack"

    NOTE: We are ignoring incoming SUBJECT lines.

"""
import json
import requests

import settings
from jutil.errors import OverrideNotAllowedError

from .base import MailHandler


class SendJackHandler(MailHandler):

    """Handle all customer mail for Send Jack.

    Attributes
    ----------
    _task_id : id

    """

    def get(self):
        raise OverrideNotAllowedError()


    def post(self, task_id):
        self._task_id = task_id

        object_data = self._construct_data_dict()
        self._send_request(object_data)


    def _send_request(self, object_data):
        """Send the request to appropriate server."""
        url = unicode("http://{}{}/{}").format(
                settings.SEND_JACK_DOMAIN,
                self.OBJECT_PATH,
                self._task_id)

        requests.post(url, data=json.dumps(object_data))


class CommentSendJackHandler(SendJackHandler):

    OBJECT_PATH = unicode("/a/comment")
    TASK_ID = unicode("task_id")
    MESSAGE = unicode("message")
    IS_FROM_CUSTOMER = unicode("is_from_customer")

    def _construct_data_dict(self):
        """Construct an object's data dict to post with the request."""
        message = unicode("{}\n{}").format(
                self._most_recent_body,
                self._stripped_signature)
        message = message.strip()

        return {
                self.TASK_ID: self._task_id,
                self.MESSAGE: message,
                self.IS_FROM_CUSTOMER: True
                }
