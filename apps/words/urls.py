from django.conf.urls import url

from .views import ConvertAllReadingsView, WordsUploadView

urlpatterns = [
    url(r'^readings/convert/$', ConvertAllReadingsView.as_view(),
        name='convert_all_readings'),
    url(r'^upload/en/$', WordsUploadView.as_view(lang='en'), name="upload_en"),
    url(r'^upload/jp/$', WordsUploadView.as_view(lang='jp'), name="upload_jp")
]
