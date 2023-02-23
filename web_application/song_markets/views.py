from django.shortcuts import render
from django.http import HttpResponse

def main(request):
    return render(request, 'song_markets/index.html', {})
