from functools import partial, wraps
from django.contrib import admin
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext
from django.conf.urls import url
from django.forms import formset_factory

from . import models, forms, formsets
from .admin_mixins import OwnershipAdminMixin


@admin.register(models.EnglishWord)
class EnglishWordAdmin(OwnershipAdminMixin):
    list_display = ('word', 'is_complete', 'created_at')
    search_fields = ('readings__romaji', 'readings__hiragana',
                     'readings__katakana', 'word',
                     'tags__eng_tag', 'tags__jap_tag')
    filter_horizontal = 'readings', 'tags'
    list_per_page = 30

    def is_complete(self, obj):
        return ugettext('Yes') if obj.is_complete() else ugettext('No')
    is_complete.short_description = _('Is Complete')


@admin.register(models.JapaneseWord)
class JapaneseWordAdmin(OwnershipAdminMixin):
    filter_horizontal = ('readings', 'kanjis', 'tags')
    list_display = ('word', 'is_complete', 'created_at')
    order_fields = 'created_at'
    search_fields = ('readings__romaji', 'readings__hiragana',
                     'readings__katakana', 'word', 'kanjis__character',
                     'tags__eng_tag', 'tags__jap_tag')
    readonly_fields = 'created_at',
    list_per_page = 30

    def is_complete(self, obj):
        return ugettext('Yes') if obj.is_complete() else ugettext('No')
    is_complete.short_description = _('Is Complete')

    def get_urls(self):
        url_patterns = super(JapaneseWordAdmin, self).get_urls()
        info = self.model._meta.app_label, self.model._meta.model_name
        my_urls = [url(r"^add_list/$",
                       self.admin_site.admin_view(self.add_list),
                       name="%s_%s_add_list" % info)]
        return my_urls + url_patterns

    @method_decorator(require_http_methods(["GET", "POST"]))
    def add_list(self, request):
        if not (self.has_add_permission(request) and self.has_add_permission(
                request)) or not request.user.is_superuser:
            return HttpResponse(status=403)
        JpWordFormset = formset_factory(
            wraps(
                forms.JpWordForm)(
                partial(
                    forms.JpWordForm,
                    user=request.user)),
            formset=formsets.BaseJpWordFormset,
            min_num=1)
        if request.method == "POST":
            formset = JpWordFormset(request.POST)
            if formset.is_valid():
                for form in formset:
                    form.save()
                return HttpResponseRedirect(reverse(
                    'admin:{app}_{model}_changelist'.format(
                        **{'app': self.model._meta.app_label,
                           'model': self.model._meta.model_name}
                    )))
        else:
            formset = JpWordFormset()
        context = dict(
            self.admin_site.each_context(request),
        )
        context['opts'] = self.model._meta
        context['formset'] = formset
        context['helper'] = formsets.BaseJpWordFormsetHelper()
        context['has_change_permission'] = self.has_change_permission(request)
        return render(
            request,
            "admin/words/japaneseword/add_list.html",
            context)

    def save_model(self, request, obj, form, change):
        form.cleaned_data['kanjis'] = models.Kanji.objects.get_kanjis(
            obj.word, obj.owner)
        super(JapaneseWordAdmin, self).save_model(request, obj, form, change)


@admin.register(models.Kanji)
class KanjiAdmin(OwnershipAdminMixin):
    filter_horizontal = 'readings',


@admin.register(models.Reading)
class ReadingAdmin(admin.ModelAdmin):
    list_display = ('id', 'romaji', 'hiragana', 'katakana')
    search_fields = ('romaji', 'hiragana', 'katakana')
    list_per_page = 30


@admin.register(models.JapaneseSyllable)
class JapaneseSyllableAdmin(admin.ModelAdmin):
    list_display = ('romaji', 'hiragana', 'katakana')
    search_fields = ('romaji', 'hiragana', 'katakana')
    list_per_page = 30
    ordering = 'hiragana',


@admin.register(models.SearchTag)
class SearchTagAdmin(OwnershipAdminMixin):
    pass
