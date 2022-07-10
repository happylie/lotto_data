# 로또 당첨 번호 데이터
<div>
<img src="https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fgithub.com%2Fhappylie%2Flotto_data&count_bg=%2379C83D&title_bg=%23555555&icon=github.svg&icon_color=%23E7E7E7&title=view&edge_flat=false"/>
<img src="https://img.shields.io/badge/SQLite->=3.34.1-blue?logo=sqlite" />
<img src="https://img.shields.io/badge/Python->=3.5-blue?logo=python&logoColor=white" />
</div>

1회 부터 현재까지 로또 당첨 번호 데이터베이스
- 매주 로또 당첨 번호 발표날 신규 회차 업데이트 예정
- https://happylie.tistory.com/97

## 로또 당첨 번호 Tool 
### 설치 방법
1. Git Clone
```
$ git clone https://github.com/happylie/lotto_data.git
```
2. Requirements 설치
```
$ pip install -r requirements.txt
```
### 실행 방법
1. Help
```
$ python lotto_data.py -h
usage: lotto [-h] [-d DB_PATH] [-i] [-s] [-t [TOP]] [-c [CUSTOM]] [-sr [SROUND]] [-er [EROUND]] [-exb] [-v]

로또 최신 당첨번호 입력 및 통계 Tool

optional arguments:
  -h, --help            show this help message and exit
  -d DB_PATH, --db DB_PATH
                        로또 당첨번호 DataBase Path
  -i, --insert          최신 로또 당첨번호 DataBase Insert
  -s, --stat            로또 당첨번호 통계
  -t [TOP], --top [TOP]
                        로또 당첨번호 전체 top 통계
  -c [CUSTOM], --custom [CUSTOM]
                        로또 당첨번호 Custom top 통계
  -sr [SROUND], --sround [SROUND]
                        로또 당첨번호 top 통계
  -er [EROUND], --eround [EROUND]
                        로또 당첨번호 top 통계
  -exb, --ex_bonus      보너스볼 제외
  -v, --version         show program's version number and exit
```
2. 최신 로또 데이터 등록
```
$ python ex_lotto.py -i                    
정상적으로 1007회 로또 당첨 번호를 데이터베이스에 등록하였습니다.
```
3. 전체 당첨번호 통계 확인
```
$ python lotto_data.py -s
### 1회 ~ 1007회 전체 통계 ###
43번 : 180개
1번 : 172개
... 이하 생략 ...
```
4. 전체 당첨번호 보너스볼 제외 통계 확인
```
$ python lotto_data.py -s -exb
### 1회 ~ 1007회 보너스볼 제외 통계 ###
34번 : 152개
18번 : 148개
... 이하 생략 ...
```
5. 당첨번호 Top 통계 확인
```
$ python lotto_data.py -t
### 1회 ~ 1007회 Top 6 전체 통계 ###
43번 : 180개
1번 : 172개
27번 : 172개
34번 : 171개
17번 : 171개
13번 : 171개

$ python lotto_data.py -t 10
### 1회 ~ 1007회 Top 10 전체 통계 ###
43번 : 180개
1번 : 172개
27번 : 172개
34번 : 171개
17번 : 171개
13번 : 171개
39번 : 167개
4번 : 167개
33번 : 167개
12번 : 165개
```
6. 당첨번호 Top 보너스볼 제외 통계 확인
```
$ python lotto_data.py -t -exb
### 1회 ~ 1007회 Top 6 보너스볼 제외 통계 ###
34번 : 152개
18번 : 148개
27번 : 146개
43번 : 146개
17번 : 145개
13번 : 145개

$ python lotto_data.py -t 10 -exb
### 1회 ~ 1007회 Top 10 보너스볼 제외 통계 ###
34번 : 152개
18번 : 148개
27번 : 146개
43번 : 146개
17번 : 145개
13번 : 145개
39번 : 145개
1번 : 143개
12번 : 142개
14번 : 142개
```
7. 당첨번호 커스텀 Top 통계 확인
```
$ python lotto_data.py -c -sr 1000 -er 1007
### 1000회 ~ 1007회 Top 6 전체 통계 ###
8번 : 4개
15번 : 4개
39번 : 3개
17번 : 3개
19번 : 2개
42번 : 2개

$ python lotto_data.py -c 10 -sr 1000 -er 1007
### 1000회 ~ 1007회 Top 10 전체 통계 ###
8번 : 4개
15번 : 4개
39번 : 3개
17번 : 3개
19번 : 2개
42번 : 2개
25번 : 2개
45번 : 2개
29번 : 2개
37번 : 2개
```
8.당첨번호 커스텀 Top 보너스볼 제외 통계 확인
```
$ python lotto_data.py -c -sr 1000 -er 1007 -exb
### 1000회 ~ 1007회 Top 6 보너스볼 제외 통계 ###
8번 : 4개
19번 : 2개
42번 : 2개
17번 : 2개
25번 : 2개
45번 : 2개

$ python lotto_data.py -c 10 -sr 1000 -er 1007 -exb
### 1000회 ~ 1007회 Top 10 보너스볼 제외 통계 ###
8번 : 4개
19번 : 2개
42번 : 2개
17번 : 2개
25번 : 2개
45번 : 2개
29번 : 2개
39번 : 2개
15번 : 2개
37번 : 2개
```
## 현재 데이터 
- 1회 ~ 1021회 / 2022.06.25 추가
- 1022회 / 2022.07.02 추가
- 1023회 / 2022.07.09 추가

## 데이터 스키마

### tb_lotto_list

- 각회별 로또 당첨 번호 리스트

| 필드명    | Type     | 설명      |
|:-------:|:--------:|:--------:|
|  round  | INTEGER  | 회차      |
|  date   | TEXT     | 회차 추첨일 |
|  1st    | INTEGER  | 1번째 번호 |
|  2nd    | INTEGER  | 2번째 번호 |
|  3rd    | INTEGER  | 3번째 번호 |
|  4th    | INTEGER  | 4번째 번호 |
|  5th    | INTEGER  | 5번째 번호 |
|  6th    | INTEGER  | 6번째 번호 |
|  bonus  | INTEGER  | 보너스 번호 |

![table_info](https://user-images.githubusercontent.com/24468970/156866295-02558131-2840-404d-9f56-0cb995c2d0f3.png)
