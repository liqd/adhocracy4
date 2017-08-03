from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^request/$',
        views.InitiatorRequestView.as_view(),
        name='initiator_request'),
]
