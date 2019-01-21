from flask_wtf import FlaskForm

from wtforms import TextField, IntegerField, TextAreaField, SubmitField,\
                    RadioField, SelectField, PasswordField, StringField
from wtforms.fields.html5 import DateField, TelField, EmailField

from wtforms.widgets import PasswordInput
from wtforms import validators , validators

from Ung_dung.Xu_ly.Xu_ly_Model import *

from flask_ckeditor import CKEditorField

class Form_Khach_hang(FlaskForm):
    Th_Ma_so = TextField("Tên đăng nhập",[validators.Required("Vui lòng nhập mã số")])
    Th_Ho_ten =TextField("Họ tên",[validators.Required("Vui lòng nhập họ tên.")])
    #coerce=int để form trả về giá trị int vì form trả vể giá trị string
    Th_Phai = SelectField(u'Phái',choices=[(0,'Nam'),(1,'Nữ')],coerce=int)

    Th_Ngay_sinh= DateField("Ngày sinh")
    Th_Dien_thoai= TelField("Số điện thoại",[validators.Required("Vui lòng nhập số điện thoại")])
    Th_Email = EmailField("Địa chỉ Mail",[validators.DataRequired(),validators.Email()])
    Th_Dia_chi = TextField("Địa chỉ",[validators.Required("Vui lòng nhập địa chỉ")])
    Th_Mat_khau = PasswordField('Mật khẩu',[validators.InputRequired(),validators.EqualTo('Th_Mat_khau_xac_nhan',
    message="Mật khẩu phải trùng với mật khẩu xác nhận")])
    Th_Mat_khau_xac_nhan= PasswordField('Xác nhận mật khẩu')
    Th_Submit= SubmitField("Tạo tài khoản")
