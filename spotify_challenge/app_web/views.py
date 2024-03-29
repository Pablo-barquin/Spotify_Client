from urllib.parse import urlencode, parse_qs, urlparse
from app_web.own_code.spotify_client import SpotifyClient
from django.shortcuts import redirect, render

from django.http import JsonResponse

# Create your views here.
def home(request):
    '''Página simple de inicio con botón para llegar a la zona de autorización'''
    return render(request, "app_web/home.html")

def spotify_auth(request):
    '''Construye la URL de autorización y redirije al usuario a ella'''
    config = SpotifyClient()

    params = {
        "client_id": config.client_id,
        "response_type": "code",
        "redirect_uri": config.redirect_uri,  
        "scope": config.scope,  
        "code_challenge_method": "S256",
        "code_challenge": config.code_challenge
    }

    request.session['code_verifier'] = config.code_verifier
    request.session['access_token'] = None
    url = f"https://accounts.spotify.com/authorize?{urlencode(params)}"

    return redirect(url)

def spotify_callback(request):
    '''Maneja el código de autorización una vez que el usuario es redirigido a la aplicación'''
    query_string = urlparse(request.get_full_path()).query # request.get_full_path() obtiene la url actual.
    params = parse_qs(query_string)
    code = params.get('code', [None])[0]    # Diccionario de parametros. Si encuentra code, devuelve el primer valor, sino None

    config = SpotifyClient()
    if not request.session['access_token'] and code:
        code_verifier = request.session.get('code_verifier')
        request.session['access_token'] = config.get_access_token(code, code_verifier)
    elif not request.session['access_token']:
        return JsonResponse({"error": "No se ha aceptado la solicitud"})

    tracks_info = config.get_top_tracks(request.session['access_token'])
    user_profile = config.get_user_profile(request.session['access_token'])
    tracks_recently = config.get_recently_played_tracks(request.session['access_token'])
    return render(request, 'app_web/user_info.html', {'top_tracks': tracks_info, 'user_profile': user_profile, 'tracks_recently': tracks_recently})