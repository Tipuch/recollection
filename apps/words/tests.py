from django.db.models import Prefetch
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.test import override_settings
from django.urls import reverse

from apps.words.models import Reading, JapaneseWord, Kanji


class TestWords(TestCase):

    fixtures = ['fixtures/jap_syllables.json', 'fixtures/test_readings.json']

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        User = get_user_model()
        User.objects.create_superuser('test@test.com', "12345")

    @classmethod
    def tearDownClass(cls):
        super().setUpClass()
        User = get_user_model()
        User.objects.all().delete()

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

    def test_convert_readings(self):
        client = Client()
        response = client.get(reverse('words:convert_all_readings'))
        self.assertEqual(response.status_code, 302)
        readings = Reading.objects.all()
        self.assertEqual(readings[0].romaji, 'attakai')
        self.assertEqual(readings[0].hiragana, 'あったかい')
        self.assertEqual(readings[0].katakana, 'アッタカイ')
        self.assertEqual(readings[1].romaji, 'taberu')
        self.assertEqual(readings[1].hiragana, 'たべる')
        self.assertEqual(readings[1].katakana, 'タベル')
        self.assertEqual(readings[2].romaji, 'atatakai')
        self.assertEqual(readings[2].hiragana, 'あたたかい')
        self.assertEqual(readings[2].katakana, 'アタタカイ')

    @override_settings(STATICFILES_STORAGE=None)
    def test_add_jp_word_admin(self):
        User = get_user_model()
        user = User.objects.get(email='test@test.com')
        add_dict = {'word': '今晩は', 'owner': user.id}
        self.client.force_login(user)
        post = self.client.post(reverse('admin:words_japaneseword_add'),
                                add_dict)
        self.assertRedirects(post,
                             reverse('admin:words_japaneseword_changelist'))
        jp_word = JapaneseWord.objects.prefetch_related(
            Prefetch(
                lookup='kanjis',
                queryset=Kanji.objects.order_by('character'))).get(word='今晩は')
        kanjis = jp_word.kanjis.all()
        self.assertEqual(len(kanjis), 2)
        self.assertEqual(kanjis[0].character, '今')
        self.assertEqual(kanjis[1].character, '晩')
