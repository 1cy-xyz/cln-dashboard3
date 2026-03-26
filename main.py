import os
import asyncio
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
import discord
from discord.ext import commands

# --------------------------
# Environment Variables
# --------------------------
BOT_TOKEN = os.environ.get("BOT_TOKEN")
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

# --------------------------
# Background Bot Startup
# --------------------------
@app.on_event("startup")
async def startup_event():
    if BOT_TOKEN:
        asyncio.create_task(bot.start(BOT_TOKEN))
    else:
        print("⚠️ BOT_TOKEN not set! Bot will not start.")

# --------------------------
# Public Routes
# --------------------------
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.get("/login")
async def login():
    discord_oauth = (
        f"https://discord.com/api/oauth2/authorize"
        f"?client_id={DISCORD_CLIENT_ID}"
        f"&redirect_uri={DISCORD_REDIRECT_URI}"
        f"&response_type=code&scope=identify%20guilds"
    )
    return RedirectResponse(discord_oauth)

@app.get("/callback")
async def callback(request: Request, code: str):
    # Placeholder for OAuth2 token exchange & user session setup
    return RedirectResponse("/dashboard")

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    # Placeholder: show servers owned by the user
    return templates.TemplateResponse("home.html", {"request": request})
