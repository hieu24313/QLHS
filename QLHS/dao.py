import json
from sqlalchemy import func
from QLHS import db
from QLHS.model import *


def auth_user(username, password):
    return User.query.filter(User.username.__eq__(username.strip()),
                             User.password.__eq__(password)).first()


def get_user_by_id(user_id):
    return User.query.get(user_id)


def timlopchuaduhs():
    d = dem_so_hs()
    with open('data/quydinh.json', 'r') as f:
        quydinh = json.load(f)
    sl = int(quydinh["siso"])
    for a in d:
        i = 0
        if d[i][1] <= sl:
            return d[i]
        i = i + 1


def add_hocsinh(hocsinh_id, lop_id):
    d = danhsachlop(hocsinh_id=hocsinh_id, lop_id=lop_id)
    db.session.add(d)
    db.session.commit()


def dem_so_hs():
    query = db.session.query(lop.id, func.count(danhsachlop.lop_id)) \
        .join(danhsachlop, danhsachlop.lop_id.__eq__(lop.id), isouter=True).group_by(lop.id)
    return query.all()


def load_mon():
    return mon.query.all()


def tiepnhanhs(name, ngaysinh, diachi, gioitinh, sodt=None, email=None):
    lop_id = timlopchuaduhs()
    u = hocsinh(name=name, ngaysinh=ngaysinh, diachi=diachi, gioitinh=gioitinh, sodt=sodt, email=email)
    db.session.add(u)
    db.session.commit()
    u.id
    if lop_id:
        add_hocsinh(u.id, lop_id=lop_id[0])


def load_lop():
    query = lop.query
    return query.all()


def get_hocky_id(ten_hoc_ky, nam_hoc):
    query = db.session.query(hocky.id, hocky.tenhocky, hocky.namhoc)
    nam_hoc = nam_hoc[0:4]
    if ten_hoc_ky:
        query = query.filter(hocky.tenhocky.__eq__(ten_hoc_ky))
    if nam_hoc:
        query = query.filter(hocky.namhoc.__eq__(nam_hoc))
    a = query.all()
    return a[0][1]


def hocsinh_lop(khoi, ten_lop, hoc_ky_id):
    query = db.session.query(hocsinh.id, hocsinh.name, hocsinh.diachi, hocsinh.ngaysinh, hocsinh.gioitinh,
                             hocsinh.email) \
        .join(danhsachlop, danhsachlop.hocsinh_id.__eq__(hocsinh.id)) \
        .join(lop, lop.id.__eq__(danhsachlop.lop_id)).order_by(hocsinh.name)
    if khoi:
        query = query.filter(lop.khoi.__eq__(khoi))
    if ten_lop:
        query = query.filter(lop.tenlop.__eq__(ten_lop))
    if hoc_ky_id:
        query = query.filter(lop.hocky_id.__eq__(hoc_ky_id))
    return query.all()


