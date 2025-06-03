from fastapi import FastAPI, Request, Form, UploadFile, File, WebSocket, WebSocketDisconnect
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from auth import register_user, authenticate_user, get_current_user
from models import Base, engine, db_session, User, Message, ChatMembership, Photo
from typing import Dict, List
import os, shutil, uuid

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="super-secret-key")
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
Base.metadata.create_all(bind=engine)

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    user = get_current_user(request)
    if not user:
        return RedirectResponse("/login")
    return templates.TemplateResponse("main.html", {"request": request, "user": user})

@app.get("/register", response_class=HTMLResponse)
async def register_form(request: Request):
    return templates.TemplateResponse("registration.html", {"request": request})

@app.post("/register")
async def register(request: Request,
    name: str = Form(...),
    surname: str = Form(...),
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    password_repeat: str = Form(...)
):
    if password != password_repeat:
        return templates.TemplateResponse("registration.html", {"request": request, "error": "Пароли не совпадают"})
    user = register_user(name, surname, username, email, password)
    if not user:
        return templates.TemplateResponse("registration.html", {"request": request, "error": "Логин уже занят"})
    return RedirectResponse("/login", status_code=303)

@app.get("/login", response_class=HTMLResponse)
async def login_form(request: Request):
    return templates.TemplateResponse("vhod.html", {"request": request})

@app.post("/login")
async def login(request: Request, username: str = Form(...), password: str = Form(...)):
    user = authenticate_user(username, password)
    if not user:
        return templates.TemplateResponse("vhod.html", {"request": request, "error": "Неверный логин или пароль"})
    request.session["user_id"] = user.id
    return RedirectResponse("/", status_code=303)

@app.get("/profile", response_class=HTMLResponse)
async def profile_page(request: Request):
    user = get_current_user(request)
    if not user:
        return RedirectResponse("/login")
    photos = db_session.query(Photo).filter_by(user_id=user.id).all()
    return templates.TemplateResponse("profile.html", {"request": request, "user": user, "photos": photos})

@app.post("/upload/avatar")
async def upload_avatar(request: Request, file: UploadFile = File(...)):
    user = get_current_user(request)
    if not user:
        return RedirectResponse("/login")
    filename = f"{uuid.uuid4()}.png"
    path = f"static/avatars/{filename}"
    with open(path, "wb") as f:
        shutil.copyfileobj(file.file, f)
    user.avatar = filename
    db_session.commit()
    return RedirectResponse("/profile", status_code=303)

@app.post("/upload/photo")
async def upload_photo(request: Request, file: UploadFile = File(...)):
    user = get_current_user(request)
    if not user:
        return RedirectResponse("/login")
    filename = f"{uuid.uuid4()}.png"
    path = f"static/photos/{filename}"
    with open(path, "wb") as f:
        shutil.copyfileobj(file.file, f)
    photo = Photo(user_id=user.id, filename=filename)
    db_session.add(photo)
    db_session.commit()
    return RedirectResponse("/profile", status_code=303)

@app.post("/chat/join/{group}")
async def join_chat(request: Request, group: str):
    user = get_current_user(request)
    if not user:
        return RedirectResponse("/login")
    exists = db_session.query(ChatMembership).filter_by(user_id=user.id, group=group).first()
    if not exists:
        db_session.add(ChatMembership(user_id=user.id, group=group))
        db_session.commit()
    return RedirectResponse(f"/{group}chat", status_code=303)

@app.get("/chats", response_class=HTMLResponse)
async def chats_page(request: Request):
    user = get_current_user(request)
    if not user:
        return RedirectResponse("/login")
    user_chats = db_session.query(ChatMembership).filter_by(user_id=user.id).all()
    chat_names = list(set([chat.group for chat in user_chats]))
    return templates.TemplateResponse("chats.html", {"request": request, "user": user, "chat_names": chat_names})

@app.get("/boevikichat", response_class=HTMLResponse)
async def boeviki_chat(request: Request):
    user = get_current_user(request)
    if not user:
        return RedirectResponse("/login")
    return templates.TemplateResponse("boevikigroup.html", {"request": request, "user": user, "group_name": "boeviki"})

@app.get("/campingchat", response_class=HTMLResponse)
async def camping_chat(request: Request):
    user = get_current_user(request)
    if not user:
        return RedirectResponse("/login")
    return templates.TemplateResponse("campinggroup.html", {"request": request, "user": user, "group_name": "camping"})

@app.get("/catschat", response_class=HTMLResponse)
async def cats_chat(request: Request):
    user = get_current_user(request)
    if not user:
        return RedirectResponse("/login")
    return templates.TemplateResponse("catsgroup.html", {"request": request, "user": user, "group_name": "cats"})

@app.get("/dogschat", response_class=HTMLResponse)
async def dogs_chat(request: Request):
    user = get_current_user(request)
    if not user:
        return RedirectResponse("/login")
    return templates.TemplateResponse("dogsgroup.html", {"request": request, "user": user, "group_name": "dogs"})

@app.get("/hikingchat", response_class=HTMLResponse)
async def hiking_chat(request: Request):
    user = get_current_user(request)
    if not user:
        return RedirectResponse("/login")
    return templates.TemplateResponse("hikinggroup.html", {"request": request, "user": user, "group_name": "hiking"})

@app.get("/runningchat", response_class=HTMLResponse)
async def running_chat(request: Request):
    user = get_current_user(request)
    if not user:
        return RedirectResponse("/login")
    return templates.TemplateResponse("runninggroup.html", {"request": request, "user": user, "group_name": "running"})

@app.get("/scifichat", response_class=HTMLResponse)
async def scifi_chat(request: Request):
    user = get_current_user(request)
    if not user:
        return RedirectResponse("/login")
    return templates.TemplateResponse("scifigroup.html", {"request": request, "user": user, "group_name": "scifi"})

@app.get("/soccerchat", response_class=HTMLResponse)
async def soccer_chat(request: Request):
    user = get_current_user(request)
    if not user:
        return RedirectResponse("/login")
    return templates.TemplateResponse("soccergroup.html", {"request": request, "user": user, "group_name": "soccer"})

@app.get("/cyclingchat", response_class=HTMLResponse)
async def cycling_chat(request: Request):
    user = get_current_user(request)
    if not user:
        return RedirectResponse("/login")
    return templates.TemplateResponse("cyclinggroup.html", {"request": request, "user": user})

@app.get("/chat/messages/{group}")
async def get_messages(group: str):
    messages = db_session.query(Message).filter(Message.group == group).all()
    return [{"username": msg.user.username, "content": msg.content} for msg in messages]

@app.get("/chat/members/{group}")
async def chat_members_count(group: str):
    count = db_session.query(ChatMembership).filter_by(group=group).count()
    return {"count": count}

html_pages = [
    f for f in os.listdir("templates")
    if f.endswith(".html") and f not in ["vhod.html", "registration.html", "cyclinggroup.html", "chats.html", "profile.html"]
]

for page in html_pages:
    route = "/" + page
    template_name = page

    async def page_view(request: Request, template_name=template_name):
        return templates.TemplateResponse(template_name, {"request": request})

    app.add_api_route(route, page_view, methods=["GET"], response_class=HTMLResponse)

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, group: str):
        await websocket.accept()
        if group not in self.active_connections:
            self.active_connections[group] = []
        self.active_connections[group].append(websocket)

    def disconnect(self, websocket: WebSocket, group: str):
        if group in self.active_connections:
            self.active_connections[group].remove(websocket)

    async def broadcast(self, group: str, message: dict):
        for connection in self.active_connections.get(group, []):
            await connection.send_json(message)

manager = ConnectionManager()

@app.websocket("/ws/chat/{group}")
async def websocket_endpoint(websocket: WebSocket, group: str):
    await manager.connect(websocket, group)
    try:
        while True:
            data = await websocket.receive_json()
            user = db_session.query(User).filter(User.username == data["username"]).first()
            if user:
                msg = Message(user_id=user.id, group=group, content=data["content"])
                db_session.add(msg)
                db_session.commit()
                await manager.broadcast(group, {
                    "username": user.username,
                    "content": data["content"]
                })
    except WebSocketDisconnect:
        manager.disconnect(websocket, group)