from fastapi import FastAPI
import models
from fastapi.staticfiles import StaticFiles
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from database import engine
from routes import admin, user


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],  # You can restrict this to specific headers
)


app.mount("/uploads", StaticFiles(directory="uploads"), name="upload")
app.mount("/banners", StaticFiles(directory="banners"), name="banners")

models.Base.metadata.create_all(engine)



app.include_router(admin.router)
app.include_router(user.router)



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)