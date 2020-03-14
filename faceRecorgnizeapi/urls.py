from django.urls import path
from . import views


urlpatterns = [
    path(r'getFaces', views.getFaces),
    path(r'getImage', views.getImage),
    path(r'getPersons', views.getPersons),
    path(r'getPersonById', views.getPersonById),
    path(r'getFacesWithName', views.getFacesWithName),
    path(r'changeFacePerson', views.changeFacePerson),
    path(r'changePersonName', views.changePersonName),
    path(r'addNewPersonFace', views.addNewPersonFace),
]