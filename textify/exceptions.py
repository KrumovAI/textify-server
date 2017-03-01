class InvalidEmailFormatException(Exception):
    pass


class UserDoesNotExistException(Exception):
    pass


class ExistingUsernameException(Exception):
    pass


class PasswordsDoNotMatchException(Exception):
    pass


class PasswordTooSHortException(Exception):
    pass


class WrongEmailOrPasswordException(Exception):
    pass


class MachineCurrentlyTrainingException(Exception):
    pass
