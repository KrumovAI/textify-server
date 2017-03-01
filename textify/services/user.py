import re
import hashlib

from textify.models import User
from textify.exceptions import *
from textify.utils.fill import *


def register_user(email, password, confirm_pass):
    regex = "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

    if re.match(regex, email):
        if password != confirm_pass:
            raise PasswordsDoNotMatchException("Passwords do not much!")
        else:
            if len(password) < 3:
                raise PasswordTooSHortException("Password must have at least 3 characters!")
            else:
                try:
                    email = email.encode('utf-8')
                    User.objects.get(email=email)
                    raise ExistingUsernameException("An account with this email already exists!")
                except User.DoesNotExist:
                    m = hashlib.md5()
                    m.update(password)
                    user = User.objects.create(email=email, password=m.hexdigest())
                    fill_drawings(user)
                    return str(user.id)
    else:
        raise InvalidEmailFormatException("Invalid email format!")


def authenticate_user(email, password):
    try:
        m = hashlib.md5()
        m.update(password)
        user = User.objects.get(email=email, password=m.hexdigest())
        return str(user.id)
    except User.DoesNotExist:
        raise UserDoesNotExistException("Invalid email or password!")
