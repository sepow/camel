from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import View

from core.models import BookNode, Module


class StaffRequiredMixin(object):

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise PermissionDenied
        return super(StaffRequiredMixin, self).dispatch(request, *args, **kwargs)


class ReviewIndexView(StaffRequiredMixin, View):

    def get(self, request):
        books_with_answers = BookNode.objects.filter(node_type="question")
        modules = Module.objects.all()
        return render(request, "review/index.html", {"books": books_with_answers, "modules": modules})


class ReviewBookView(StaffRequiredMixin, View):

    def get(self, request):
        books = BookNode.objects.filter(node_type="question")
        return ""



class ReviewQuestionView(StaffRequiredMixin, View):

    def get(self, request, question_pk):
        question = BookNode.objects.get(pk=question_pk)
        return render(request, "review/question.html", {"question": question})
