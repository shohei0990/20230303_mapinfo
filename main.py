import streamlit as st                      # streamlit
from streamlit_folium import st_folium    # streamlitでfoliumを使う
import pandas as pd                         # CSVをデータフレームとして読み込む
import requests
import urllib
from urllib.parse import urlencode

# 表示するデータを読み込み2
df_final = pd.read_csv('realestate_info_finalimage.csv')

# ページ設定
st.set_page_config(
    page_title="streamlit-foliumテスト",
    page_icon="🗾",
    layout="wide"
)

# 1. 画面の表示
# サイドバー
st.sidebar.title('MAP表示条件')
xmax = st.sidebar.number_input('物件表示数 ：', 0, 1000, 100)
ymax = st.sidebar.number_input('test ：', 0, 1000, 200)

# メイン画面 検索
st.title('賃貸検索')
st.markdown("---")
st.subheader('検索条件')
extra_configs_0 = st.expander("検索条件1")  # Extra Configs
with extra_configs_0:
    se1 = st.number_input('家賃[万円]以下 ：', 0, 500, 30)
    se2 = st.number_input('面積[m^2]以上 ：', 0, 500, 50)

extra_configs_1 = st.expander("検索条件2")  # Extra Configs
with extra_configs_1:
    se3 = st.multiselect(
        '間取り', ['ワンルーム', '1K', '1DK', '1LDK', '2DK', '2LDK'], ['2LDK'])
    se4 = st.multiselect('区', ['品川', '渋谷', '江戸川', '港'], ['品川', '江戸川'])
    #se5 = st.multiselect('市町', ['南品川', '東五反田', '南大井', '東品川'], ['南品川'])

# 住所追加
extra_configs_2 = st.expander("周辺施設")  # Extra Configs
with extra_configs_2:
    se6 = st.multiselect('検索施設', ['コンビニ', 'スーパー', '病院', '公園'], ['コンビニ'])


# フィルタリング
df_final0 = df_final
joken1 = (df_final0["家賃"] > 0) & (df_final0["家賃"] < se1)
df_final0 = df_final0[joken1]
joken2 = (df_final0["面積"] > se2) & (df_final0["面積"] < 300)
df_final0 = df_final0[joken2]
joken3 = df_final0["間取り"].isin(se3)
df_final0 = df_final0[joken3]
joken4 = df_final0["区"].isin(se4)
df_final0 = df_final0[joken4]

st.subheader('(フィルター後のデータ確認用)')
# フィルター後の地図データを作成する
# 表示するデータを読み込み1

df_final0 = df_final0.drop_duplicates(subset=['名称', '階数'])

se90 = st.write(df_final0)
se91 = st.write(df_final0.shape)

if df_final0.shape[0] > 50:
    df = df_final0[:50]
else:
    df = df_final0


def Map_info(x):
    makeUrl = "https://msearch.gsi.go.jp/address-search/AddressSearch?q="
    s_quote = urllib.parse.quote(x['アドレス'])
    response = requests.get(makeUrl + s_quote)
    try:
        map_info_d = response.json()[0]["geometry"]["coordinates"]
        #map_info_d = pd.DataFrame(map_info)
        return map_info_d[0], map_info_d[1]
    except Exception as e:
        print(e)
        return 0, 0


df_info = pd.DataFrame()
df_info[['経度', '緯度']] = df.apply(lambda x: Map_info(x),
                                 axis=1, result_type='expand')

df = pd.concat([df, df_info], axis=1)

se90 = st.write(df)
se91 = st.write(df.shape)
