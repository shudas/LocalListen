from collections import namedtuple

class User(namedtuple('User', ['id', 'screen_name', 'is_fb_user', 'fb_user_id'])):
    __slots__ = ()

    def get_fb_id(self):
        if self.is_fb_user:
            return self.fb_user_id
        return None
