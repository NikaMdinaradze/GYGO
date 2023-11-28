from fastapi import FastAPI
import models
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from database import engine
from routes import admin, user
from sqladmin import Admin
from admin_panel import authentication_backend, UserAdmin

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.mount("/uploads", StaticFiles(directory="uploads"), name="upload")
app.mount("/banners", StaticFiles(directory="banners"), name="banners")
app.mount("/tmp", StaticFiles(directory="tmp"), name="tmp")

models.Base.metadata.create_all(engine)


app.include_router(admin.router)
app.include_router(user.router)

admin = Admin(app=app, engine=engine, authentication_backend=authentication_backend)
admin.add_view(UserAdmin)

