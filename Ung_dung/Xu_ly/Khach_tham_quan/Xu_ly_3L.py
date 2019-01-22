from flask import Markup, url_for
import sqlite3

from Ung_dung.Xu_ly.Xu_ly_Model import *
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# khởi tạo session 
Base.metadata.bind= engine
DBSession = sessionmaker(bind=engine)
session_1 = DBSession()

def Doc_danh_sach_SP():
    ds_San_pham_Lop_1 =None
    ds_San_pham =[]
    ds_San_pham_Lop_1 =session_1.query(San_pham).all()

    for san_pham in ds_San_pham_Lop_1:
        san_pham_Lop_1= {"ma_san_pham":san_pham.ma_san_pham,"ten_san_pham": san_pham.ten_san_pham,\
                            "ma_loai":san_pham.ma_loai ,"noi_dung_tom_tat":san_pham.noi_dung_tom_tat,\
                            "mo_ta_chi_tiet":san_pham.mo_ta_chi_tiet,"don_gia":san_pham.don_gia,\
                            "DVT":san_pham.DVT, "tinh_trang":san_pham.tinh_trang,"hinh":san_pham.hinh,\
                            "san_pham_moi":san_pham.san_pham_moi}
        ds_San_pham.append(san_pham_Lop_1)
    return ds_San_pham
def Doc_danh_sach_Khach_hang():
    ds_Khach_hang_Lop_1 =None
    ds_Khach_hang =[]
    ds_Khach_hang_Lop_1 =session_1.query(KhachHang).all()

    for khach_hang in ds_Khach_hang_Lop_1:
        khach_hang_Lop_1= {"ma_khach_hang":khach_hang.ma_khach_hang,"ten_khach_hang": khach_hang.ten_khach_hang,\
                            "phai":khach_hang.phai ,"ngay_sinh":khach_hang.ngay_sinh,\
                            "dia_chi":khach_hang.dia_chi,"dien_thoai":khach_hang.dien_thoai,\
                            "email":khach_hang.email, "matkhau":khach_hang.matkhau,}
        ds_Khach_hang.append(khach_hang_Lop_1)
    return ds_Khach_hang

def Tao_chuoi_HTML_Danh_sach_SP(Danh_sach_SP):
    Chuoi_HTML_Danh_sach= '''
    <div class="isotope" style="position: relative; height: 480px;" id="portfolio-wrap"> 
    '''
    for san_pham in Danh_sach_SP:
        Chuoi_Don_gia_Ban="Giá : {:,}".format(san_pham["don_gia"]).replace(",",".")    
        # <div class="hidden"> vì đang dùng boostrap3 tương đương với bootsrap4 là <div class="d-none">
        Chuoi_mo_ta_chi_tiet ='<div class="hidden" id="Noi_dung_chi_tiet_'+ str(san_pham["ma_san_pham"]) +'">'+ san_pham['mo_ta_chi_tiet'] +'</div>' if san_pham['mo_ta_chi_tiet']!=None else ""
        Chuoi_hinh ='''
        <div style="position: absolute; left: 0px; top: 0px; transform: translate3d(674px, 0px, 0px) 
        scale3d(1, 1, 1); width: 337px; opacity: 1;" class="portfolio-item one-four  design  isotope-item">
        <div class="portfolio-image"> <img src="'''+\
        url_for('static',filename='hinh/hinh_san_pham/'+san_pham["hinh"]) + ''' "alt="Portfolio 1"> </div>'''
        Chuoi_Overlay='''
         <div class="project-overlay">
          <div class="project-info">
            <div class="zoom-icon"></div>
            <h4 class="project-name" id="Ten_San_Pham_'''+ str(san_pham['ma_san_pham']) +'''">'''+san_pham['ten_san_pham']+ '''</h4>
            <h5 class="project-name" style="color:#cc99ff;" >'''+ san_pham['tinh_trang'] + ''' </h5>
            <h5 class="project-name" style="color:#ff66ff;" >'''+ Chuoi_Don_gia_Ban + ''' </h5>             
          </div>
          <button type="button" class="btn project-overlay" data-toggle="modal" data-target="#ID_'''+ str(san_pham['ma_san_pham']) +'''" ></button>
        </div>
        '''
        Chuoi_HTML_Danh_sach += Chuoi_hinh + Chuoi_Overlay +Chuoi_mo_ta_chi_tiet
        Chuoi_HTML_Danh_sach +="</div>"
    Danh_sach_san_pham = Danh_sach_SP
    Chuoi_HTML_Danh_sach+="</div>"
    return Markup(Chuoi_HTML_Danh_sach)
def Tao_chuoi_HTML_Modal(Danh_sach_SP,Da_dang_nhap):
    Chuoi_modal=""
    for san_pham in Danh_sach_SP:
        if Da_dang_nhap:
            Chuoi_form ='''
            <div>
                <form method="post" action="/">            
                    <input type="hidden" name="Th_Ma_so" value="'''+str(san_pham['ma_san_pham'])+'''"/>
                    <input type="number" name="Th_So_luong" value="1" min="1" max="10"/>
                    <button type="submit" class="btn button3"><p class="text-white">Thêm vào giỏ hàng</p></button>
                </form>
            </div>
            '''
        else:
             Chuoi_form='''
                <div>
                    <form method="post" action="/">            
                     <a href="/Dang_nhap_khach_hang"> <button type="button" class="btn button3"><p class="text-white">Thêm vào giỏ hàng</p></button></a>
                    </form>
                </div>
            '''
        Chuoi_mo_ta_chi_tiet ='<div>'+ str(san_pham['mo_ta_chi_tiet']) +'</div>' if san_pham['mo_ta_chi_tiet']!=None else ""
        Chuoi_modal +='''
        <div class="modal fade" id="ID_'''+ str(san_pham['ma_san_pham']) +'''"  tabindex="-1" role="dialog" aria-labelledby="exampleModalLabel" aria-hidden="true">
                <div class="modal-dialog" role="document">
                <div class="modal-content">
                    <div class="modal-header">
                       '''+ Chuoi_form +'''
                        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                        <span aria-hidden="true">&times;</span>
                        </button>
                    </div>
                    <div class="modal-body">
                        <h2 >''' +san_pham['ten_san_pham']+ '''</h2>
                        <img src="'''+ url_for('static',filename='hinh/hinh_san_pham/'+san_pham["hinh"]) + '''" >
                        '''+Chuoi_mo_ta_chi_tiet +'''
                        <div align="center" id="Chi_tiet_SP"></div>
                    </div>
                    <div class="modal-footer">

                    </div>
                </div>
                </div>
                </div>
        '''
    return Markup(Chuoi_modal)

def Lay_chi_tiet_SP(Danh_sach_san_pham,ma_so):
    Danh_sach = list(filter(lambda San_pham_chon: San_pham_chon['ma_san_pham']==ma_so,Danh_sach_san_pham))

    San_pham=Danh_sach[0] if len(Danh_sach)==1 else None

    return San_pham

def Tao_chuoi_HTML_gio_hang(Danh_sach_SP_chon):
    
    #Đây là phần bọc modal cho giỏ hàng
    Chuoi_HTML_Danh_sach = '''
    <div class="modal fade" id="gioHang" role="dialog" aria-labelledby="exampleModalLabel" aria-hidden="true">
      <div class="modal-dialog modal-dialog-cus" role="document">
        <div class="modal-content">
          
            <button type="button" class="close" data-dismiss="modal" aria-label="Close">
            <span aria-hidden="true">&times;</span>
            </button>  
    '''
    Chuoi_HTML_Danh_sach += '<div class="dropdown-item">'
    Chuoi_HTML_Danh_sach +='<div class="section-title h3" id="Portfolio" style="font-family:Dosis;"> &nbsp;&nbsp;&nbsp;Chi tiết giỏ hàng</div>'
    Chuoi_HTML_Danh_sach+='</div>'
    Chuoi_HTML_Danh_sach +='<div class="card" style="padding-bottom: 20px;">'
    for san_pham in Danh_sach_SP_chon:
        Chuoi_Don_gia_Ban="Đơn giá Bán {:,}".format(san_pham["don_gia"]).replace(",",".")    
        Chuoi_Hinh_nho='<img class="card-img-top"  style="width:60px;height:60px"  src="'+ \
                 url_for('static', filename ="hinh/hinh_san_pham/"+ san_pham["hinh"]) + '" />'
        
        Chuoi_Thong_tin='<div class="btn" style="text-align:left">' + \
                san_pham["ten_san_pham"] + "<br />" + Chuoi_Don_gia_Ban + "</div>"
        
        Chuoi_form =  '''<div ><form method="post" action="/">            
                <input type="hidden" name="Th_Ma_so_1" value="'''+san_pham["ma_san_pham"]+'''"/>
                <input type="number" name="Th_So_luong_1" value="'''+str(san_pham["So_luong"])+'''" min="0" max="10"/>
                <button class="btn button5" type="submit">Cập nhật</button>
                </form></div>'''
        
        Chuoi_HTML ='<div class="col-auto">' +  \
                Chuoi_Hinh_nho + Chuoi_Thong_tin + Chuoi_form+ '</div>' 
        Chuoi_HTML_Danh_sach +=Chuoi_HTML 
    Chuoi_Dat_hang = '''<div class="dropdown-item pull-right "><form method="post" action="/Dat_hang">  
                <button class="btn button4">Tiến hành đặt hàng</button>
                </form></div>'''
    Chuoi_HTML_Danh_sach +="</div>"
    
    Chuoi_HTML_Danh_sach += Chuoi_Dat_hang+'</div></div></div>'

    return Markup(Chuoi_HTML_Danh_sach)  

def Dang_nhap_Khach_hang(Danh_sach_Khach_hang, Ten_dang_nhap, Mat_khau):
    Danh_sach = list(filter(
        lambda Khach_hang: Khach_hang['ma_khach_hang'] == Ten_dang_nhap and Khach_hang["matkhau"] == Mat_khau
        , Danh_sach_Khach_hang))
    khach_hang = Danh_sach[0] if len(Danh_sach)==1 else None
    
    return khach_hang

def Tao_chuoi_HTML_Khach_hang(Khach_hang):    
    Chuoi_HTML_Khach_hang = ""
    #Chuoi_Hinh = '<img  style="width:60px;height:60px"  src="'+ \
    #             url_for('static', filename = 'hinh/NV_1.png') + '" />'
    Chuoi_Gio_hang ='''
           <li>
           <button class="btn button3" type="button" id="dropdownMenuButton" data-toggle="modal"  data-target="#gioHang">Giỏ hàng</button>
           </li>
    '''
    Chuoi_Thong_tin = '<a href="#" > Xin chào quý khách: ' + \
                 Khach_hang["ten_khach_hang"] + "</a>"    
    Chuoi_HTML_Khach_hang += Chuoi_Thong_tin + Chuoi_Gio_hang+ '<li><a href="/Dang_xuat_khach_hang"><button class="btn button5" type="button" >Đăng xuất</button></a></li>'    
    return Markup(Chuoi_HTML_Khach_hang)  

def Tao_chuoi_HTML_Dat_hang(Danh_sach_SP):
    Tong_so_tien =0
    Chuoi_HTML_Danh_sach='''
    <div class="container">
    <h2>ĐƠN HÀNG</h2>
    <div class="work_section">
      <div class="row">
        <div class="col-lg-6 col-sm-6 wow fadeInLeft delay-05s animated" style="visibility: visible; animation-name: fadeInLeft;">
    '''
    for san_pham in Danh_sach_SP:
        Thanh_tien = int(san_pham["So_luong"]) * int(san_pham["don_gia"])
        Tong_so_tien += Thanh_tien

        Chuoi_SP='<div class="service-list">'
        Chuoi_hinh = '<div class="service-list-col1"> <img style="width:60px; height:60px;" src="'+\
                    url_for('static',filename="hinh/hinh_san_pham/"+ san_pham["hinh"])+'"/> </div>'
        Chuoi_noi_dung='''
                <div class="service-list-col2">
                    <h3>'''+san_pham['ten_san_pham']+'''</h3>
                    <p>Số lượng: '''+ str(san_pham["So_luong"]) +'''</br>
                    '''
        Chuoi_Don_gia_Ban="Đơn giá Bán {:,}".format(san_pham["don_gia"]).replace(",",".")
        Chuoi_Thanh_tien = "Thành tiền:" +str(san_pham["So_luong"]) +"x" + \
                            "{:,}".format(san_pham["don_gia"]).replace(",",".") + " = " +\
                            "{:,}".format(Thanh_tien).replace(",",".")
        Chuoi_noi_dung+=''' 
                    '''+ Chuoi_Don_gia_Ban +'''</br>
                    '''+ Chuoi_Thanh_tien +'''    
                    </p>
                </div>
                '''
        Chuoi_SP+= Chuoi_hinh+Chuoi_noi_dung
        Chuoi_SP+= '</div>'
        Chuoi_HTML_Danh_sach+=Chuoi_SP

    Chuoi_Tong_tien="<br/>Tổng tiền {:,}".format(Tong_so_tien).replace(",",".")
    Chuoi_HTML_Danh_sach+='''

        <div class="work_bottom"> <span>'''+ Chuoi_Tong_tien +'''</span> <a href="#contact" class="contact_btn">Đặt hàng</a> </div>
        </div>
        <figure class="col-lg-6 col-sm-6  text-right wow fadeInUp delay-02s animated" style="visibility: visible; animation-name: fadeInUp;"> </figure>
      </div>
    </div>
    </div>
    '''
    return Markup(Chuoi_HTML_Danh_sach)