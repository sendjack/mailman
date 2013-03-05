"""
    urls
    ----

    URLs for the Tornado handlers.

"""
from handlers.send_jack import CommentSendJackHandler
from handlers.vendor import TaskVendorHandler, CommentVendorHandler


url_patterns = [
        (r"/sendjack/task/([0-9]+)/comment", CommentSendJackHandler),

        (r"/vendor/([a-z]+)/task/([0-9]+)", TaskVendorHandler),
        (r"/vendor/([a-z]+)/task/([0-9]+)/comment", CommentVendorHandler),
        ]
