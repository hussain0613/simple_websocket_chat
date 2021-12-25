from fastapi import FastAPI, Response, WebSocket, WebSocketDisconnect
import json

from utils import WebSocketManager, read_settings

app: FastAPI = FastAPI()


websocket_manager: WebSocketManager = WebSocketManager()
settings: dict = read_settings()


@app.get("/")
async def index():
    with open("www/index.html", "br") as f:
        return Response(content=f.read(), media_type="text/html")


@app.get("/statics/js/{script_file_name}")
async def get_script(script_file_name: str):
    with open(f"www/statics/js/{script_file_name}", "br") as f:
        return Response(content=f.read(), media_type="text/javascript")

@app.get("/statics/css/{script_file_name}")
async def get_script(script_file_name: str):
    with open(f"www/statics/css/{script_file_name}", "br") as f:
        return Response(content=f.read(), media_type="text/css")


@app.post("/login")
async def login(creds: dict[str, str]):
    if creds["display_name"] == "" or creds["display_name"].lower() == "server":
        content = {"message": "You can't be the server!"}
        return Response(content=json.dumps(content).encode(), status_code=403, media_type="application/json")
    
    if "#" in creds["display_name"]:
        content = {"message": "You can't have a # in your display name!"}
        return Response(content=json.dumps(content).encode(), status_code=403, media_type="application/json")
    
    if creds["password"] in settings.get("passwords"):
        
        display_name: str = creds["display_name"]
        if display_name in websocket_manager.users:
            websocket_manager.users[display_name] += 1
            display_name += f"#{websocket_manager.users[display_name]}"

        content = {"message": f"Successfully logged in as {display_name}!"}
        return Response(content=json.dumps(content).encode(), status_code=200, headers={"Set-Cookie": f"display_name={display_name}"}, media_type="application/json")
    
    content = {"message": "Invalid display_name or password!"}
    return Response(content=json.dumps(content).encode(), status_code=401, media_type="application/json")


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    try:
        await websocket.accept()
        await websocket_manager.add_websocket(websocket, websocket.cookies.get("display_name"))
        while True:
            data = await websocket.receive_json()
            await websocket_manager.broadcast(websocket_manager.get_display_name(websocket), data["message"])

    except WebSocketDisconnect:
        display_name = websocket_manager.get_display_name(websocket)
        await websocket_manager.remove_websocket(websocket)
        print(f"{display_name} disconnected!")

