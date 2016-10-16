from django.db import models


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
        for i in reversed(range(1, len(value)+1)):
            result = None
            try:
                result = lookup_method(value[:i])
                return result
            except self.model.DoesNotExist:
                continue
        return result


class ReadingManager(models.Manager):
    def convert_all_readings(self):
        for reading in self.get_queryset().all():
            if reading.romaji:
                reading.field_tracker.changed()['romaji'] = reading.romaji
            elif reading.hiragana:
                reading.field_tracker.changed()['hiragana'] = reading.hiragana
            elif reading.katakana:
                reading.field_tracker.changed()['katakana'] = reading.katakana
            reading.save()
