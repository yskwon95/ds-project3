from flask import Blueprint, render_template, request
from my_app.utils import main_funcs
from my_app import db
from my_app.models.user_model import User
from my_app.models.tweet_model import Tweet
from my_app.services.tweepy_api import get_user,get_tweets
from my_app.utils.main_funcs import predict_text

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/compare', methods=["GET", "POST"])
def compare_index():
    """
    users 에 유저들을 담아 넘겨주세요. 각 유저 항목은 다음과 같은 딕셔너리
    형태로 넘겨주셔야 합니다.
     -  {
            "id" : "유저의 아이디 값이 담긴 숫자",
            "username" : "유저의 유저이름 (username) 이 담긴 문자열"
        }
    prediction 은 다음과 같은 딕셔너리 형태로 넘겨주셔야 합니다:
     -   {
             "result" : "예측 결과를 담은 문자열입니다",
             "compare_text" : "사용자가 넘겨준 비교 문장을 담은 문자열입니다"
         }
    """

    users = User.query.all()
    prediction = None
    
    if request.method == "POST":
        ## user1, user2
        user_1_name = request.form['user_1']

        user_1 = User.query.filter(User.id == user_1_name).first()

        ## user_list for func
        user_list = [user_1]

        ## text to predict
        compare_text = request.form['compare_text']

        ## prediction
        prediction = {"result" : predict_text(user_list,compare_text),
                      "compare_text" : compare_text}

        return render_template('compare_user.html', users=users, prediction=prediction)
    return render_template('compare_user.html', users=users),200

@bp.route('/user')
def user_index():
    """
    user_list 에 유저들을 담아 템플렛 파일에 넘겨주세요
    """

    msg_code = request.args.get('msg_code', None)
    
    alert_msg = main_funcs.msg_processor(msg_code) if msg_code is not None else None

    user_list = User.query.all()

    return render_template('user.html', alert_msg=alert_msg, user_list=user_list)