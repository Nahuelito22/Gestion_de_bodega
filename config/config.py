import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "claveporDefecto")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI", "sqlite:///bodega.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False