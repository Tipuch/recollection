from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, JsonResponse
from django.utils.decorators import method_decorator
from django.views.generic import View

from .models import Reading
from .forms import WordsUploadForm


class ConvertAllReadingsView(View):

    @method_decorator(staff_member_required)
    def dispatch(self, request, *args, **kwargs):
        return super(
            ConvertAllReadingsView,
            self).dispatch(
            request,
            *args,
            **kwargs)

    def get(self, request):
        Reading.objects.convert_all()
        content_type = ContentType.objects.get_for_model(Reading)
        return HttpResponseRedirect(reverse(
            'admin:{app}_{model}_changelist'.format(
                **{'app': content_type.app_label, 'model': content_type.model}
            )))


class WordsUploadView(View):
    lang = None

    @method_decorator(staff_member_required)
    def dispatch(self, request, *args, **kwargs):
        return super(WordsUploadView, self).dispatch(request, *args, **kwargs)

    def post(self, request):
        owner = request.user
        form = WordsUploadForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                form.handle_uploaded_file(self.lang, owner)
            except ValueError as e:
                form.add_error("words", str(e))
                return JsonResponse(form.errors.as_json(), status=400)
        else:
            return JsonResponse(form.errors.as_json(), status=400)
