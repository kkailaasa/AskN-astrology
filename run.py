import uvicorn
import os

if __name__ == "__main__":
    app_port = int(os.getenv("APP_PORT", 8000))
    uvicorn.run("app.main:app", host="0.0.0.0", port=app_port, reload=True)
