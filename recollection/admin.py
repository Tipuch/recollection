from django.contrib.admin import AdminSite, site


class CustomAdminSite(AdminSite):
    site_header = 'Recollection'

    def __init__(self, *args, **kwargs):
        super(CustomAdminSite, self).__init__(*args, **kwargs)
        self._registry.update(site._registry)

site = CustomAdminSite()
