import streamlit as st                    # streamlit
from streamlit_folium import st_folium    # streamlitでfoliumを使う
import pandas as pd
import requests
import urllib
from urllib.parse import urlencode
import gspread
from google.oauth2 import service_account
from google.oauth2.service_account import Credentials
from gspread_dataframe import get_as_dataframe
from gspread_dataframe import set_with_dataframe
from matplotlib import pyplot as plt
import japanize_matplotlib


japanize_matplotlib.japanize()
# plt.rcParams['font.family'] = 'MS Gothic'

# ページ設定
st.set_page_config(
    page_title="streamlit-foliumテスト",
    page_icon="🗾",
    layout="wide"
)

# セッションステートを取得
state = st.session_state
# googleスプレッドシートの認証 streamlit io　のシークレット活用


def gsheet_read():
    scopes = ['https://www.googleapis.com/auth/spreadsheets',
              'https://www.googleapis.com/auth/drive']
    credentials = service_account.Credentials.from_service_account_info(
        st.secrets["gcp_service_account"], scopes=scopes)
    gc = gspread.authorize(credentials)

    # googleスプレッドシートの読み込み
    SP_SHEET_KEY = st.secrets.SP_SHEET_KEY.key  # スプレッドシートのキー
    sh = gc.open_by_key(SP_SHEET_KEY)
    SP_SHEET = 'ueno003'  # sheet名
    worksheet = sh.worksheet(SP_SHEET)  # シートのデータ取得

    # sampleデータの取得
    pre_data = worksheet.get_all_values()
    col_name = pre_data[0][:]
    df_gs = pd.DataFrame(pre_data[1:], columns=col_name)

    # 取得数字データのstr型から数字の型変換
    select_columns_num = ['面積', '家賃', '敷金', '礼金',
                          '管理費', '築年数', '構造', '階数', '徒歩時間']
    pre0_df = df_gs[select_columns_num]
    for column in pre0_df:
        pre0_df[column] = pd.to_numeric(pre0_df[column], errors='coerce')
    df_gs[select_columns_num] = pre0_df

    return(df_gs)

# 緯度・経度情報の取得


def Map_info(x):
    makeUrl = "https://msearch.gsi.go.jp/address-search/AddressSearch?q="
    s_quote = urllib.parse.quote(x['アドレス'])
    response = requests.get(makeUrl + s_quote)
    try:
        map_info_d = response.json()[0]["geometry"]["coordinates"]
        return map_info_d[0], map_info_d[1]
    except Exception as e:
        print(e)
        return 0, 0


df_final = pd.DataFrame()
# 公開時に使用する。
df_final = gsheet_read()

# ローカルテスト用
#df_final = pd.read_csv('realestateinfo_test _ueno003.csv')

# 1. 画面の表示
# サイドバー
# st.sidebar.title('MAP表示条件')
# xmax = st.sidebar.number_input('物件表示数 ：', 0, 1000, 100)
# ymax = st.sidebar.number_input('test ：', 0, 1000, 200)

# メイン画面 検索
st.title('賃貸物件の絞り込み')
st.markdown("---")
text_col, gra_col = st.columns([1, 1], gap="medium")
text_col.subheader('絞り込み条件 : ')
se1_min, se1_max = text_col.slider("● 家賃[万円] の 下限 ～ 上限", 0, 100, (3, 30))
se2_min, se2_max = text_col.slider("● 面積[m^2] の 下限 ～ 上限 ", 0, 250, (5, 90))
se3_min, se3_max = text_col.slider("● 駅徒歩[分] 以内", 0, 30, (0, 15))

st.markdown("---")
text_col2, gra_col2, jr_col2, eki_col2 = st.columns([1, 1, 1, 1], gap="medium")
text_col2.subheader('詳細条件1 : ')

se4_min, se4_max = text_col2.slider("● 築年数 ", 0, 30, (0, 15))
se4_min, se4_max = text_col2.slider("● 階数 ", 0, 30, (0, 15))

#    se3 = st.multiselect(
#        '間取り', ['ワンルーム', '1K', '1DK', '1LDK', '2DK', '2LDK'], ['2LDK'])
#    se4 = st.multiselect('区', ['品川', '渋谷', '江戸川', '港'], ['品川'])
#    se5 = st.multiselect('市町', ['南品川', '東五反田', '南大井', '東品川'], ['南品川'])
# df[df['id'] == 1]

# フィルタリング
df_final0 = df_final
joken1 = (df_final0["家賃"] > se1_min) & (df_final0["家賃"] < se1_max)
df_final0 = df_final0[joken1]
joken2 = (df_final0["面積"] > se2_min) & (df_final0["面積"] < se2_max)
df_final0 = df_final0[joken2]
joken3 = (df_final0["徒歩時間"] > se3_min) & (df_final0["徒歩時間"] < se3_max)
df_final0 = df_final0[joken3]
joken4 = (df_final0["築年数"] > se4_min) & (df_final0["築年数"] < se4_max)
df_final0 = df_final0[joken4]
# joken3 = df_final0["間取り"].isin(se3)
# df_final0 = df_final0[joken3]
# joken4 = df_final0["区"].isin(se4)
# df_final0 = df_final0[joken4]

japanize_matplotlib.japanize()
gra_col.subheader(f"物件ヒット数 {df_final0.shape[0]}件　:　")
fig = plt.figure(figsize=(10, 5))
plt.hist(df_final0["家賃"], bins=30, range=(0, 50))  # , normed=True
plt.xlim([0, 50])
plt.ylim([0, 50])
plt.xlabel('家賃[万円]')
plt.ylabel('物件数')
# plt.title("物件数")
gra_col.pyplot(fig)

if text_col.button('検索実行'):
    state.df = df_final0
    se50 = text_col.write('➡➡➡   P1 物件探しのページに進んでください！')

# df_room = pd.DataFrame([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
#                       columns=['ワンルーム', '1R', '1K', '1DK', '1LDK', '2K', '2DK', '2LDK', '3K', '3DK', '3LDK', '4K', '4DK', '4LDK'])

a0 = (df_final0['間取り'] == 'ワンルーム').sum()
a1 = (df_final0['間取り'] == '1R').sum()
a2 = (df_final0['間取り'] == '1K').sum()
a3 = (df_final0['間取り'] == '1DK').sum()
a4 = (df_final0['間取り'] == '1LDK').sum()
a5 = (df_final0['間取り'] == '2K').sum()
a6 = (df_final0['間取り'] == '2DK').sum()
a7 = (df_final0['間取り'] == '2LDK').sum()
a8 = (df_final0['間取り'] == '3K').sum()
a9 = (df_final0['間取り'] == '3DK').sum()
a10 = (df_final0['間取り'] == '3LDK').sum()
a11 = (df_final0['間取り'] == '4K').sum()
a12 = (df_final0['間取り'] == '4DK').sum()
a13 = (df_final0['間取り'] == '4LDK').sum()
a15 = (df_final0['間取り'] == '1SLDK').sum()
a14 = df_final0.shape[0]-(a0+a1+a2+a3+a4+a5+a6+a7+a8+a9+a10+a11+a12+a13+a15)

gra_col2.subheader('2 :')
gra_col2.write('● 間取り')
gra_col2.checkbox(f"ワンルーム  ({a0+a1}件)", value=True)
gra_col2.checkbox(f"1K/DK/LDK/1SLDK ({a2+a3+a4+a15}件)", value=True)
gra_col2.checkbox(f"2K/DK/LDK ({a5+a6+a7}件)", value=True)
gra_col2.checkbox(f"3K/DK/LDK ({a8+a9+a10}件)", value=True)
gra_col2.checkbox(f"4K/DK/LDK ({a11+a12+a13}件)", value=True)
gra_col2.checkbox(f"5K以上 ({a14}件)", value=True)

jr_col2.subheader('3 :')
jr_col2.write('● 最寄駅:JR')
jr_col2.checkbox(f"大井町駅", value=True)
jr_col2.checkbox(f"西大井駅", value=True)
jr_col2.checkbox(f"大崎駅", value=True)
jr_col2.checkbox(f"大森駅", value=True)
jr_col2.checkbox(f"五反田駅", value=True)

eki_col2.subheader('4 :')
eki_col2.write('● 最寄駅:')
eki_col2.checkbox(f"荏原町駅", value=True)
eki_col2.checkbox(f"戸越銀座駅", value=True)
eki_col2.checkbox(f"戸越公園駅", value=True)
eki_col2.checkbox(f"不動前駅", value=True)
eki_col2.checkbox(f"旗の台駅", value=True)
eki_col2.checkbox(f"立会川駅", value=True)
eki_col2.checkbox(f"品川シーサイド駅", value=True)
eki_col2.checkbox(f"新馬場駅", value=True)
eki_col2.checkbox(f"中延駅", value=True)
eki_col2.checkbox(f"戸越駅", value=True)
eki_col2.checkbox(f"大森海岸駅", value=True)
eki_col2.checkbox(f"荏原中延駅", value=True)


st.markdown("---")
se90 = st.write(df_final0)
se91 = st.write(df_final0.shape)

st.subheader('(フィルター後のデータ確認用)')


if df_final0.shape[0] > 50:
    df = df_final0[:50]
else:
    df = df_final0
