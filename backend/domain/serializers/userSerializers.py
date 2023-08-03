class UserSerializer:
    def __init__(self, user):
        self.data = {key: getattr(user, key) for key in user.__dict__ if not key.startswith("_")}

    def to_dict(self):
        return self.data
