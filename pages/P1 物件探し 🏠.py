import streamlit as st
import pandas as pd
import numpy as np

# セッションステートを取得
state = st.session_state

if "df" not in state:
    state.df = pd.DataFrame()

st.title('賃貸一覧')
st.markdown("---")

# ページ処理
df_select = state.df
df_select_image1 = df_select
page_num_max = 1 + (df_select.shape[0] // 20)
# range関数で0からi-1までの整数を生成し、list関数でリストに変換する
j = list(range(page_num_max))
# リストの先頭に1を加える
j = [x + 1 for x in j]
sele_fil = ['-', '家賃 : 安い順', '家賃 : 高い順',
            '面積：小さい順', '面積 : 大きい順', '駅徒歩 : 近い順', '駅徒歩 : 遠い順']

in1_col, in2_col, in3_col = st.columns([1, 1, 1], gap="medium")
in1_col.subheader(f"物件ヒット数 {df_select.shape[0]}件:")
in3_col.subheader(f"並び変え:")
option = in3_col.selectbox('選択して下さい', sele_fil)
st.markdown("---")

df_select_image0 = df_select_image1
if(option == '-'):
    df_select_image0 = df_select_image1
if(option == '家賃 : 安い順'):
    df_select_image0 = df_select_image1.sort_values(
        '家賃', ascending=True)  # False
if(option == '家賃 : 高い順'):
    df_select_image0 = df_select_image1.sort_values(
        '家賃', ascending=False)  # False
if(option == '面積：小さい順'):
    df_select_image0 = df_select_image1.sort_values(
        '面積', ascending=True)  # False
if(option == '面積 : 大きい順'):
    df_select_image0 = df_select_image1.sort_values(
        '面積', ascending=False)  # False
if(option == '駅徒歩 : 近い順'):
    df_select_image0 = df_select_image1.sort_values(
        '徒歩時間', ascending=True)  # False
if(option == '駅徒歩 : 遠い順'):
    df_select_image0 = df_select_image1.sort_values(
        '徒歩時間', ascending=False)  # False

in2_col.subheader(f"ページ選択:")
option = in2_col.selectbox('ページ番号を選んで下さい', j)
if(df_select.shape[0] > 20*(option)):
    in1_col.subheader(f"{20*(option-1)+1} ~ {20*(option)}件の表示")
    df_select_image = df_select_image0[20*(option-1):20*(option)-1]
else:
    in1_col.subheader(f"{20*(option-1)+1} ~ {df_select.shape[0]}件の表示")
    df_select_image = df_select_image0[20*(option-1):]
#df_select_image = df_select[:20]

df_table = pd.DataFrame()
# 20件以下はそのまま
# 20件以上 st.write(df_final0.shape)

for i, row in df_select_image.iterrows():
    image_col, info_col, sele_col = st.columns([2, 3, 2], gap="medium")
    info_col.subheader(f"● {row['名称']}")
    image_col.image(f"{row['画像']}", use_column_width=True)

    # st.write(m_data)

    table_index = ["住所", "家賃[万円]", "間取り", "面積[m^2]", '最寄駅',
                   '徒歩時間[分]', '築年数', '階数', '構造', '敷金[万円]', '礼金[万円]', '管理費[万円]']
    table = [row['アドレス'], row['家賃'], row['間取り'], row['面積'], row['最寄駅'],
             row['徒歩時間'], row['築年数'], row['階数'], row['構造'], row['敷金'], row['礼金'], row['管理費']]

    df_table[f"{row['名称']}"] = pd.DataFrame(
        data=np.array(table), index=table_index
    )

    info_col.dataframe(df_table[f"{row['名称']}"], width=500, height=458)

    sele_col.subheader("●周辺施設")
    if sele_col.button(f"MAP確認.{i}"):
        state.df_map  = row
        state.df_map2 = df_table[f"{row['名称']}"]
        se50 = sele_col.write('➡➡➡   P2 地図確認のページに進んでください！')

    st.markdown("---")

se90 = st.write(state.df)
se91 = st.write(state.df.shape)
