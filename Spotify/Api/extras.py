from .models import Token
from django.utils import timezone
from datetime import timedelta
from requests import post, get, Request
from requests.exceptions import HTTPError, RequestException
from .credentials import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI

BASE_URL = 'https://api.spotify.com/v1/me/'

# Verificar tokens
def check_tokens(session_id):
    try:
        return Token.objects.get(user=session_id)
    except Token.DoesNotExist:
        return None

# Crear o actualizar tokens en el modelo
def create_or_update_tokens(session_id, access_token, refresh_token, expires_in, token_type):
    tokens = check_tokens(session_id)
    
    if expires_in is None:
        expires_in = 3600  # Valor predeterminado, por ejemplo, 1 hora
    else:
        expires_in = int(expires_in)
    
    expires_in = timezone.now() + timedelta(seconds=expires_in)
    
    if tokens:
        tokens.access_token = access_token
        tokens.refresh_token = refresh_token
        tokens.expires_in = expires_in
        tokens.token_type = token_type
        tokens.save(update_fields=['access_token', 'refresh_token', 'expires_in', 'token_type'])
    else:
        tokens = Token(
            user=session_id,
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=expires_in,
            token_type=token_type
        )
        tokens.save()

# Verificar si el usuario está autenticado en Spotify
def is_spotify_authenticated(session_id):
    tokens = check_tokens(session_id)
    if tokens:
        if tokens.expires_in <= timezone.now():
            refresh_token_fun(session_id)
        return True
    return False

# Refrescar el token
def refresh_token_fun(session_id):
    tokens = check_tokens(session_id)
    if tokens is None:
        return {'Error': 'Token no encontrado para refrescar'}
    
    refresh_token = tokens.refresh_token

    try:
        response = post('https://accounts.spotify.com/api/token', data={
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token,
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET
        }).json()
        
        access_token = response.get('access_token')
        expires_in = response.get('expires_in')
        token_type = response.get('token_type')
        
        if not access_token or not expires_in:
            return {'Error': 'Error al refrescar el token'}
        
        create_or_update_tokens(
            session_id=session_id,
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=expires_in,
            token_type=token_type
        )
    except Exception as e:
        return {'Error': str(e)}

# Ejecutar la solicitud a Spotify
def spotify_request_execution(session_id, endpoint):
    token = check_tokens(session_id)
    
    if token is None:
        return {'Error': 'Token no encontrado o no válido'}
    
    headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + token.access_token}
    
    try:
        response = get(BASE_URL + endpoint, headers=headers)
        response.raise_for_status()  # Lanza una excepción si la respuesta HTTP es un error
        return response.json()
    except HTTPError as http_err:
        return {'Error': f'HTTP error occurred: {http_err}'}
    except RequestException as req_err:
        return {'Error': f'Request error occurred: {req_err}'}
    except Exception as err:
        return {'Error': f'Other error occurred: {err}'}
