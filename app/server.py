from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
import pyotp
from starlette.responses import PlainTextResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pathlib import Path

app = FastAPI()
templates = Jinja2Templates(directory="templates")

VALID_USERNAME = "testuser"
VALID_PASSWORD = "testpass"
TOTP_SECRET = "JBSWY3DPEHPK3PXP"

@app.get("/login", response_class=HTMLResponse)
async def login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login", response_class=HTMLResponse)
async def login(request: Request, username: str = Form(...), password: str = Form(...), totp: str = Form(...)):
    totp_gen = pyotp.TOTP(TOTP_SECRET)
    if username == VALID_USERNAME and password == VALID_PASSWORD and totp == totp_gen.now():
        return PlainTextResponse("Login Successful!")
    return PlainTextResponse("Invalid credentials or TOTP code", status_code=401)

# Create templates directory and place login.html
Path("templates").mkdir(exist_ok=True)
with open("templates/login.html", "w") as f:
    f.write("""
<form method="post">
  Username: <input name="username"><br>
  Password: <input name="password" type="password"><br>
  TOTP Code: <input name="totp"><br>
  <button type="submit">Login</button>
</form>
""")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="127.0.0.1", port=8000, reload=True)
