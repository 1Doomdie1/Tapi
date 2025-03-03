from os       import getenv
from unittest import skipIf

def premium_test(func):
    return skipIf(getenv("SKIP_PREMIUM_TESTS") == "1", "Skipping premium test")(func)