"""
    urls
    ----

    URLs for the Tornado handlers.

"""
from handlers.mail import CommentHandler


url_patterns = [
        (r"/comment", CommentHandler),
        ]
