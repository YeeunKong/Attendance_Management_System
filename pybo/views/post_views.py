from datetime import datetime
from flask import Blueprint, render_template, request, session, url_for, g
from werkzeug.utils import redirect
from pybo.forms import PostForm
from pybo.models import Post, User

from pybo import db

bp = Blueprint('post', __name__, url_prefix='/post')


@bp.route('/list/')
def _list():
    post_list = Post.query.order_by(Post.create_date.desc())
    return render_template('post_list.html', post_list=post_list)


@bp.route('/view/<int:id>/')
def view(id):
    post = Post.query.get_or_404(id)
    return render_template('post_view.html', post=post)


@bp.route('/write/', methods=('GET', 'POST'))
def write():
    form = PostForm()
    user_id = session.get('user_id')
    current_user = User.query.filter_by(id=user_id).first() #현재 로그인한 유저

    # 작성한 post DB에 저장
    if request.method == 'POST':
        post = Post(post_id = 0, writer=current_user.username, title=form.title.data, 
        content=form.content.data, create_date=datetime.now())
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('post._list'))
    return render_template('post_write.html', form=form)

