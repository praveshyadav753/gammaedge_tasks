from django.test import RequestFactory
from fastapi import FastAPI, HTTPException, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from datetime import datetime


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/")
def home(request: Request):
    context = {
        "request": request,
        "title": "Dashboard",
        "user": {
            "name": "Abdul",
            "role": "Admin",
            "notifications": 3,
            "is_logged_in": True
        },
        "features": [
            {"title": "API Speed", "enabled": True},
            {"title": "User Authentication", "enabled": True},
            {"title": "Analytics Module", "enabled": False},
            {"title": "Cloud Backup", "enabled": True},
        ],
        "stats": {
            "users": 128,
            "projects": 42,
            "uptime": "99.9%"
        },
        "current_year": datetime.now().year
    }
    return templates.TemplateResponse("home.html", context)

