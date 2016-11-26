from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect


class OwnershipAdminMixin(admin.ModelAdmin):

    def save_model(self, request, obj, form, change):
        if not getattr(obj, 'id'):
            obj.owner = request.user
        super(OwnershipAdminMixin, self).save_model(request, obj, form, change)

    def get_form(self, request, obj, **kwargs):
        if not request.user.is_superuser:
            exclude = kwargs.get('exclude', []) + ['owner']
            readonly_fields = self.get_readonly_fields(request, obj)
            exclude.extend(readonly_fields)
            kwargs.update({'exclude': exclude})
            return super(OwnershipAdminMixin, self).get_form(request, obj,
                                                             **kwargs)
        form = super(OwnershipAdminMixin, self).get_form(request, obj,
                                                         **kwargs)
        if not obj and request.user.is_superuser:
            form.base_fields['owner'].initial = request.user
        return form

    def get_queryset(self, request):
        qs = super(OwnershipAdminMixin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(owner=request.user)

    def change_view(self, request, object_id, **kwargs):
        content_type = ContentType.objects.get_for_model(self.model)
        if not self.get_queryset(request).filter(id=object_id).exists():
            return HttpResponseRedirect(reverse(
                'admin:{app}_{model}_changelist'.format(
                    **{'app': content_type.app_label,
                       'model': content_type.model}
                )))

        return super(OwnershipAdminMixin, self).change_view(request, object_id,
                                                            **kwargs)

    def delete_view(self, request, object_id, **kwargs):
        content_type = ContentType.objects.get_for_model(self.model)
        if not self.get_queryset(request).filter(id=object_id).exists():
            return HttpResponseRedirect(reverse(
                'admin:{app}_{model}_changelist'.format(
                    **{'app': content_type.app_label,
                       'model': content_type.model}
                )))

        return super(OwnershipAdminMixin, self).delete_view(request, object_id,
                                                            **kwargs)

    def history_view(self, request, object_id, **kwargs):
        content_type = ContentType.objects.get_for_model(self.model)
        if not self.get_queryset(request).filter(id=object_id).exists():
            return HttpResponseRedirect(reverse(
                'admin:{app}_{model}_changelist'.format(
                    **{'app': content_type.app_label,
                       'model': content_type.model}
                )))

        return super(OwnershipAdminMixin, self).history_view(
            request, object_id, **kwargs
        )
