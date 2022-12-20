from flask import render_template, request, redirect, session
from QLHS import dao, app, login, admin
from flask_login import login_user, logout_user, current_user, login_required
from QLHS.decorators import annonymous_user
import json
import datetime


def index():
    return render_template('index.html')


def logout_my_user():
    logout_user()
    return redirect('/login')


@annonymous_user
def login_my_user():
        if request.method.__eq__('POST'):
            username = request.form['username']
            password = request.form['password']
            user = dao.auth_user(username=username, password=password)
            if user:
                login_user(user=user)
                n = request.args.get('next')
                return redirect(n if n else '/')
        return render_template('login.html')


def themHS():
    msgbox = ''
    if request.method.__eq__('POST'):
        s = request.form.get('birthday', False)
        a = int(s[0:4])
        with open('data/quydinh.json', 'r') as f:
            quydinh = json.load(f)
        b = int(quydinh["tuoimin"])
        c = int(quydinh["tuoimax"])
        year = datetime.datetime.now()
        year = year.year
        a = int(year - a)
        if a < b or a > c:
            msgbox = 'Tuổi không hợp lệ'
            return render_template('NV/themHS.html', msgbox=msgbox, b=b, c=c)
        dao.tiepnhanhs(name=request.form['username'], ngaysinh=request.form.get('birthday', False),
                       diachi=request.form['address']
                       , gioitinh=request.form['sex'], sodt=request.form['phone'], email=request.form['email'])
        return render_template('NV/themHS.html')
    return render_template('NV/themHS.html')


def admin_login():
    username = request.form.get('username', False)
    password = request.form.get('password', False)
    user = dao.auth_user(username=username, password=password)
    if user:
        login_user(user=user)

    return redirect('/admin')


def ql_hs():
    return render_template('NV.html')


def ql_diem():
    return render_template('GV.html')


def bangDiem():
    load_mon = dao.load_mon()
    return render_template('GV/bangDiem.html', load_mon=load_mon)


def capNhatLop():
    errmsg = ''
    lop = dao.load_lop()
    if request.method.__eq__('POST'):
        t = request.form.get('date')
        nam_hoc = t[0:4]
        khoi = request.form.get('khoi')
        ten_lop = request.form.get('lop')
        hoc_ky = request.form.get('hocky')
        try:
            hocky_id = dao.get_hocky_id(ten_hoc_ky=hoc_ky, nam_hoc=nam_hoc)
            load_hocsinh = dao.hocsinh_lop(khoi=khoi, ten_lop=ten_lop, hoc_ky_id=hocky_id)
            return render_template('/NV/capNhatLop.html', lop=lop, load_hocsinh=load_hocsinh)
        except:
            errmsg = 'Có lỗi xảy ra hoặc không có dữ liệu!'
    lop = dao.load_lop()
    return render_template('/NV/capNhatLop.html', lop=lop, errmsg=errmsg)


def nhapDiem():
    return render_template('GV/nhapDiem.html')


def capNhatDiem():
    return render_template('/GV/capNhatDiem.html')


def tiepNhanHS():
    msgbox = ''
    if request.method.__eq__('POST'):
        s = request.form.get('birthday', False)
        a = int(s[0:4])
        with open('data/quydinh.json', 'r') as f:
            quydinh = json.load(f)
        b = int(quydinh["tuoimin"])
        c = int(quydinh["tuoimax"])
        year = datetime.datetime.now()
        year = year.year
        a = int(year - a)
        if a < b or a > c:
            msgbox = 'Tuổi không hợp lệ'
            return render_template('NV/tiepNhanHS.html', msgbox=msgbox, b=b, c=c)
        dao.tiepnhanhs(name=request.form['username'], ngaysinh=request.form.get('birthday', False), diachi=request.form['address']
                ,gioitinh=request.form['sex'], sodt=request.form['phone'], email=request.form['email'])
        return render_template('NV/tiepNhanHS.html')
    return render_template('NV/tiepNhanHS.html')