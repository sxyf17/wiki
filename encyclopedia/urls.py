from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<str:title>", views.entry, name="entry"),
    path("search/", views.search, name="search"),
    path("random/", views.randEntry, name="randEntry"),
    path("new/", views.newEntry, name="new"),
    path("edit/", views.editEntry, name="edit"),
    path("save/", views.saveEntry, name="save")
    
]

