from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey, Enum, DATE
from sqlalchemy.orm import relationship, backref
from QLHS import db, app
from enum import Enum as UserEnum
from flask_login import UserMixin


class UserRole(UserEnum):
    ADMIN = 1
    GV = 2
    NV = 3


class BaseModel(db.Model):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)


class hocsinh(BaseModel):
    __tablename__ = 'hocsinh'

    name = Column(String(200), nullable=False)
    ngaysinh = Column(DATE, nullable=False)
    diachi = Column(String(200), nullable=False)
    gioitinh = Column(String(50), nullable=False)
    email = Column(String(200), nullable=True)
    sodt = Column(String(20), nullable=True)
    thuoclop = relationship('danhsachlop', backref='hocsinh', lazy=True)

    def __str__(self):
        return self.name


class hocky(BaseModel):
    __tablename__ = 'hocky'

    tenhocky = Column(String(100), nullable=False)
    namhoc = Column(Integer, nullable=False)
    lop = relationship('lop', backref='hocky', lazy=True)

    def __str__(self):
        return self.tenhocky


class User(BaseModel, UserMixin):  #Giao vien va nhan vien
    __tablename__ = 'user'

    name = Column(String(50), nullable=False)
    username = Column(String(50), unique=True)
    password = Column(String(50))
    active = Column(Boolean, default=True)
    user_role = Column(Enum(UserRole), default=UserRole.GV)
    gvcn = relationship('lop', backref='user', lazy=True)

    def __str__(self):
        return self.name


class lop(BaseModel):
    __tablename__ = 'lop'

    tenlop = Column(String(100), nullable=False)
    hocky_id = Column(Integer, ForeignKey(hocky.id), nullable=False)
    gvcn_id = Column(Integer, ForeignKey(User.id))
    khoi = Column(Integer, nullable=True)
    hocsinhtronglop = relationship('danhsachlop', backref='lop', lazy=True)

    def __str__(self):
        return self.tenlop


class danhsachlop(BaseModel):
    __tablename__ = 'danhsachlop'

    hocsinh_id = Column(Integer, ForeignKey(hocsinh.id), nullable=False)
    lop_id = Column(Integer, ForeignKey(lop.id), nullable=False)
    diemcualop = relationship('diem', backref='danhsachlop', lazy=True)


class mon(BaseModel):
    __tablename__ = 'mon'

    tenmon = Column(String(100), nullable=False)
    codiem = relationship('diem', backref='mon', lazy=True)

    def __str__(self):
        return self.tenmon


class loaidiem(BaseModel):
    __tablename__ = 'loaidiem'
    loai = Column(String(100), nullable=False)
    heso = Column(Integer, nullable=False)
    diem_loai = relationship('diem', backref='loaidiem', lazy=True)

    def __str__(self):
        return self.loai


class diem(BaseModel):
    __tablename__ = 'diem'

    sodiem = Column(Float, nullable=False)
    mon_id = Column(Integer, ForeignKey(mon.id), nullable=False)
    hocsinh_id = Column(Integer, ForeignKey(danhsachlop.id), nullable=False)
    loaidiem_id = Column(Integer, ForeignKey(loaidiem.id), nullable=False)

    def __str__(self):
        return self.sodiem


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        u = User(name='hieu', username='ADMIN', password='123',
                 user_role=UserRole.ADMIN
                 )

        u2 = User(name='hieu', username='GV', password='123',
                 user_role=UserRole.GV
                 )

        u3 = User(name='hieu', username='NV', password='123',
                 user_role=UserRole.NV
                 )

        db.session.add_all([u, u2, u3])
        db.session.commit()

