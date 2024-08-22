import pandas as pd
import requests
from io import BytesIO
import folium
import json

# GitHub raw 파일 URL
url = 'https://raw.githubusercontent.com/aaqq8/SteadyEstate/main/%EC%84%9C%EC%9A%B8%20%EC%A4%91%EC%9C%84%20%EC%A0%84%EC%84%B8%20%EA%B0%80%EA%B2%A9%20%EB%8B%A8%EB%8F%85%EC%A3%BC%ED%83%9D.xlsx'

# 파일 가져오기
response = requests.get(url)

if response.status_code == 200:
    # 엑셀 파일을 pandas로 읽기 (openpyxl 엔진 사용)
    file_decoded = BytesIO(response.content)
    df = pd.read_excel(file_decoded, engine='openpyxl')

    # 연도와 월별 데이터만 선택 (첫 번째 열은 '지 역'이고 나머지는 가격 데이터)
    price_data = df.iloc[:, 1:]  # 첫 번째 열은 제외하고 나머지 열 선택
    price_data.set_index(df['지 역'], inplace=True)  # '지 역'을 인덱스로 설정

    # 구별 중위 전세 가격 계산 (행 단위로 중위값 계산)
    seoul_group_data = price_data.median(axis=1)

    # 결과 확인
    print(seoul_group_data.head())
else:
    print("파일을 가져오지 못했습니다.")