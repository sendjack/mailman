"""
    vendor
    ------

    Handle incoming mails from vendors for Jackalope (web server).

    Email/Mailgun Prefix: "[vendor_name]"

"""
import json
import requests

from jutil.errors import OverrideNotAllowedError
import settings

from .base import MailHandler


class VendorHandler(MailHandler):

    """Handle mail from vendors for Jackalope.

    Attributes:
    _vendor : str
    _task_id : id
    _object_data : dict

    """

    def get(self):
        raise OverrideNotAllowedError()


    def post(self, vendor, task_id):
        self._vendor = vendor
        self._task_id = task_id

        object_data = self._construct_data_dict()
        self._send_request(object_data)


    def _send_request(self, object_data):
        """Send the request to appropriate server."""
        url = unicode("http://{}/{}{}/{}").format(
                settings.JACKALOPE_DOMAIN,
                self._vendor,
                self.OBJECT_PATH,
                self._task_id)

        requests.post(url, data=json.dumps(object_data))


class TaskVendorHandler(VendorHandler):

    OBJECT_PATH = unicode("/task")

    def _construct_data_dict(self):
        """Construct an object's data dict to post with the request."""
        return {}


class CommentVendorHandler(VendorHandler):

    OBJECT_PATH = unicode("/comment")
    MESSAGE = unicode("message")

    def _construct_data_dict(self):
        """Construct an object's data dict to post with the request."""
        message = unicode("{}\n{}").format(
                self._most_recent_body,
                self._stripped_signature)
        message = message.strip()

        return {self.MESSAGE: message}

        # note: other MIME headers are also posted here...

        # attachments
        #for file in self.request.files:
        #    # do something with the file
        #    pass

        # returned text is ignored but HTTP status code matters. mailgun wants
        # to see 2xx, otherwise it will make another attempt in 5 minutes.
        # tornado finishes requests automatically
