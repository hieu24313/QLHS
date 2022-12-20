from QLHS.model import *
from QLHS import db, app, dao
from flask_admin import Admin, BaseView, expose, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user, logout_user
from wtforms import TextAreaField
from wtforms.widgets import TextArea
from flask import request, redirect
import json


class AuthenticatedModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN


class RuleView(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN


class CKTextAreaWidget(TextArea):
    def __call__(self, field, **kwargs):
        if kwargs.get('class'):
            kwargs['class'] += ' ckeditor'
        else:
            kwargs.setdefault('class', 'ckeditor')
        return super(CKTextAreaWidget, self).__call__(field, **kwargs)


class CKTextAreaField(TextAreaField):
    widget = CKTextAreaWidget()


class AuthenticatedView(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated


class StatsView(RuleView):
    @expose('/')
    def index(self):
        return self.render('admin/stats.html')


class Rule(RuleView):
    @expose('/', methods=['get', 'post'])
    def quydinh(self):
        msgerr=''
        with open('data/quydinh.json', 'r') as f:
            quydinh = json.load(f)
        with open('data/quydinh.json', 'w') as f:
            if request.method.__eq__('POST'):
                a = request.form['tuoimin']
                b = request.form['tuoimax']
                if b < a:
                    msgerr = 'Tuổi tối thiểu không thể lớn hơn tuổi tối đa!'
                    f.write(json.dumps(quydinh))
                    return self.render('admin/quydinh.html', quydinh=quydinh, msgerr=msgerr)
                else:
                    quydinh["tuoimin"] = a
                    quydinh["tuoimax"] = b
                    quydinh["siso"] = request.form['siso']
                f.write(json.dumps(quydinh))
            else:
                f.write(json.dumps(quydinh))
        return self.render('admin/quydinh.html', quydinh=quydinh)


class Userview(AuthenticatedModelView):
    can_export = True
    can_view_details = True
    column_exclude_list = ['password']
    column_filters = ['name', 'user_role']
    form_excluded_columns = ['gvcn', 'active']
    column_labels = {
        'name': 'Tên người dùng',
        'username': 'Tên tài khoản',
        'active': 'Trạng thái',
        'user_role': 'Loại người dùng'
    }


class Quanlymon(AuthenticatedModelView):
    column_display_pk = True
    can_view_details = True
    form_excluded_columns = ['codiem']
    column_filters = ['id', 'tenmon']
    column_searchable_list = ['id', 'tenmon']
    column_labels = {
        'id': 'Mã môn',
        'tenmon': 'Tên môn học'
    }


class quanlylop(AuthenticatedModelView):
    column_display_pk = True
    can_view_details = True
    form_excluded_columns = ['hocsinhtronglop']
    column_labels = {
        'id': 'Mã lớp',
        'tenlop': 'Tên lớp',
        'user': 'Giáo viên chủ nhiệm',
        'hocky': 'Học Kỳ',
        'khoi': 'Khối'
    }


class MyAdminView(AdminIndexView):
    @expose('/')
    def index(self):
        return self.render('admin/index.html')


class LogoutView(AuthenticatedView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/admin')


class loai_diem(AuthenticatedModelView):
    can_view_details = True
    form_excluded_columns = ['diem_loai']
    column_labels = {
        'loai': 'Loại điểm',
        'heso': 'Hệ số'
    }


admin = Admin(app=app, name='Quản lý học sinh', template_mode='bootstrap4', index_view=MyAdminView())
admin.add_view(StatsView(name='Thông kê'))
admin.add_view(Quanlymon(mon, db.session, name='Quản lý môn học'))
admin.add_view(Userview(User, db.session, name='Quản lý giáo viên/nhân viên'))
admin.add_view(quanlylop(lop, db.session, name='Quản lý lớp'))
admin.add_view(Rule(name='Quy định'))
admin.add_view(loai_diem(loaidiem, db.session, name='Loại điểm'))
admin.add_view(LogoutView(name='Đăng xuất'))