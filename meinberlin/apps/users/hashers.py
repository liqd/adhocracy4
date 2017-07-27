import hashlib

from django.contrib.auth.hashers import SHA1PasswordHasher
from django.utils.crypto import constant_time_compare
from django.utils.encoding import force_bytes


class A2PasswordHasher(SHA1PasswordHasher):
    """SHA1 based Adhocracy2 password hashes.

    Same as SHA1 hash but password and salt are switched.
    """

    algorithm = "a2"

    def encode(self, password, salt):
        assert password is not None
        assert salt and '$' not in salt
        hash = hashlib.sha1(force_bytes(password + salt)).hexdigest()
        return "%s$%s$%s" % (self.algorithm, salt, hash)

    def verify(self, password, encoded):
        algorithm, salt, hash = encoded.split('$', 2)
        assert algorithm == self.algorithm
        encoded_2 = self.encode(password, salt)
        return constant_time_compare(encoded, encoded_2)
