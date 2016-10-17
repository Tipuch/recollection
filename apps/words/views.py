from django.shortcuts import render
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.views.generic import View
from django.http import HttpResponseRedirect

from apps.words.models import Reading


class ConvertAllReadingsView(View):
    def get(self, request):
        Reading.objects.convert_all()
        content_type = ContentType.objects.get_for_model(Reading)
        return HttpResponseRedirect(reverse('admin:{app}_{model}_changelist'.format(
            **{'app':content_type.app_label, 'model':content_type.model}
        )))
