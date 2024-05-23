from fastapi import FastAPI, Request, Depends, status
from starlette.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_redoc_html, get_swagger_ui_html
from app.api.api_v1.api import api_router
from app.core.config import EnvConfig, settings
from fastapi.staticfiles import StaticFiles
from fastapi.security import HTTPBasic,  HTTPBasicCredentials
import secrets
from app.api.exceptions import HTTPException


app = FastAPI(
    docs_url=None,
    redoc_url=None,
)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

security = HTTPBasic()


def get_current_dev_username(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, "user")
    correct_password = secrets.compare_digest(credentials.password, "password")
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html(username: str = Depends(get_current_dev_username)):
    print(f"{username} accessed /docs")
    return get_swagger_ui_html(
        title=settings.PROJECT_NAME,
        openapi_url=f"/openapi.json",
        swagger_js_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5.11.6/swagger-ui-bundle.js",
        swagger_css_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5.11.6/swagger-ui.css",
    )

@app.get("/redoc", include_in_schema=False)
async def custom_swagger_ui_html(username: str = Depends(get_current_dev_username)):
    print(f"{username} accessed /redoc")
    return get_redoc_html(
        title=settings.PROJECT_NAME,
        openapi_url=f"/openapi.json",
        redoc_js_url="https://cdn.jsdelivr.net/npm/redoc@2.1.4/bundles/redoc.standalone.js",
    )

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    if settings.ENV_CONFIG == EnvConfig.PROD:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
    elif settings.ENV_CONFIG == EnvConfig.STAG:
        # CORS set for a frontend app in staging environment deployed on any Vercel Preview - Modify this accordingly to match the pattern of your preview environment or more strictly to match the url of your staging deployment. Mobile apps do not need any specific CORS settings to be able to call the backend
        app.add_middleware(
            CORSMiddleware,
            allow_origin_regex="https://.*\.vercel\.app",  # noqa
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
    elif settings.ENV_CONFIG == EnvConfig.DEV:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
    else:
        raise Exception(f"Provide ENV_CONFIG: {settings.ENV_CONFIG} is not supported")

app.include_router(api_router, prefix=settings.API_V1_STR)
