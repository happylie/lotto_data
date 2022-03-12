# 로또 당첨 번호 데이터
<div>
<img src="https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fgithub.com%2Fhappylie%2Flotto_data&count_bg=%2379C83D&title_bg=%23555555&icon=github.svg&icon_color=%23E7E7E7&title=view&edge_flat=false"/>
<img src="https://img.shields.io/badge/SQLite-v3.34.1-blue?logo=sqlite" />
<img src="https://img.shields.io/badge/Python-3.5.x +-blue?logo=python&logoColor=white" />
</div>

1회 부터 현재까지 로또 당첨 번호 데이터베이스
- 매주 로또 당첨 번호 발표날 신규 회차 업데이트 예정
- https://happylie.tistory.com/97

## 현재 데이터 
- 1회 ~ 1004회 / 2022.03.04 추가
- 1005회 / 2022.03.05 추가
- 1006회 / 2022.03.12 추가

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

## 최신 당첨 번호 Tool 이용해서 업데이트 하기
### 사용 방법
1. python 3.5.x 버전 이상에서 구동
2. requirements.txt 내 패키기 설치
   - requests
   - bs4
3. lotto_data.py 실행
   - $ python lotto_data.py
