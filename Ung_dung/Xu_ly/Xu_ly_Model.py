from sqlalchemy.dialects.mysql import INTEGER, VARCHAR

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import(Column, Float,ForeignKey,Integer, String,Date, Text, Index,
                        create_engine)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from flask_login import UserMixin, LoginManager, current_user, login_user

engine= create_engine('sqlite:///Ung_dung/Du_lieu/ql_Shop_my_Pham.db?check_same_thread=False')
Base= declarative_base()
metadata = Base.metadata

class San_pham(Base):
    __tablename__ = 'san_pham'
    ma_san_pham = Column(String(50),nullable=False,unique=True ,primary_key=True)
    ten_san_pham = Column(String(100),nullable=False)
    ma_loai= Column(Integer,nullable=False)
    noi_dung_tom_tat = Column(String(255), nullable= False)
    #mo_ta_chi_tiet nullable =True
    mo_ta_chi_tiet=Column(String(1000))
    don_gia= Column(Integer,nullable=False)
    DVT= Column(String(20),nullable=False)
    tinh_trang= Column(String(100), nullable= False, default='Đang demo, chưa có hàng')
    hinh = Column(String(200))
    so_luong_ton= Column(Integer, nullable=True)
    don_gia_nhap = Column(Integer,nullable=True)
    san_pham_moi= Column(INTEGER(4),nullable=False,default=0)

class CtHoaDon(Base):
    __tablename__ = 'ct_hoa_don'

    so_hoa_don = Column(String(5 ), nullable=False)
    id_san_pham = Column(String(6 ), nullable=False)
    so_luong = Column(INTEGER(11), nullable=False)
    don_gia = Column(INTEGER(11), nullable=False)
    stt = Column(INTEGER(11), primary_key=True)


class HoaDon(Base):
    __tablename__ = 'hoa_don'

    so_hoa_don = Column(Integer, autoincrement=True , primary_key=True)
    ngay_hd = Column(String(100), nullable=False)
    ma_khach_hang = Column(String(100 ), nullable=False)
    tri_gia = Column(Integer,nullable=False)


class KhachHang(Base):
    __tablename__ = 'khach_hang'

    ma_khach_hang = Column(String(200), primary_key=True)
    ten_khach_hang = Column(String(100 ), nullable=False)
    phai = Column( INTEGER(1), nullable=False)
    ngay_sinh = Column(String(200), nullable=False)
    dia_chi = Column(String(200 ), nullable=False)
    dien_thoai = Column(String(20 ), nullable=False)
    email = Column(String(100 ), nullable=False)
    matkhau = Column(String(100 ), nullable=False)


class LoaiNguoiDung(Base):
    __tablename__ = 'loai_nguoi_dung'

    ma_loai_nguoi_dung = Column( String(3), primary_key=True)
    ten_loai_nguoi_dung = Column(VARCHAR(100), nullable=False)


class LoaiSanPham(Base):
    __tablename__ = 'loai_san_pham'

    ma_loai = Column(INTEGER(11), primary_key=True)
    ten_loai = Column(String(50 ), nullable=False)
    url_ten_loai = Column(String(200 ), nullable=False)
    mo_ta = Column(Text(20))
    ma_loai_cha = Column(INTEGER(11), nullable=False)
    hinh = Column(String(200 ), nullable=False)

# bổ sung thêm subclass usermixin để class có cac thuộc tính is_active, etc sử dụng cho flask_login
class NguoiDung(Base,UserMixin):
    __tablename__ = 'nguoi_dung'
    ma_nguoi_dung = Column(INTEGER(11), primary_key=True)
    # phai them bien id de cap cho phuong thuc usermixin thực hiện chức năng login()
    id= ma_nguoi_dung
    ma_loai_nguoi_dung = Column( String(3), nullable=False, index=True)
    ho_ten = Column(VARCHAR(100), nullable=False)
    ten_dang_nhap = Column(VARCHAR(100), nullable=False)
    mat_khau = Column(VARCHAR(100), nullable=False)
    email = Column(VARCHAR(100))
    ngay_dang_ky = Column(Date)
    ngay_dang_nhap_cuoi = Column(Date)
    active = Column( String(4), nullable=False)


class NhaCungCap(Base):
    __tablename__ = 'nha_cung_cap'

    ma_nha_cung_cap = Column(INTEGER(11), primary_key=True)
    ten_nha_cung_cap = Column(String(100 ), nullable=False)
    ten_nha_cung_cap_url = Column(String(200 ), nullable=False)
    dia_chi = Column(String(200 ), nullable=False)
    dien_thoai = Column(String(20 ), nullable=False)
    email = Column(String(100 ), nullable=False)
    fax = Column(String(20 ), nullable=False)
    nha_cung_cap_hang_dau = Column( String(1), nullable=False)
    hinh_nha_cung_cap = Column(String(100 ), nullable=False)

class SanPhamKhuyenMai(Base):
    __tablename__ = 'san_pham_khuyen_mai'

    ma_san_pham = Column(INTEGER(11), primary_key=True, nullable=False)
    ma_loai = Column(INTEGER(11), nullable=False)
    ma_loai_cha = Column(INTEGER(11), nullable=False)
    don_gia_khuyen_mai = Column(Float(asdecimal=True), nullable=False)
    noi_dung_khuyen_mai = Column(Text(20), nullable=False)
    dot_khuyen_mai = Column(INTEGER(11), primary_key=True, nullable=False)
    tu_ngay = Column(Date, primary_key=True, nullable=False)
    den_ngay = Column(Date, primary_key=True, nullable=False)
    hinh_khuyen_mai = Column(String(100 ), nullable=False)


class ThuongHieu(Base):
    __tablename__ = 'thuong_hieu'
    __table_args__ = (
        Index('ma_thuong_hieu', 'ten_thuong_hieu', 'ten_thuong_hieu_url', 'dia_chi', 'dien_thoai', 'email', 'fax', 'thuong_hieu_hang_dau', 'hinh_thuong_hieu', unique=True),
    )

    ma_thuong_hieu = Column(INTEGER(11), primary_key=True)
    ten_thuong_hieu = Column(String(100 ), nullable=False)
    ten_thuong_hieu_url = Column(String(200 ), nullable=False)
    dia_chi = Column(String(200 ), nullable=False)
    dien_thoai = Column(String(20 ), nullable=False)
    email = Column(String(100 ), nullable=False)
    fax = Column(String(20 ), nullable=False)
    thuong_hieu_hang_dau = Column( String(1), nullable=False)
    hinh_thuong_hieu = Column(String(100 ), nullable=False)

if __name__=="__main__":
    Base.metadata.create_all(engine)
    print("đã tạo csdl")
