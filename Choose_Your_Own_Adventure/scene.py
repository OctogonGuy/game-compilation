"""
Represents a scene in Choose your own Adventure. It has a
title and a body.
"""
class Scene():
    """Represents a scene."""
    def __init__(self, title, body):
        self.title = title
        self.body = body

    def get_title(self):
        """Returns the title"""
        return self.title

    def get_body(self):
        """Returns the body"""
        return self.body

    def __str__(self):
        return self.title + \
               '\n' + self.body