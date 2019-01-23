from Ung_dung import app
from flask import  redirect, render_template , session, request, Markup
from datetime import datetime

from sqlalchemy.orm import sessionmaker
from sqlalchemy import exc
from sqlalchemy import update

from Ung_dung.Xu_ly.Khach_tham_quan.Xu_ly_3L import *

#**********import form**************
    # import ckeditor
from Ung_dung.Xu_ly.Khach_tham_quan.Xu_ly_Form import*
from flask_ckeditor import CKEditor

#************khởi tạo session_1*****
Base.metadata.bind= engine
DBSession= sessionmaker(bind=engine)
session_1=DBSession()

@app.route('/', methods=['GET','POST'])
def index():
#**************Khởi động dữ liệu *********
    Danh_sach_SP_chon =[]
    Danh_sach_san_pham = Doc_danh_sach_SP()
    Da_dang_nhap = False

#**************Menu khach hang************

    Chuoi_HTML_Khach_hang = ""
    Chuoi_QL_Dang_nhap =""
    if session.get('Khach_hang_dang_nhap'):
        print('get sessions')
        Khach_hang_dang_nhap = session['Khach_hang_dang_nhap']
        Chuoi_HTML_Khach_hang= Tao_chuoi_HTML_Khach_hang(Khach_hang_dang_nhap)

        #*xử lý button"thêm vào giỏ hàng
        Da_dang_nhap=True
    else:
        Chuoi_QL_Dang_nhap = '''
        <a href="/Dang_nhap_khach_hang">
        <button class="btn button3" role="button">Đăng nhập</button></a>
        '''


#*************Khởi tạo giỏ hàng***********
    if request.method == 'POST':
        print("đã nhận post")
        if request.form.get('Th_Ma_so')!=None:
         #Truy vấn session['Gio_hang] khi khách chọn sản phẩm tiếp theo
                if session.get('Gio_hang'):
                       Danh_sach_SP_chon = session['Gio_hang']['Gio_hang']
                ma_so=request.form.get('Th_Ma_so')
                so_luong = request.form.get('Th_So_luong')

                #********xử lý update số lượng khi khách hàng chọn lại sản phẩm đã có trong giỏ hàng*******
                #Lưu ý : đang xử lý với 1 SP thông  qua mã số
                #Check đã có tivi trong giõ hàng chưa :
                # =>tra cứu mã số đang xử lý có trong Danh_sach_SP_chon(Lay_chi_tiet_SP không rỗng)
                # => San phẩm đã có trong giõ hàng 
                if Lay_chi_tiet_SP(Danh_sach_SP_chon,ma_so)!=None:
                    SP_chon_cu = Lay_chi_tiet_SP(Danh_sach_SP_chon,ma_so)
                        # Lấy số lượng đã có trong giỏ hàng bằng so_luong_cu
                    so_luong_cu =SP_chon_cu["So_luong"]
                        # lưu ý so_luong mới được lấy khi người dùng click chọn lại sản phẩm
                        # bằng hàm SP_chon["So_luong"] = so_luong bên dưới
                        # update lại số lượng mới
                    print ("số lượng cũ",so_luong_cu)
                    so_luong= int(so_luong_cu) + int(so_luong)
                        #so_luong đã dược update phải remove Tivi_cu 
                        # để phiên update sau so_luong nay thành so_luong cũ 
                        #Lưu ý: SP_chon không bị mất khỏi giỏ hàng sau khi remove vì
                        #hàm Danh_sach_SP_chon.append(SP_chon) bên dưới đã update lại SP
                    Danh_sach_SP_chon.remove(SP_chon_cu)

                # setup so_luong
                SP_chon = Lay_chi_tiet_SP(Danh_sach_san_pham,ma_so)
                SP_chon["So_luong"] = so_luong
                Danh_sach_SP_chon.append(SP_chon)
                print("Danh sách_sản phẩm_chọn", Danh_sach_SP_chon)
                session['Gio_hang']={'Gio_hang':Danh_sach_SP_chon}

    #***************cập nhật giỏ hàng *************
    if request.form.get('Th_Ma_so_1')!=None:
         #Truy vấn session['Gio_hang] khi khách chọn sản phẩm tiếp theo
        Danh_sach_SP_chon_update=[]

        # truyền dữ liệu vào Danh_sach_SP_chon_update để hiện thị giỏ hàng
        if session.get('Gio_hang'):
            Danh_sach_SP_chon_update = session['Gio_hang']['Gio_hang']

        ma_so_1=request.form.get('Th_Ma_so_1')
        print("mã số 1",ma_so_1)
        so_luong_1 = int(request.form.get('Th_So_luong_1'))
        SP_chon = Lay_chi_tiet_SP(Danh_sach_SP_chon_update,ma_so_1)
            
            # trường hợp số lượng =0 và sp_chon vẫn còn => tiến hành xóa sp
        if SP_chon !=None:
            Danh_sach_SP_chon_update.remove(SP_chon)
        if so_luong_1 >0 and SP_chon!=None:
            #cập nhật số lượng
            SP_chon['So_luong'] =so_luong_1
            Danh_sach_SP_chon_update.append(SP_chon)
        session['Gio_hang']={'Gio_hang':Danh_sach_SP_chon_update}
        if session.get('Gio_hang'):
            Danh_sach_SP_chon = session['Gio_hang']['Gio_hang']
    if session.get('Gio_hang'):
        Danh_sach_SP_chon = session['Gio_hang']['Gio_hang']

    #****************kết xuất dữ liệu****************
    chuoi_HTML_gio_hang = Tao_chuoi_HTML_gio_hang(Danh_sach_SP_chon)
    chuoi_the_hien=Tao_chuoi_HTML_Danh_sach_SP(Danh_sach_san_pham)
    chuoi_modal = Tao_chuoi_HTML_Modal(Danh_sach_san_pham,Da_dang_nhap)
    Khung =render_template("khach_hang/MH_Khach_hang.html",
        Chuoi_HTML_Khach_hang= Chuoi_HTML_Khach_hang,
        Chuoi_QL_Dang_nhap=Markup(Chuoi_QL_Dang_nhap),
        chuoi_HTML_gio_hang=chuoi_HTML_gio_hang,
        chuoi_the_hien=chuoi_the_hien,chuoi_modal=chuoi_modal)
    return Khung

@app.route('/Dang_ky', methods=['GET','POST'])
def Dang_ky():
    Chuoi_ket_qua=""
    form = Form_Khach_hang()
    if form.validate_on_submit():
        ma_khach_hang=request.form['Th_Ma_so']
        ten_khach_hang = request.form['Th_Ho_ten']
        phai=request.form['Th_Phai']
        ngay_sinh = request.form['Th_Ngay_sinh']
        dia_chi = request.form['Th_Dia_chi']
        dien_thoai=request.form['Th_Dien_thoai']
        email = request.form['Th_Email']
        mat_khau = request.form['Th_Mat_khau']
        
        kh= KhachHang(ma_khach_hang=ma_khach_hang, ten_khach_hang=ten_khach_hang, phai=phai, ngay_sinh=ngay_sinh,
                        dia_chi=dia_chi, dien_thoai=dien_thoai,email=email,matkhau=mat_khau)
        print(kh)
        session_1.add(kh)
        try:
            session_1.commit()
            Chuoi_ket_qua = "Đã tạo tài khoản thành công"

        except exc.SQLAlchemyError: 
            print(exc.SQLAlchemyError)
            Chuoi_ket_qua= "Tên đăng nhập này đã có, Vui lòng tên đăng nhập khác"
        
    return render_template('khach_hang/MH_Dang_ky.html',form=form, Chuoi_ket_qua=Markup(Chuoi_ket_qua))

@app.route("/Dang_nhap_khach_hang", methods=['GET','POST'])
def Dang_nhap():
#*****Khởi động dữ liệu nguồn/nội bộ*******
    if session.get('Khach_hang_dang_nhap'):
        return redirect(url_for('index'))
    Danh_sach_khach_hang=Doc_danh_sach_Khach_hang()
    Ten_dang_nhap=""
    Mat_khau=""
    Chuoi_Thong_bao= "Xin vui lòng Nhập Tên đăng nhập và Mật khẩu"
    if request.method=='POST':
        Ten_dang_nhap=request.form.get('Th_Ten_dang_nhap')
        Mat_khau= request.form.get('Th_Mat_khau')
        Khach_hang= Dang_nhap_Khach_hang(Danh_sach_khach_hang,Ten_dang_nhap,Mat_khau)
        print("khách hàng",Khach_hang)
        Hop_le=(Khach_hang!=None)
        if Hop_le:
            session['Khach_hang_dang_nhap']=Khach_hang
            return redirect(url_for('index'))
        else:
            Chuoi_Thong_bao="Đăng nhập không hợp lệ"
    Khung =render_template('khach_hang/MH_Dang_nhap.html',Chuoi_Thong_bao=Chuoi_Thong_bao)
    return Khung

@app.route("/Dang_xuat_khach_hang")
def Dang_xuat_khach_hang():
    session.pop('Khach_hang_dang_nhap',None)
    return redirect(url_for("index"))
@app.route('/Dat_hang',methods=['GET','POST'])
def Dat_hang():
    Chuoi_QL_Dang_nhap =""
    Chuoi_HTML_dat_hang =""
    Chuoi_Thong_bao =""
    if session.get('Khach_hang_dang_nhap'):
        if session.get('Gio_hang'):
            SP_dat_hang = session['Gio_hang']['Gio_hang']
            Khach_hang_dang_nhap = session['Khach_hang_dang_nhap']
            Chuoi_HTML_dat_hang= Tao_chuoi_HTML_Dat_hang(SP_dat_hang,Khach_hang_dang_nhap)
            Chuoi_HTML_Khach_hang= Tao_chuoi_HTML_Khach_hang(Khach_hang_dang_nhap)

            if request.method =='POST':
                for san_pham in SP_dat_hang:
                    so_luong_ton =san_pham['so_luong_ton']
                    so_luong = int(san_pham["So_luong"])
                    ma_san_pham =san_pham["ma_san_pham"]
                    so_luong_ton_update = so_luong_ton-so_luong
                    session_1.query(San_pham).filter(San_pham.ma_san_pham== ma_san_pham).update({"so_luong_ton":so_luong_ton_update})
                    session_1.commit()



                ngay_hd = datetime.now()
                ma_khach_hang = session['Khach_hang_dang_nhap']['ma_khach_hang']
                tri_gia = request.form.get('Th_Tong_tien')
                so_hoa_don =request.form.get('Th_So_hoa_don')
                print("trị giá",tri_gia)
                print("mã khách hàng",ma_khach_hang)
                print("số hóa đơn",so_hoa_don)
                print("ngày HD",ngay_hd)
                hd= HoaDon( ngay_hd=str(ngay_hd), ma_khach_hang=ma_khach_hang, tri_gia=tri_gia)
                session_1.add(hd)
                try:
                    session_1.commit()
                    return redirect(url_for('Ket_qua_dat_hang'))
                except exc.SQLAlchemyError: 
                    print("lỗi sql",exc.SQLAlchemyError)
                    pass
        else:
            return redirect(url_for("index"))
    else:
        Chuoi_QL_Dang_nhap = '''
        <a href="/Dang_nhap_khach_hang">
        <button class="btn button3" role="button">Đăng nhập</button></a>
        '''
    Khung= render_template("khach_hang/MH_Dat_hang.html",
                        Chuoi_HTML_Khach_hang= Chuoi_HTML_Khach_hang,
                        Chuoi_QL_Dang_nhap=Chuoi_QL_Dang_nhap,
                        Chuoi_HTML_dat_hang=Chuoi_HTML_dat_hang)
    return Khung

@app.route("/Dat_hang_ket_qua")
def Ket_qua_dat_hang():
    session.pop('Gio_hang',None)
    return "đà đặt thành công"
