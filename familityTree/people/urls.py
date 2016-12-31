from django.conf.urls import url
from .views import PeopleViewSet


people_urls = [
    url(r'peoples/$', PeopleViewSet.as_view({'get': 'list'})),
    url(r'peoples/(?P<pk>\d+)/$', PeopleViewSet.as_view({'get': 'retrieve'}))
]