from django.conf.urls import url

from .views import ConvertAllReadingsView

urlpatterns = [
    url(r'^readings/convert', ConvertAllReadingsView.as_view(), name='convert_all_readings'),
]
