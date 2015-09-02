from configure import db
from models.user import User
from bson import ObjectId


def __user_from_document(d=None):
    if d is None:
        return None
    # User object uses id as attribute
    d['id'] = d['_id']
    d.pop('_id')
    return User(**d)


def get_user(_id=None, _fb_id=None):
    if _id is None and _fb_id is None:
        raise ValueError("Either _id of _fb_id must be provided")
    # priority goes to object id then to other ids
    res = None
    if _id is not None:
        if isinstance(_id, str):
            _id = ObjectId(_id)
        res = db.user.find_one({'_id': _id})
    elif _fb_id is not None:
        res = db.user.find_one({'fb_user_id', _fb_id})
    return __user_from_document(res)


def create_user(_screen_name=None, _fb_user_id=None):
    if _screen_name is None or len(_screen_name) == 0:
        raise ValueError("Cannot create user without a name")
    u = User
    u.screen_name = _screen_name
    if _fb_user_id is not None:
        u.is_fb_user = True
        u.fb_user_id = _fb_user_id
    else:
        u.is_fb_user = False
        u.fb_user_id = -1
    u_dict = u._asdict()
    # dont save to db with id attribute. default _id attribute replaces this
    u_dict.pop('id')
    db.user.insert_one(u_dict)
    return True


def get_or_create_user(_fb_id=None):
    res = None
    if _fb_id is not None:
        res = get_user(_fb_id=_fb_id)
        # not in db so must create the user
        if res is None:
            # get the screen name
            name = 'yoyo'
    return
