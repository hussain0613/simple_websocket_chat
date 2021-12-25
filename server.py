from app import app

if __name__ == "__main__":
    import uvicorn
    from utils import read_settings
    settings: dict = read_settings()

    uvicorn.run("server:app", host = settings.get("host"), port = settings.get("port"), reload=True)

