from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin

app=Flask(__name__,template_folder="Giao_dien",static_folder="Media")
app.secret_key="2018"

# import cac app 
import Ung_dung.app_khach_hang
import Ung_dung.app_admin
