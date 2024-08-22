import pandas as pd
import requests
from io import BytesIO
import folium
import json

# GitHub raw 파일 URL
url = 'https://raw.githubusercontent.com/aaqq8/SteadyEstate/main/%EC%84%9C%EC%9A%B8%20%EC%A4%91%EC%9C%84%20%EB%A7%A4%EB%A7%A4%20%EA%B0%80%EA%B2%A9%20%EC%95%84%ED%8C%8C%ED%8A%B8.xlsx'

# 파일 가져오기
response = requests.get(url)

if response.status_code == 200:
    # 엑셀 파일을 pandas로 읽기 (openpyxl 엔진 사용)
    file_decoded = BytesIO(response.content)
    df = pd.read_excel(file_decoded, engine='openpyxl')

    # 연도와 월별 데이터만 선택 (첫 번째 열은 '지 역'이고 나머지는 가격 데이터)
    price_data = df.iloc[:, 1:]  # 첫 번째 열은 제외하고 나머지 열 선택
    price_data.set_index(df['지 역'], inplace=True)  # '지 역'을 인덱스로 설정

    # 구별 중위 매매 가격 계산 (행 단위로 중위값 계산)
    seoul_group_data = price_data.median(axis=1)

    # 결과 확인
    print(seoul_group_data.head())
else:
    print("파일을 가져오지 못했습니다.")

# GeoJSON 파일 가져오기
r = requests.get('https://raw.githubusercontent.com/southkorea/seoul-maps/master/kostat/2013/json/seoul_municipalities_geo_simple.json')
c = r.content
seoul_geo = json.loads(c)

# Folium 지도 생성
m = folium.Map(
    location=[37.559819, 126.963895],
    zoom_start=11, 
    tiles='CartoDB Voyager'
)

# GeoJson 레이어 추가 (서울 지역구 경계)
folium.GeoJson(
    seoul_geo,
    name='지역구'
).add_to(m)

# Choropleth Layer 추가 (서울 구별 중위 매매 가격)
folium.Choropleth(
    geo_data=seoul_geo,
    data=seoul_group_data, 
    fill_color='YlOrRd',  # 색상 변경 가능
    fill_opacity=0.5,
    line_opacity=0.2,
    key_on='feature.properties.name',  # GeoJSON의 'name' 속성을 데이터와 매핑
    legend_name="지역구별 중위 매매 가격 (천원)"
).add_to(m)

# 지도 표시
m.save('seoul_apartment_prices_median_map.html')
print("지도가 'seoul_apartment_prices_median_map.html' 파일로 저장되었습니다.")
