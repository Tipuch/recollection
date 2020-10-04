from django.urls import path

from .views import ConvertAllReadingsView

app_name = 'words'
urlpatterns = [
    path('readings/convert',
         ConvertAllReadingsView.as_view(),
         name='convert_all_readings'),
]
