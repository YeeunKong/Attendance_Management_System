from flask import Blueprint, render_template
from pybo.models import User
from pybo import db
from facial_req import parallel_camera_work

bp = Blueprint('attend', __name__, url_prefix='/attend')

btn_pin = 15

is_cam_on = False

def check_attend(user):
    attend_user = User.query.filter_by(username=user).all()
    attend_user[0].attendance = "O"
    db.session.commit()


@bp.route('/')
def _attend(): 
    global is_cam_on
    # Cam이 꺼져있으면 프로세스 실행
    if not is_cam_on:
        parallel_camera_work()
        is_cam_on=True
    user_list = User.query.all()
    return render_template('attend.html', user_list=user_list)


@bp.route('/reset/')
def reset():
    user_list = User.query.all()
    for user in user_list:
        user.attendance = "X"
    db.session.commit()
    return render_template('attend.html', user_list=user_list)
