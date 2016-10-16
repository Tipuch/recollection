from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext

from . import models
from .admin_mixins import OwnershipAdminMixin
from .validators import KANJI_PATTERN


@admin.register(models.EnglishWord)
class EnglishWordAdmin(OwnershipAdminMixin):
    list_display = ('word', 'created_at', 'is_complete')
    search_fields = ('readings__romaji', 'readings__hiragana', 'readings__katakana', 'word',
                        'tags__eng_tag', 'tags__jap_tag')
    filter_horizontal = 'readings', 'tags'

    def is_complete(self, obj):
        return ugettext('Yes') if obj.is_complete() else ugettext('No')
    is_complete.short_description = _('Is Complete')


@admin.register(models.JapaneseWord)
class JapaneseWordAdmin(OwnershipAdminMixin):
    filter_horizontal = ('readings', 'kanjis', 'tags')
    list_display = ('word', 'created_at', 'is_complete')
    order_fields = 'created_at'
    search_fields = ('readings__romaji', 'readings__hiragana', 'readings__katakana',
                     'word', 'kanjis__character', 'tags__eng_tag', 'tags__jap_tag')
    readonly_fields = 'created_at',

    def is_complete(self, obj):
        return ugettext('Yes') if obj.is_complete() else ugettext('No')
    is_complete.short_description = _('Is Complete')

    def save_model(self, request, obj, form, change):
        characters = list(obj.word)
        final_kanjis = []
        for character in characters:
            if KANJI_PATTERN.match(character):
                final_kanjis.append(models.Kanji.objects.get_or_create(character=character)[0])
        form.cleaned_data['kanjis'] = final_kanjis
        super(JapaneseWordAdmin, self).save_model(request, obj, form, change)


@admin.register(models.Kanji)
class KanjiAdmin(admin.ModelAdmin):
    filter_horizontal = 'readings',


@admin.register(models.Reading)
class ReadingAdmin(admin.ModelAdmin):
    list_display = ('id', 'romaji', 'hiragana', 'katakana')


@admin.register(models.JapaneseSyllable)
class JapaneseSyllableAdmin(admin.ModelAdmin):
    list_display = ('romaji', 'hiragana', 'katakana')
    ordering = 'hiragana',


@admin.register(models.SearchTag)
class SearchTagAdmin(admin.ModelAdmin):
    pass
