from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
import os
import discord
from discord.ext import commands

# --------------------------
# Environment Variables
# --------------------------
DISCORD_CLIENT_ID = int(os.environ.get("DISCORD_CLIENT_ID"))
DISCORD_CLIENT_SECRET = os.environ.get("DISCORD_CLIENT_SECRET")
DISCORD_REDIRECT_URI = os.environ.get("DISCORD_REDIRECT_URI")
BOT_OWNER_IDS = os.environ.get("BOT_OWNER_IDS", "").split(",")  # comma-separated IDs
SESSION_SECRET = os.environ.get("SESSION_SECRET", "supersecret")

# --------------------------
# FastAPI Setup
# --------------------------
app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key=SESSION_SECRET)
templates = Jinja2Templates(directory="templates")

# --------------------------
# Discord Bot Setup
# --------------------------
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

@app.on_event("startup")
async def startup_event():
    await bot.start(os.environ.get("BOT_TOKEN"))

# --------------------------
# Public Routes
# --------------------------
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

# --------------------------
# OAuth2 Login
# --------------------------
@app.get("/login")
async def login():
    discord_oauth = (
        f"https://discord.com/api/oauth2/authorize"
        f"?client_id={DISCORD_CLIENT_ID}"
        f"&redirect_uri={DISCORD_REDIRECT_URI}"
        f"&response_type=code&scope=identify%20guilds"
    )
    return RedirectResponse(discord_oauth)

# --------------------------
# Callback (Discord OAuth2)
# --------------------------
@app.get("/callback")
async def callback(request: Request, code: str):
    # Placeholder for OAuth2 token exchange & user session setup
    return RedirectResponse("/dashboard")

# --------------------------
# Dashboard
# --------------------------
@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    # Placeholder: show servers owned by the user
    return templates.TemplateResponse("home.html", {"request": request})
