import re

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

KANJI_PATTERN = re.compile("[\u4e00-\u9fff]")
HIRAGANA_PATTERN = re.compile("[\u3040-\u309f\u30fc]")
KATAKANA_PATTERN = re.compile("[\u30a0-\u30ff]")
ASCII_PATTERN = re.compile("[\u0000-\u007f]")


def validate_jap_char(value):
    for char in value:
        if not (KANJI_PATTERN.match(char) or
                HIRAGANA_PATTERN.match(char) or KATAKANA_PATTERN.match(char)):
            raise ValidationError(
                _('"%(value)s" contains non Japanese character(s)'),
                params={'value': value}
            )


def validate_eng_char(value):
    for char in value:
        if not (ASCII_PATTERN.match(char)):
            raise ValidationError(
                _('"%(value)s" contains non Alphabetical character(s)'),
                params={'value': value}
            )


def validate_hiragana_char(value):
    for char in value:
        if not (HIRAGANA_PATTERN.match(char)):
            raise ValidationError(
                _('"%(value)s" contains non Hiragana character(s)'),
                params={'value': value}
            )


def validate_katakana_char(value):
    for char in value:
        if not (KATAKANA_PATTERN.match(char)):
            raise ValidationError(
                _('"%(value)s" contains non Katakana character(s)'),
                params={'value': value}
            )
