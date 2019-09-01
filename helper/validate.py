import re
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from apps.admin.postal_code.models import PostalCode


# check katakana japan
def isHarfKana(value):
    return re.match(r"^[゠-ヿ]+$", value) is not None


# check kanji japan
def isHarfKanji(value):
    return re.match(r"^[㐀-䶵一-鿋豈-頻]+$", value) is not None


# check number
def isInteger(value):
    return re.match(r"^\d+$", value) is not None


# check lowercase character
def isAlphaLowerCase(value):
    return re.match(r"^[a-z]+$", value) is not None


# check uppercase character
def isAlphaUpperCase(value):
    return re.match(r"^[A-Z]+$", value) is not None


# check alpha number
def isAlphaNumeric(value):
    return re.match(r"^\w+$", value) is not None


# check ascii symbol
def isAsciiSymbol():
    return ['@', '.', '+', '-', '_']


def validate_key(value):
    for characters in value:
        if not (isInteger(characters) or isAlphaUpperCase(characters) or isAlphaLowerCase(characters)):
            raise ValidationError(
                _('Is not character english, number'),
            )


def validate_version(value):
    item = value.split('.')
    if len(item) != 4:
        raise ValidationError(
                    _('Wrong format. Example: ”aa.bb.cc.dd”'),
                )
    for i in item:
        if not isInteger(i):
            raise ValidationError(
                        _('Wrong format. Example: ”aa.bb.cc.dd”'),
                    )


def validate_furi(value):
    for characters in value:
        if not (isHarfKana(characters) or characters == '\u0020'):
            raise ValidationError(
                _('Is not Furigana'),
            )


def validate_tel(value):
    for characters in value:
        if not (isInteger(characters) or characters == '-'):
            raise ValidationError(
                _('Is not number or -'),
            )


def validate_address_furi(value):
    for characters in value:
        if not (isHarfKana(characters) or isInteger(characters) or characters == '\u0020'):
            raise ValidationError(
                _('Is not Furigana'),
            )


def validate_postal_code(value):
    if not PostalCode.objects.filter(zip=value):
        raise ValidationError(
            _('Postal code not found'),
        )


def validate_activation_pass(value):
    for characters in value:
        if not (isAlphaUpperCase(characters) or isAlphaLowerCase(characters) or isInteger(characters) or characters == '\u0020'):
            raise ValidationError(
                _('Is not character english, number'),
            )


def validate_activate_status_code(value):
    for characters in value:
        if not (isInteger(characters)):
            raise ValidationError(
                _('Is not number'),
            )
