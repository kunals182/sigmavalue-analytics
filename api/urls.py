from django.urls import path
from .views import UploadExcelView, test_api, analyze_query

urlpatterns = [
    path("test/", test_api),
    path("upload/", UploadExcelView.as_view()),
    path("analyze/", analyze_query),
]
