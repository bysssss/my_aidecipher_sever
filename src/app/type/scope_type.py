import enum


class ScopeType(str, enum.Enum):
    ADMIN = 'ADMIN'
    USER = 'USER'

    @classmethod
    def admin_level(cls):
        ls = list()
        ls.append(cls.ADMIN.value)
        return ls

    @classmethod
    def user_level(cls):
        ls = list()
        ls.append(cls.ADMIN.value)
        ls.append(cls.USER.value)
        return ls
