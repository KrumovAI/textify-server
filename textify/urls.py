from django.conf.urls import url

from . import views

urlpatterns = [
    # ex: /polls/
    url(r'^$', views.textify, name='textify'),
    url(r'^handwritten$', views.textify_handwritten, name='textify_handwritten'),
    url(r'^drawings$', views.get_drawings, name='drawings'),
    url(r'^drawings/upload$', views.upload_drawings, name='drawings_upload'),
    url(r'^train$', views.train_machines, name='train'),
    url(r'^register$', views.register, name='register'),
    url(r'^login$', views.login, name='login'),
]
