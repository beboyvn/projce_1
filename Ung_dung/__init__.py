from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin

app=Flask(__name__,template_folder="Giao_dien",static_folder="Media")
app.secret_key="2018"

#**************cấu hình mail*************
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] =465
app.config['MAIL_USERNAME']= 'python244t7cn@gmail.com'
app.config['MAIL_PASSWORD']='Python244'
app.config['MAIL_USE_TLS']=False
app.config['MAIL_USE_SSL']=True

# import cac app 
import Ung_dung.app_khach_hang
import Ung_dung.app_admin
