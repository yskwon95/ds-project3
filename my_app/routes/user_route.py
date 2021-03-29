from flask import Blueprint, request, redirect, url_for, Response
from my_app.services import tweepy_api, embedding_api
from my_app.models import user_model, tweet_model
from my_app.services.tweepy_api import get_user,get_tweets
from my_app.services.embedding_api import get_embeddings
from my_app.models.user_model import User
from my_app.models.tweet_model import Tweet
from my_app import db


bp = Blueprint('user', __name__)


@bp.route('/user', methods=['POST'])
def add_user():
    """
    add_user 함수는 JSON 형식으로 전달되는 폼 데이터로 유저를 트위터에서 조회한 뒤에
    해당 유저와 해당 유저의 트윗들을 벡터화한 값을 데이터베이스에 저장합니다.
    요구사항:
      - HTTP Method: `POST`
      - Endpoint: `api/user`
      - 받는 JSON 데이터 형식 예시:
            ```json
            {
                "username":"업데이트할 유저의 username",
                "new_username":"새로 업데이트할 username"
            }
            ```
    상황별 요구사항:
      - 주어진 데이터에 `username` 키가 없는 경우:
        - 리턴값: "Needs username"
        - HTTP 상태코드: `400`
      - 주어진 데이터의 `username` 에 해당하는 유저가 트위터에 존재하지 않은 경우:
        - 리턴값: main_route.py 에 있는 user_index 함수로 리다이렉트 합니다.
        - HTTP 상태코드: `400`
     - 주어진 데이터의 `username` 을 가지고 있는 데이터가 이미 데이터베이스에 존재하는 경우:
        - 해당 유저의 트윗 값들을 업데이트 합니다.
        - 리턴값: main_route.py 에 있는 user_index 함수로 리다이렉트 합니다.
        - HTTP 상태코드: `200`
      - 정상적으로 주어진 `username` 을 트위터에서 가져오고 해당 유저의 트윗 또한 가져화 벡터화해서 데이터베이스에 기록한 경우:
        - 리턴값: main_route.py 에 있는 user_index 함수로 리다이렉트 합니다.
        - HTTP 상태코드: `200`
    """
    # username이 있는가?
    username = request.form["username"].lower()
    if not username:
      return "Needs username", 400  
    
    # 트위터에 username이 있는가?
    try :
      raw_user = get_user(username)
    except :
      return redirect(url_for('main.user_index', msg_code=0), code=400)
      
    # DB에 있는가?
    user = User.query.filter(User.username == username).first()
    if user:
      db.session.delete(user)
      db.session.commit()
    
    user = User(username=username
                ,full_name=raw_user.name
                ,followers=raw_user.followers_count)
    db.session.add(user)
    db.session.commit()
    # tweet 텍스트 + embedding 넣기
    txt = [[tw.full_text] for tw in get_tweets(username)]
    for tw in txt:
      tw_emb = get_embeddings(tw)
      tweet_up = Tweet(text=tw[0], embedding=tw_emb[0], user_id=user.id)
      db.session.add(tweet_up)
      db.session.commit()

    return redirect(url_for('main.user_index', msg_code=0), code=200)


@bp.route('/user/', defaults={ 'user_id' : None })
@bp.route('/user/<int:user_id>')
def delete_user(user_id):
    """
    delete_user 함수는 `user_id` 를 엔드포인트 값으로 넘겨주면 해당 아이디 값을 가진 유저를 데이터베이스에서 제거해야 합니다.
    요구사항:
      - HTTP Method: `GET`
      - Endpoint: `api/user/<user_id>`
    상황별 요구사항:
      -  `user_id` 값이 주어지지 않은 경우:
        - 리턴값: 없음
        - HTTP 상태코드: `400`
      - `user_id` 가 주어졌지만 해당되는 유저가 데이터베이스에 없는 경우:
        - 리턴값: 없음
        - HTTP 상태코드: `404`
      - 주어진 `username` 값을 가진 유저를 정상적으로 데이터베이스에서 삭제한 경우:
        - 리턴값: main_route.py 에 있는 user_index 함수로 리다이렉트 합니다.
        - HTTP 상태코드: `200`
    """
    if user_id is None :
      return "user_id is not given",400

    user = User.query.filter(User.id == user_id).first()
    if not user:
      return "Can't find user id '{user_id}' in DB",404
    else :
      db.session.delete(user)
      db.session.commit()

      return redirect(url_for('main.user_index', msg_code=3), code=200)