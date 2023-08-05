import re
from django.utils.text import slugify
import string, random, re


def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return "".join(random.choice(chars) for _ in range(size))


def unique_slug_generator(instance, new_slug=None):
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.full_name)
    klass = instance.__class__
    qs_exists = klass.objects.filter(slug=slug).exists()
    if qs_exists:
        new_slug = "{slug}--{randstr}".format(
            slug=slug, randstr=random_string_generator(size=4)
        )
        return unique_slug_generator(instance, new_slug=new_slug)
    return slug


def validate_password(password):
    pattern = r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
    p = re.compile(pattern)
    if re.search(p, password):
        return True
    return False


def validate_phone(phone):
    pattern = r"^(?:\+977|977|0)?(?:98[4-7]|97[7-8]|96[4-6]|985|984|980|981|982|961|962|988|960|972|963|972|973|974|975|976|977|978|980|981|982|983|984|985|986)\d{7}$"
    if not re.match(pattern, str(phone)):
        return False
    return True


def validate_email(email):
    url_pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    p = re.compile(url_pattern)
    if re.search(p, email):
        return True
    return False


def validate_url(image):
    url_pattern = (
        "((http|https)://)(www.)?"
        + "[a-zA-Z0-9@:%._\\+~#?&//=]"
        + "{2,256}\\.[a-z]"
        + "{2,6}\\b([-a-zA-Z0-9@:%"
        + "._\\+~#?&//=]*)"
    )
    p = re.compile(url_pattern)
    if re.search(p, image):
        return True
    return False


def validate_uuid(id):
    uuid_pattern = "^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"
    p = re.compile(uuid_pattern)
    if re.match(p, id):
        return True
    return False
