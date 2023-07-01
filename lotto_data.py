#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import requests
import sqlite3
import os.path
import argparse
from bs4 import BeautifulSoup
from collections import defaultdict
from collections import Counter


class HandelColors:
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'


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

    def latest_round(self):
        try:
            cur = self.conn.cursor()
            cur.execute('SELECT round FROM tb_lotto_list ORDER BY round DESC')
            ret = cur.fetchone()[0]
            return int(ret)
        except Exception as err:
            print(err)
            return 0

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

    def select_all(self):
        try:
            cur = self.conn.cursor()
            query = """
            SELECT 
                GROUP_CONCAT(data.num) AS num 
            FROM (
                SELECT 
                    ("1st"||","||"2nd"||","||"3rd"||","||"4th"||","||"5th"||","||"6th"||","||"bonus") AS num
                FROM
                    tb_lotto_list
                ) AS data
            """
            cur.execute(query)
            return cur.fetchone()
        except Exception as err:
            print(err)
            return ""

    def select_all_except_bonus(self):
        try:
            cur = self.conn.cursor()
            query = """
            SELECT 
                GROUP_CONCAT(data.num) AS num 
            FROM (
                SELECT 
                    ("1st"||","||"2nd"||","||"3rd"||","||"4th"||","||"5th"||","||"6th") AS num
                FROM
                    tb_lotto_list
                ) AS data
            """
            cur.execute(query)
            return cur.fetchone()
        except Exception as err:
            print(err)
            return ""

    def select_custom(self, sround, eround):
        try:
            cur = self.conn.cursor()
            query = """
            SELECT
                GROUP_CONCAT(num) AS num 
            FROM (
                SELECT 
                    ("1st"||","||"2nd"||","||"3rd"||","||"4th"||","||"5th"||","||"6th"||","||"bonus") AS num
                FROM
                    tb_lotto_list
                WHERE
                    round BETWEEN {sround} and {eround}
                ) 
            """.format(sround=sround, eround=eround)
            cur.execute(query)
            return cur.fetchone()
        except Exception as err:
            print(err)
            return ""

    def select_custom_except_bonus(self, sround, eround):
        try:
            cur = self.conn.cursor()
            query = """
            SELECT
                GROUP_CONCAT(num) AS num 
            FROM (
                SELECT 
                    ("1st"||","||"2nd"||","||"3rd"||","||"4th"||","||"5th"||","||"6th") AS num
                FROM
                    tb_lotto_list
                WHERE
                    round BETWEEN {sround} and {eround}
                ) 
            """.format(sround=sround, eround=eround)
            cur.execute(query)
            return cur.fetchone()
        except Exception as err:
            print(err)
            return ""


class LottoData:
    """
    로또 최신 데이터 확인 및 데이터베이스 Insert
    """
    def __init__(self, db_path):
        self.db_path = db_path
        self.site_url = 'https://www.dhlottery.co.kr/common.do?method=main&mainMode=default'

    @staticmethod
    def __set_round_date(round_date):
        try:
            rd = round_date.replace('-', '.')
            return rd.strip('(').strip(')').strip('추첨')
        except Exception as err:
            print(err)
            return round_date


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
                "round_date": self.__set_round_date(content_data.find('span', {'id': 'drwNoDate'}).text),
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
        except Exception as err:
            print(err)
        sys.exit(0)


class LottoStatistics:
    """
    로또 당첨 번호 통계 확인
    """
    def __init__(self, db_path):
        self.db_path = db_path
        self.handler = HandelSQLite(self.db_path)

    def all(self, bonus=True):
        try:
            last_round = self.handler.latest_round()
            if bonus:
                data = self.handler.select_all()
                comment = "전체 통계"
            else:
                data = self.handler.select_all_except_bonus()
                comment = "보너스볼 제외 통계"
            data_list = list(map(int, data[0].split(",")))
            counter = Counter(data_list)
            print("### 1회 ~ {last_round}회 {comment} ###".format(last_round=last_round, comment=comment))
            for i in counter.most_common(45):
                print("{num}번 : {cnt}개".format(num=i[0], cnt=i[1]))
        except Exception as err:
            print(err)
        sys.exit(0)

    def custom_top(self, count=6, bonus=True):
        try:
            if not isinstance(count, int):
                count = 6
            last_round = self.handler.latest_round()
            if bonus:
                data = self.handler.select_all()
                comment = "전체 통계"
            else:
                data = self.handler.select_all_except_bonus()
                comment = "보너스볼 제외 통계"
            data_list = list(map(int, data[0].split(",")))
            counter = Counter(data_list)
            print("### 1회 ~ {last_round}회 Top {count} {comment} ###".format(
                last_round=last_round, count=count, comment=comment)
            )
            for i in counter.most_common(count):
                print("{num}번 : {cnt}개".format(num=i[0], cnt=i[1]))
        except Exception as err:
            print(err)
        sys.exit(0)

    def custom_round_top(self, sround, eround, count=6, bonus=True):
        try:
            last_round = self.handler.latest_round()
            if not isinstance(sround, int):
                sround = 1
            if not isinstance(eround, int):
                eround = last_round
            if not isinstance(count, int):
                count = 6
            if sround > last_round or eround > last_round:
                print("입력하신 {eround}회차는 존재하지 않습니다. \n"
                      "마지막 회차는 {last_round}회차 입니다. \n"
                      "다시 입력 부탁 드립니다.".format(eround=eround, last_round=last_round))
                sys.exit(0)
            if bonus:
                data = self.handler.select_custom(sround, eround)
                comment = "전체 통계"
            else:
                data = self.handler.select_custom_except_bonus(sround, eround)
                comment = "보너스볼 제외 통계"
            data_list = list(map(int, data[0].split(",")))
            counter = Counter(data_list)
            print("### {sround}회 ~ {eround}회 Top {count} {comment} ###".format(
                sround=sround, eround=eround, count=count, comment=comment)
            )
            for i in counter.most_common(count):
                print("{num}번 : {cnt}개".format(num=i[0], cnt=i[1]))
        except Exception as err:
            print(err)
        sys.exit(0)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='lotto', description='로또 최신 당첨번호 입력 및 통계 Tool')
    try:
        parser.add_argument('-d', '--db', dest='db_path', type=str, default='./lotto_data.db',
                            help='로또 당첨번호 DataBase Path')
        parser.add_argument('-i', '--insert', action='store_true', help='최신 로또 당첨번호 DataBase Insert')
        parser.add_argument('-s', '--stat', action='store_true', help='로또 당첨번호 통계')
        parser.add_argument('-t', '--top', type=int, nargs='?', const=6, help='로또 당첨번호 전체 top 통계')
        parser.add_argument('-c', '--custom', type=int, nargs='?', const=6, help='로또 당첨번호 Custom top 통계')
        parser.add_argument('-sr', '--sround', type=int, nargs='?', const=1, help='로또 당첨번호 top 통계')
        parser.add_argument('-er', '--eround', type=int, nargs='?', const=1007, help='로또 당첨번호 top 통계')
        parser.add_argument('-exb', '--ex_bonus', dest="ex_bonus", action='store_false', help='보너스볼 제외')
        parser.add_argument('-v', '--version', action='version', version='%(prog)s 1.1')
        args = parser.parse_args()
        db_path = args.db_path
        if args.insert:
            lotto_data = LottoData(db_path)
            lotto_data.run()
            sys.exit(0)
        LottoStatistics = LottoStatistics(db_path)
        if args.stat:
            LottoStatistics.all(args.ex_bonus)
            sys.exit(0)
        if args.top:
            LottoStatistics.custom_top(args.top, args.ex_bonus)
            sys.exit(0)
        if args.custom and args.sround and args.eround:
            LottoStatistics.custom_round_top(args.sround, args.eround, args.custom, args.ex_bonus)
            sys.exit(0)
    except Exception as err:
        print(err)
        sys.exit(0)

