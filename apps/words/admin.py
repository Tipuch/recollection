from django.contrib import admin

from .models import *
from .validators import KANJI_PATTERN


@admin.register(EnglishWord)
class EnglishWordAdmin(admin.ModelAdmin):
    list_display = 'word', 'created_at'
    search_fields = ('readings__romaji', 'readings__hiragana', 'readings__katakana', 'word')
    filter_horizontal = 'readings',


@admin.register(JapaneseWord)
class JapaneseWordAdmin(admin.ModelAdmin):
    filter_horizontal = 'readings', 'kanjis'
    list_display = 'word', 'created_at',
    order_fields = 'created_at'
    search_fields = ('readings__romaji', 'readings__hiragana', 'readings__katakana',
                     'word', 'kanjis__character')
    readonly_fields = 'created_at',

    def save_model(self, request, obj, form, change):
        characters = list(obj.word)
        final_kanjis = []
        for character in characters:
            if KANJI_PATTERN.match(character):
                final_kanjis.append(Kanji.objects.get_or_create(character=character)[0])
        form.cleaned_data['kanjis'] = final_kanjis
        super(JapaneseWordAdmin, self).save_model(request, obj, form, change)


@admin.register(Kanji)
class KanjiAdmin(admin.ModelAdmin):
    filter_horizontal = 'readings',


@admin.register(Reading)
class ReadingAdmin(admin.ModelAdmin):
    list_display = ('romaji', 'hiragana', 'katakana')
