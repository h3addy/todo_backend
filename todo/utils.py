import string
import random
import uuid
from .models import AppUser


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def generateAccessToken():
    token = uuid.uuid3(uuid.NAMESPACE_DNS, id_generator())
    try:
        AppUser.objects.get(accessToken=token)
        generateAccessToken()
    except AppUser.DoesNotExist:
        return token
