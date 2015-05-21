class User:
    id = 0
    screen_name = ""
    fb_user = False
    fb_user_id = 0
    sc_user = False
    loc = ""
    city = ""
    genres = set()

    def __init__(self, _screen_name, _fb_user=False, _fb_user_id=0, _sc_user=False, _city=""):
        self.screen_name = _screen_name
        self.fb_user = _fb_user
        self.fb_user_id = _fb_user_id
        self.sc_user = _sc_user
        self.city = _city

    def add_genre(self, genre=""):
        genre.strip()
        if genre == "":
            return
        self.genres.add(genre)