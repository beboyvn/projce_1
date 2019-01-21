from flask import Flask ,flash, redirect, render_template, request, session, abort, url_for, Markup
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_login import UserMixin, LoginManager, current_user, login_user, logout_user
from flask_admin.contrib import sqlamodel
from Xu_ly.Xu_ly_Model import*
from sqlalchemy.orm import sessionmaker
from sqlalchemy import exc
from sqlalchemy.orm import configure_mappers
from flask_admin import BaseView, expose
import os
import os.path as op
from flask_admin.contrib import fileadmin

configure_mappers()
Base.metadata.bind = engine
DBSession= sessionmaker(bind=engine)
session = DBSession()

app = Flask(__name__, static_url_path="", static_folder = "Media", template_folder='Giao_dien')
app.secret_key = "123"
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite://Ung_dung/Du_lieu/ql_Shop_my_Pham.db?check_same_thread=False'

admin = Admin(app,
            index_view=AdminIndexView(
                name='shop mỹ phẩm', 
                url='/quan_tri/'
                ),
            template_mode='bootstrap3'
            )
           

login = LoginManager(app)

@login.user_loader
def load_user(id):
    quan_tri = session.query(NguoiDung).filter(NguoiDung.ma_nguoi_dung==id).first()
    return quan_tri

class MyModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated

class LogoutView(BaseView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect(url_for('admin.login'))



#Upload hình
path= op.join(op.dirname(__file__),'Media/files')
try:
    os.mkdir(path)
except OSError:
    pass
admin.add_view(fileadmin.FileAdmin(path,'/Media/files/',name='Upload hình'))
#--------------------------

#Thêm administrative view ở đây
class san_pham_View(MyModelView):
    column_display_pk= True
    can_create= True
    can_delete= False
    can_export =True
    # -------------xử lý Markup field hyperlink -------------
    #_user_fromatter là phương thức build-in trong flask_admin lấy 4 đối số là view,context,model,name
    def _user_formatter(view,context,model,name):
        markupstring = model.mo_ta_chi_tiet
        return Markup(markupstring)
    column_formatters = {
        'mo_ta_chi_tiet': _user_formatter
    }
    #--------------hết phần xử lý markup-----------------

    column_list=('ma_san_pham','ten_san_pham','ma_loai','noi_dung_tom_tat','mo_ta_chi_tiet',
    'don_gia','DVT','tinh_trang','hinh','san_pham_moi')
    form_columns =('ma_san_pham','ten_san_pham','ma_loai','noi_dung_tom_tat','mo_ta_chi_tiet',
    'don_gia','DVT','tinh_trang','hinh','san_pham_moi')
    #column_lables = dict(Ma_so="Mã số",Ten='Tên')
    #inline_models = [(Giang_day,dict(form_columns=['id','Ma_so_Giao_vien'])),(Hoc_sinh)]
    # tìm khóa ngoại


admin.add_view(san_pham_View(San_pham,session,"Sản phẩm"))
class MyView(BaseView):
    @expose('/')
    def index(self):
        return self.render('admin/myview.html')

admin.add_view(MyView(name="View của tôi",menu_icon_type='glyph'))
admin.add_view(LogoutView(name="Đăng xuất",menu_icon_type='glyph'))

@app.route("/quan_tri/login",endpoint="admin.login",methods=['GET','POST'])
def Dang_nhap():
    Chuoi_Thong_bao =""
    if request.method == "POST":
        Ten_dang_nhap = request.form.get('Th_Ten_dang_nhap')
        Mat_khau = request.form.get('Th_Mat_khau')
        print("mật khẩu",Mat_khau)
        quan_tri_User = session.query(NguoiDung).filter(NguoiDung.ten_dang_nhap==Ten_dang_nhap).first()
        quan_tri_Password= session.query(NguoiDung).filter(NguoiDung.mat_khau == Mat_khau).first()
        
        Hop_le_User= quan_tri_User
        Hop_le_Password= quan_tri_Password
        if Hop_le_User and Hop_le_Password:
            # tạo session login 
            login_user(quan_tri_User)
            return redirect(url_for('admin.index'))
        else:
            Chuoi_Thong_bao= "Đăng nhập không hợp lệ"

    Khung = render_template('Quan_tri/MH_Quan_tri.html', Chuoi_Thong_bao=Chuoi_Thong_bao)
    return Khung

if __name__ == "__main__":
    app.debug=True
    app.run()