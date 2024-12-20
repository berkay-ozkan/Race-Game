from django.http import HttpResponse

# Create your views here.


def NotImplemented(*args, **kwargs):
    return HttpResponse("This page is yet to be implemented.")
