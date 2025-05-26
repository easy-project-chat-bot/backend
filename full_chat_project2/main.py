from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from auth import get_current_user, register_user, authenticate_user
from models import Base, engine, Message, User, db_session

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="your-secret-key")
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

Base.metadata.create_all(bind=engine)
connections = set()

@app.get("/", response_class=HTMLResponse)
async def chat_page(request: Request, user: User = Depends(get_current_user)):
    if not user:
        return RedirectResponse("/login")
    messages = db_session.query(Message).all()
    return templates.TemplateResponse("index.html", {"request": request, "user": user, "messages": messages})

@app.get("/register")
async def register_form(request: Request):
    return templates.TemplateResponse("registration.html", {"request": request})

@app.post("/register")
async def register(request: Request, username: str = Form(...), password: str = Form(...)):
    if register_user(username, password):
        return RedirectResponse("/login", status_code=302)
    return templates.TemplateResponse("registration.html", {"request": request, "error": "User exists"})

@app.get("/login")
async def login_form(request: Request):
    return templates.TemplateResponse("vhod.html", {"request": request})

@app.post("/login")
async def login(request: Request, username: str = Form(...), password: str = Form(...)):
    user = authenticate_user(username, password)
    if not user:
        return templates.TemplateResponse("vhod.html", {"request": request, "error": "Invalid credentials"})
    request.session["user"] = user.id
    return RedirectResponse("/", status_code=302)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connections.add(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            for connection in connections:
                await connection.send_text(data)
    except WebSocketDisconnect:
        connections.remove(websocket)