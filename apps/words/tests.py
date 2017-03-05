from django.test import TestCase

from apps.words.models import Reading


class TestWords(TestCase):

    fixtures = ['fixtures/jap_syllables.json']

    def test_convert_from_hiragana(self):
        reading = Reading(hiragana='あったかあい')
        syllables = reading.convert_from_japanese_character(Reading.HIRAGANA)
        romaji_list = [syllable.romaji for syllable in syllables]
        hiragana_list = [syllable.hiragana for syllable in syllables]
        katakana_list = [syllable.katakana for syllable in syllables]
        self.assertEqual(romaji_list, ['a', 't', 'ta', 'ka', 'a', 'i'])
        self.assertEqual(katakana_list, list('アッタカアイ'))
        self.assertEqual(hiragana_list, list('あったかあい'))

    def test_convert_from_katakana(self):
        reading = Reading(katakana='アッタカーイ')
        syllables = reading.convert_from_japanese_character(Reading.KATAKANA)
        romaji_list = [syllable.romaji for syllable in syllables]
        katakana_list = [syllable.katakana for syllable in syllables]
        hiragana_list = [syllable.hiragana for syllable in syllables]
        self.assertEqual(romaji_list, ['a', 't', 'ta', 'ka', 'a', 'i'])
        self.assertEqual(katakana_list, list('アッタカアイ'))
        self.assertEqual(hiragana_list, list('あったかあい'))

    def test_convert_from_romaji(self):
        reading = Reading(romaji='attakaai')
        syllables = reading.convert_from_romaji()
        romaji_list = [syllable.romaji for syllable in syllables]
        katakana_list = [syllable.katakana for syllable in syllables]
        hiragana_list = [syllable.hiragana for syllable in syllables]
        self.assertEqual(romaji_list, ['a', 't', 'ta', 'ka', 'a', 'i'])
        self.assertEqual(katakana_list, list('アッタカアイ'))
        self.assertEqual(hiragana_list, list('あったかあい'))

    def test_convert_global_romaji(self):
        reading = Reading(romaji='attakaai')
        reading.convert()
        self.assertEqual(reading.romaji, 'attakaai')
        self.assertEqual(reading.katakana, 'アッタカーイ')
        self.assertEqual(reading.hiragana, 'あったかあい')

    def test_convert_global_katakana(self):
        reading = Reading(katakana='アッタカーイ')
        reading.convert()
        self.assertEqual(reading.romaji, 'attakaai')
        self.assertEqual(reading.katakana, 'アッタカーイ')
        self.assertEqual(reading.hiragana, 'あったかあい')

    def test_convert_global_hiragana(self):
        reading = Reading(hiragana='あったかあい')
        reading.convert()
        self.assertEqual(reading.romaji, 'attakaai')
        self.assertEqual(reading.katakana, 'アッタカーイ')
        self.assertEqual(reading.hiragana, 'あったかあい')
