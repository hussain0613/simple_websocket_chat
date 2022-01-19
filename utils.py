import json
from fastapi import WebSocket

## a class to manage websocket connections
class WebSocketManager:
    """
    A class to manage websocket connections
    """
    def __init__(self):
        self.active_websockets: dict[WebSocket, str] = {}
        self.users: dict[str, int] = {}
    
    async def add_websocket(self, websocket: WebSocket, display_name: str):
        if display_name not in self.users:
            self.users[display_name] = 1
        else:
            self.users[display_name] += 1
            display_name += f"#{self.users[display_name]}"
            
        self.active_websockets[websocket] = display_name
        await websocket.send_json({
            "user": "server", 
            "message": f"[*] Welcome to the server {display_name} ({websocket.client.host}:{websocket.client.port})!",
            "active_users": list(self.active_websockets.values())
        })
        await self.broadcast("server", f"[*] {display_name} ({websocket.client.host}:{websocket.client.port}) has joined the chat!", exclude={websocket})
    
    def get_display_name(self, websocket):
        return self.active_websockets.get(websocket)
    
    async def remove_websocket(self, websocket: WebSocket):
        display_name: str = self.active_websockets.get(websocket)
        del self.active_websockets[websocket]
        await self.broadcast("server", f"[*] {display_name} has left the chat!", exclude={websocket})
    
    async def broadcast(self, user:str, message: str, exclude: set[WebSocket] = set()):
        for websocket in self.active_websockets:
            if(websocket not in exclude):
                await websocket.send_json({"user": user, "message": message})


## settings related functions
def get_default_settings() -> dict:
    """
    Returns a dict containing default settings.
    """
    
    return {
        "host": "0.0.0.0",
        "port": 9900,
        "passwords": ["1234", "4321"],
    }


def set_settings(settings: dict) -> None:
    """
    'settings' is a dict containing the settings to be saved.
    Saves the given 'settings' to file named 'server_settings.json'
    """

    with open("server_settings.json", "w") as f:
        json.dump(settings, f)
    print("[*] Default settings written to server_settings.json")


def read_settings() -> dict:
    """
    Reads the settings from a file named 'server_settings.json' and returns it as a dict.
    If the file does not exist, creates the file with default settings with the same name and returns the default settings.
    """
    
    settings: dict = {}
    try:
        with open("server_settings.json", "r") as f:
            settings = json.load(f)
    except FileNotFoundError:
        settings = get_default_settings()
        set_settings(settings)
        
    return settings

