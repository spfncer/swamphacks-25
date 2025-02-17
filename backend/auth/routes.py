from urllib.parse import quote_plus, urlencode
from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse, HTMLResponse

from auth.config import auth0_config, oauth

auth_router = APIRouter()


@auth_router.get("/login", tags=["Authentication Functions"])
async def login(request: Request):
    """
    Redirects the user to the Auth0 Universal Login (https://auth0.com/docs/authenticate/login/auth0-universal-login)
    """
    if "id_token" not in request.session:
        return await oauth.auth0.authorize_redirect(
            request, redirect_uri=request.url_for("callback")
        )
    return RedirectResponse(url="/")


@auth_router.get("/signup", tags=["Authentication Functions"])
async def signup(request: Request):
    """
    Redirects the user to the Auth0 Universal Login (https://auth0.com/docs/authenticate/login/auth0-universal-login)
    """
    if "id_token" not in request.session:  # it could be userinfo instead of id_token
        return await oauth.auth0.authorize_redirect(
            request, redirect_uri=request.url_for("callback"), screen_hint="signup"
        )
    return RedirectResponse(url="/")


@auth_router.get("/logout", tags=["Authentication Functions"])
def logout(request: Request):
    """
    Redirects the user to the Auth0 Universal Login (https://auth0.com/docs/authenticate/login/auth0-universal-login)
    """
    response = RedirectResponse(
        url="https://"
        + auth0_config["DOMAIN"]
        + "/v2/logout?"
        + urlencode(
            {
                "returnTo": request.url_for("read_root"),
                "client_id": auth0_config["CLIENT_ID"],
            },
            quote_via=quote_plus,
        )
    )
    request.session.clear()
    return response  # 👈 updated code


@auth_router.get("/callback", tags=["Authentication Functions"])
async def callback(request: Request):
    """
    Callback redirect from Auth0
    """
    token = await oauth.auth0.authorize_access_token(request)
    # Store `id_token`, and `userinfo` in session
    request.session["id_token"] = token["id_token"]
    request.session["userinfo"] = token["userinfo"]

    return RedirectResponse(url="/login_successful")  # 👈 updated code

@auth_router.get("/profile", tags=["Authentication Functions"])
async def profile(request: Request):
    if "userinfo" in request.session:
        return {**{"auth": True}, **request.session["userinfo"]}
    else:
        return {"auth": False}

# Define a route for login success
@auth_router.get("/login_successful", tags=["Authentication Functions"], response_class=HTMLResponse)
async def login_successful():
    with open("static/login_successful.html", "r") as file:
        html_content = file.read()
    return HTMLResponse(content=html_content)
