from django.shortcuts import render
from django.http import HttpResponse

def main(request):
    """
    Function
    """
    if request.method == 'POST':
        artist = request.POST.get('artist-name')
        return render(request, 'song_markets/search.html', {"artist": artist})
    return render(request, 'song_markets/main.html', {})
