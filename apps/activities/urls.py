from django.conf.urls import url


from . import views

urlpatterns = [
    url(r'^all/$',
        views.AllActivitiesView.as_view(),
        name='activities-all'),
]
