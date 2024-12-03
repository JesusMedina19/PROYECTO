# ...existing code...

AUTHENTICATION_BACKENDS = [
    'Inventario.authentication.CustomAuthBackend',
]

AUTH_USER_MODEL = 'Inventario.Usuario'

LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'categorias'  
LOGOUT_REDIRECT_URL = 'login'

# ...existing code...