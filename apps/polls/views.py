from django.shortcuts import render


def detail(request):
    return render(request, 'meinberlin_polls/poll_detail.html', {})
