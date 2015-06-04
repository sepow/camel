from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.ReviewIndexView.as_view()),
    url(r'^question/(?P<question_pk>[0-9]+)/$', views.ReviewQuestionView.as_view())
]
