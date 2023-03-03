import streamlit as st
import pandas as pd
from streamlit_folium import st_folium    # streamlitでfoliumを使う
import folium                               # folium
import pandas as pd                         # CSVをデータフレームとして読み込む
import requests
import urllib
from urllib.parse import urlencode


# セッションステートを取得
state = st.session_state

if "df_map" not in state:
    state.df_map = pd.DataFrame()

df_map_0 = state.df_map

st.title(f"● {df_map_0['名称']}　　詳細・MAP情報")
st.markdown("---")

image_col, info_col, sele_col = st.columns([2, 3, 2], gap="medium")
image_col.image(f"{df_map_0['画像']}", use_column_width=True)

# info_col.text(f"住所　：{df_select_image['アドレス'][0]}")
# info_col.text(f"家賃　：{df_select_image['家賃'][0]}")
# info_col.text(f"間取り：{df_select_image['間取り'][0]}")
# info_col.text(f"面積　：{df_select_image['面積'][0]}")
# info_col.text(f"最寄駅：{df_select_image['最寄駅'][0]}")
# info_col.text(f"最寄駅：{df_select_image['徒歩時間'][0]}")
# info_col.text(f"築年数：{df_select_image['築年数'][0]}")
# info_col.text(f"階数　：{df_select_image['階数'][0]}")
# info_col.text(f"構造　：{df_select_image['構造'][0]}")
# info_col.text(f"敷金　：{df_select_image['敷金'][0]}")
# info_col.text(f"礼金　：{df_select_image['礼金'][0]}")
# info_col.text(f"管理費：{df_select_image['管理費'][0]}")

se90 = info_col.write(state.df_map)

st.markdown("---")
makeUrl = "https://msearch.gsi.go.jp/address-search/AddressSearch?q="
s_quote = urllib.parse.quote(df_map_0['アドレス'])
response = requests.get(makeUrl + s_quote)
map_info_d = response.json()[0]["geometry"]["coordinates"]
lng, lat = map_info_d[0], map_info_d[1]

# 地図の中心の緯度/経度、タイル、初期のズームサイズを指定します。
m = folium.Map(
    location=[lat, lng],
    tiles='https://cyberjapandata.gsi.go.jp/xyz/pale/{z}/{x}/{y}.png',
    attr='都道府県庁所在地、人口、面積(2016年)',
    zoom_start=15
)

# ポップアップの作成(都道府県名＋都道府県庁所在地＋人口＋面積)
pop = f"・家賃…{df_map_0['家賃']} "
folium.Marker(
    # 緯度と経度を指定
    location=[lat, lng],
    # ツールチップの指定(都道府県名)
    tooltip=df_map_0['名称'],
    # ポップアップの指定
    popup=folium.Popup(pop, max_width=300),
    # アイコンの指定(アイコン、色)
    icon=folium.Icon(icon="home", icon_color="white", color="red")
).add_to(m)

# パラメータリスト
# api_key = 'AGIzaSyAdFUui2C-RKcw48ApjPQJtBR_AAxIoWg4'
api_key = st.secrets.GMAP
radius = 500  # 半径500m
keyword = "コンビニ"
language = 'ja'

# エンドポイントURL
places_endpoint = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
# # パラメータ
params = {
    "key": api_key,
    "location": f"{lat},{lng}",
    "radius": radius,
    "keyword": keyword,
    "language": language,
}

# URLエンコード, リクエストURL生成
params_encoded = urlencode(params)
places_url = f"{places_endpoint}?{params_encoded}"

# 結果取得
r = requests.get(places_url)
data = r.json()

# APIレスポンスを取得
places = r.json()["results"]
df_cb = pd.DataFrame(columns=['名称', '住所', '緯度', '経度'])

# 各コンビニの位置情報を表示
for place in places:
    temp = pd.DataFrame(data=[[place["name"], place["vicinity"], round(place["geometry"]["location"]["lat"], 7), round(
        place["geometry"]["location"]["lng"], 7)]], columns=df_cb.columns)
    df_cb = pd.concat([df_cb, temp])
    print("名称:", place["name"])

df_cb = df_cb.reset_index()

for i, row in df_cb.iterrows():
    # ポップアップの作成(都道府県名＋都道府県庁所在地＋人口＋面積)
    pop = f"・名称…{row['名称']} <br>・距離[m]…"
    folium.Marker(
        # 緯度と経度を指定
        location=[row['緯度'], row['経度']],
        # ツールチップの指定(都道府県名)
        tooltip=row['名称'],
        # ポップアップの指定
        popup=folium.Popup(pop, max_width=300),
        # アイコンの指定(アイコン、色)
        icon=folium.Icon(icon="bell", icon_color="white", color="blue")
    ).add_to(m)

map_col2, info_col2 = st.columns([2, 1], gap="medium")

map_col2.subheader("MAP")
with map_col2:
    map = st_folium(m, width=1000, height=600)

se90 = st.write(state.df_map)
se91 = st.write(state.df_map.shape)
