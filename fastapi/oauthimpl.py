from fastapi import FastAPI, Request
from starlette.middleware.sessions import SessionMiddleware
from authlib.integrations.starlette_client import OAuth, OAuthError
from starlette.responses import RedirectResponse
import json

app = FastAPI()

# SessionMiddleware is required for OAuth state validation
app.add_middleware(SessionMiddleware, secret_key="secreast_key")

oauth = OAuth()
oauth.register(
    name='google',
    client_id='YOUR_GOOGLE_CLIENT_ID',
    client_secret='YOUR_GOOGLE_CLIENT_SECRET',
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'}
)

@app.get('/')
async def homepage(request: Request):
    user = request.session.get('user')
    if user:
        return {"message": f"Hello {user['name']}", "user": user}
    return {"message": "Not logged in", "login_url": "/login"}

@app.get('/login')
async def login(request: Request):
    # This generates the Google login URL and redirects the user
    redirect_uri = request.url_for('auth')
    return await oauth.google.authorize_redirect(request, redirect_uri)

@app.get('/auth')
async def auth(request: Request):
    try:
        # Token exchange: code -> access_token
        token = await oauth.google.authorize_access_token(request)
    except OAuthError as error:
        return {"error": error.error}
    
    user = token.get('userinfo')
    if user:
        request.session['user'] = dict(user)
    return RedirectResponse(url='/')

@app.get('/logout')
async def logout(request: Request):
    request.session.pop('user', None)
    return RedirectResponse(url='/')



# //////////////////////////////////////////////////////////////

# from httpx_oauth.clients.google import GoogleOAuth2
# from fastapi_users import FastAPIUsers

# google_client = GoogleOAuth2("CLIENT_ID", "CLIENT_SECRET")

# # Then add the router to your app
# app.include_router(
#     fastapi_users.get_oauth_router(google_client, auth_backend, "JWT_SECRET"),
#     prefix="/auth/google",
#     tags=["auth"],
# )