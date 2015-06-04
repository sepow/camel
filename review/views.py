from django.http import HttpResponse
from django.shortcuts import render

from core.models import BookNode


def index(request):

    books_with_answers = BookNode.objects.filter(node_type="question")

    return render(request, "review/index.html", {"books": books_with_answers})
