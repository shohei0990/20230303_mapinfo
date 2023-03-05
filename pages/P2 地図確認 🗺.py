import streamlit as st
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
df_mapsele = pd.DataFrame([[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]],
                          columns=['駅', 'バス停', 'スーパー', '公園', '薬局', 'コンビニ', '学校', '飲食店'])

st.title(f"● {df_map_0['名称']}　　MAP情報")
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

info_col2, map_col2, = st.columns([1, 3], gap="medium")

info_col2.subheader("周辺検索:")
df_mapsele['駅'][0] = info_col2.checkbox("駅")
df_mapsele['バス停'][0] = info_col2.checkbox("バス停")
df_mapsele['スーパー'][0] = info_col2.checkbox("スーパー")
df_mapsele['公園'][0] = info_col2.checkbox("公園")
df_mapsele['薬局'][0] = info_col2.checkbox("薬局")
df_mapsele['コンビニ'][0] = info_col2.checkbox("コンビニ")
df_mapsele['学校'][0] = info_col2.checkbox("学校")
df_mapsele['飲食店'][0] = info_col2.checkbox("飲食店")


if info_col2.button('MAP検索'):
    state.map_sele = 1

if "map_sele" not in state:
    state.map_sele = 0

elif state.map_sele == 1:

    for column_name, item in df_mapsele.iteritems():
        print('------')
        print(column_name)
        print(item)
        print(item[0])
        print('======\n')

        if item[0] == True:
            # パラメータリスト
            api_key = st.secrets.GMAP.key
            radius = 500  # 半径500m
            keyword = column_name
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
                    icon=folium.Icon(
                        icon="bell", icon_color="white", color="blue")
                ).add_to(m)

map_col2.subheader("地図:")
with map_col2:
    map = st_folium(m, width=1000, height=600)


st.markdown("---")

image_col, info_col, sele_col = st.columns([2, 3, 2], gap="medium")
image_col.image(f"{df_map_0['画像']}", use_column_width=True)

df_0 = pd.DataFrame(state.df_map2)
info_col.subheader(f"● {df_0.columns[0]}")
info_col.dataframe(state.df_map2, width=500, height=458)
