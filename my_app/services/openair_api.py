import requests
import pandas as pd

cities = ['서울', '부산', '대구', '인천', '광주', '대전', '울산','경기', '강원', '충북', '충남', '전북', '전남', '경북', '경남', '제주', '세종']
serviceKey = 'M1iN3AHXsY2arykGcomyFyS16TTG5V%2Ftwy%2B1pTToDLK8ottKutqdpbla7Fna9tjr4xMe89FHcSeCzJ4ixfxqFw%3D%3D'
endpoint = 'http://openapi.airkorea.or.kr/openapi/services/rest/ArpltnInforInqireSvc/getCtprvnRltmMesureDnsty?sidoName={cities}&ServiceKey={serviceKey}&ver=1.3&_returnType=json'.format(serviceKey=serviceKey)


def get_dust(screen_name):
    """
    `get_user` 함수는 트위터의 `screen_name` 이 주어지면 tweepy 를 통해 해당
    트위터 유저를 조회한 객체를 그대로 리턴합니다.
    """
    resp = requests.get(endpoint)
    raw_json = resp.json()
    return raw_json
