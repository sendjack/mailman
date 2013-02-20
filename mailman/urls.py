"""
    urls
    ----

    URLs for the Tornado handlers.

"""
from handlers.mail import CommentHandler, TaskHandler


url_patterns = [
        (r"/comment", CommentHandler),
        (r"/task", TaskHandler),
        ]
