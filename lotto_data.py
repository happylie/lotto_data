#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import requests
import sqlite3
import os.path
from bs4 import BeautifulSoup
from collections import defaultdict


class HandelSQLite:
    """
    DataBase 관련 Handling Class
    """
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)

    def __del__(self):
        self.conn.close()

    def check_latest_round(self, input_round):
        try:
            cur = self.conn.cursor()
            cur.execute('SELECT round FROM tb_lotto_list ORDER BY round DESC')
            select_round = cur.fetchone()
            if int(input_round) == int(select_round[0]):
                return False
            return True
        except Exception as err:
            print(err)
            return False

    def insert_data(self, input_data):
        try:
            cur = self.conn.cursor()
            query = """
            INSERT INTO 
                tb_lotto_list 
            VALUES (
                    {round}, '{date}', {drw_1st}, {drw_2nd}, {drw_3rd}, {drw_4th}, {drw_5th}, {drw_6th}, {bonus}
                    )
            """.format(
                round=input_data.get('round'), date=input_data.get('round_date'), drw_1st=input_data.get('drw_1st'),
                drw_2nd=input_data.get('drw_2nd'), drw_3rd=input_data.get('drw_3rd'), drw_4th=input_data.get('drw_4th'),
                drw_5th=input_data.get('drw_5th'), drw_6th=input_data.get('drw_6th'), bonus=input_data.get('drw_bnus')
            )
            cur.execute(query)
            self.conn.commit()
            return True
        except Exception as err:
            print(err)
            return False


class LottoData:
    """
    로또 최신 데이터 확인 및 데이터베이스 Insert
    """
    def __init__(self, db_path):
        self.db_path = db_path
        self.site_url = 'https://www.dhlottery.co.kr/common.do?method=main'

    def __get_lotto_info(self):
        """
        동행복권 사이트에서 최신 회차 데이터 가지고 오기
        :return: bool, dict
        """
        ret_json = defaultdict(int)
        try:
            info_data = requests.get(self.site_url)
            if info_data.status_code != 200:
                return False, {}
            bs = BeautifulSoup(info_data.text, 'html.parser')
            content_data = bs.find('div', {'class': 'content'})
            if not content_data:
                return False, {}
            ret_json = {
                "round": int(content_data.find('strong', {'id': 'lottoDrwNo'}).text),
                "round_date": content_data.find('span', {'id': 'drwNoDate'}).text.replace('-', '.'),
                "drw_1st": int(content_data.find('span', {'id': 'drwtNo1'}).text),
                "drw_2nd": int(content_data.find('span', {'id': 'drwtNo2'}).text),
                "drw_3rd": int(content_data.find('span', {'id': 'drwtNo3'}).text),
                "drw_4th": int(content_data.find('span', {'id': 'drwtNo4'}).text),
                "drw_5th": int(content_data.find('span', {'id': 'drwtNo5'}).text),
                "drw_6th": int(content_data.find('span', {'id': 'drwtNo6'}).text),
                "drw_bnus": int(content_data.find('span', {'id': 'bnusNo'}).text)
            }
            return True, ret_json
        except Exception as err:
            print(err)
            return False, ret_json

    def run(self):
        try:
            ret, data = self.__get_lotto_info()
            if not ret:
                print("동행복권 사이트에서 최신 로또 당첨 번호를 가지고 오지 못했습니다.")
                sys.exit(0)
            latest_round = data.get('round')
            if not os.path.exists(self.db_path):
                print("로또 데이터베이스 파일이 존재하지 않습니다.")
                sys.exit(0)
            handler = HandelSQLite(self.db_path)
            if not handler.check_latest_round(latest_round):
                print("{latest_round}회 로또 당첨 번호 데이터가 이미 존재합니다.".format(latest_round=latest_round))
                sys.exit(0)
            if not handler.insert_data(data):
                print("{latest_round}회 로또 당첨 번호 입력 중 문제가 발생하였습니다.".format(latest_round=latest_round))
                sys.exit(0)
            print("정상적으로 {latest_round}회 로또 당첨 번호를 데이터베이스에 등록하였습니다.".format(latest_round=latest_round))
            sys.exit(0)
        except Exception as err:
            print(err)
            sys.exit(0)


if __name__ == '__main__':
    db_path = './lotto_data.db'   # 반드시 데이테베이스 위치를 지정.
    lotto_data = LottoData(db_path)
    lotto_data.run()
