import enum


class GrantType(str, enum.Enum):
    PASSWORD = 'password'
    CLIENT_CREDENTIALS = 'client_credentials'

    @classmethod
    def is_type(cls, _type):
        if not isinstance(_type, str):
            return False
        if cls.PASSWORD.value == _type:
            return True
        if cls.CLIENT_CREDENTIALS.value == _type:
            return True
        return False

    @classmethod
    def ls(cls):
        ls = list()
        ls.append(cls.PASSWORD.value)
        ls.append(cls.CLIENT_CREDENTIALS.value)
        return ls
