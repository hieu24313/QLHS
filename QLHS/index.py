from flask import render_template, request, redirect, session, jsonify
from QLHS import dao, app, login, admin,  controllers
from flask_login import login_user, logout_user, current_user, login_required
from QLHS.decorators import annonymous_user
import cloudinary.uploader
import json
import datetime

app.add_url_rule("/", 'index', controllers.index)
app.add_url_rule('/logout', 'logout', controllers.logout_my_user)
app.add_url_rule('/login', 'login-user', controllers.login_my_user, methods=['get', 'post'])
app.add_url_rule('/login-admin', 'login-admin', controllers.admin_login, methods=['post'])
app.add_url_rule('/NV', 'ql_hs', controllers.ql_hs)
app.add_url_rule('/GV', 'ql_diem', controllers.ql_diem)
app.add_url_rule('/GV/bangDiem', 'bangDiem', controllers.bangDiem)
app.add_url_rule('/GV/nhapDiem', 'nhapDiem', controllers.nhapDiem)
app.add_url_rule('/GV/capNhatDiem', 'capNhatDiem', controllers.capNhatDiem)
app.add_url_rule('/NV/tiepNhanHS', 'tiepNhanHS', controllers.tiepNhanHS, methods=['get', 'post'])
app.add_url_rule('/NV/themHS', 'themHS', controllers.themHS, methods=['get', 'post'])
app.add_url_rule('/NV/capNhatLop', 'capNhatLop', controllers.capNhatLop, methods=['post', 'get', 'delete'])


@login.user_loader
def load_user(user_id):
    return dao.get_user_by_id(user_id)


if __name__ == '__main__':
    app.run(debug=True)