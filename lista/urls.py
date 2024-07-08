from django.urls import path, re_path

from .views import *

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('resolution/<slug:slug>/<pk>/', ResolutionGenerator.as_view(), name='resolution_version'),
    path('search-lista-cotejo-versiones/', search_list_versiones, name='search_versiones'),
]