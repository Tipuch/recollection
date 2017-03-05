from django.db import models

from .validators import KANJI_PATTERN


class JapaneseSyllableManager(models.Manager):

    def lookup_romaji(self, value):
        return self.get_queryset().get(romaji=value)

    def lookup_hiragana(self, value):
        return self.get_queryset().get(hiragana=value)

    def lookup_katakana(self, value):
        return self.get_queryset().get(katakana=value)

    def lookup_syllable(self, lookup_method, value):
        """
        This method looks up viable Japanese Syllables
        it returns the appropriate JapaneseSyllable object.
        """
        result = None
        for i in reversed(range(1, len(value) + 1)):
            try:
                result = lookup_method(value[:i])
                return result
            except self.model.DoesNotExist:
                continue
        return result


class ReadingManager(models.Manager):

    def convert_all(self):
        for reading in self.get_queryset().all():
            reading.save(force_conversion=True)


class KanjiManager(models.Manager):

    def get_kanjis(self, word, owner):
        return [self.get_queryset().get_or_create(character=character, owner=owner)[0]
                for character in list(word)
                if KANJI_PATTERN.match(character)]
