from django.http import HttpResponse
from django.shortcuts import render

from camel.models import BookNode


def index(request):

    books_with_answers = BookNode.objects.all()

    return render(request, "review/index.html", {"books": books_with_answers})
