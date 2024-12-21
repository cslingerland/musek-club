from django.urls import path

from . import views

app_name = 'clubs'
urlpatterns = [
    path("", views.ClubListView.as_view(), name="clubs"),
    path("new/", views.ClubFormView.as_view(), name='club-create'),
    path("<slug:slug>/", views.ClubView.as_view(), name="club"),
    path("<slug:slug>/<int:pk>", views.PickView.as_view(), name="pick"),
    path("<slug:slug>/new-pick/", views.PickFormView.as_view(), name="pick-create")
]