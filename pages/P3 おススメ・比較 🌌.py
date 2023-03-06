import streamlit as st
import pandas as pd
import plotly.express as px
from matplotlib import pyplot as plt
import japanize_matplotlib
from joblib import load
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error as MSE
import numpy as np

japanize_matplotlib.japanize()

# セッションステートを取得
state = st.session_state
df_table5 = pd.DataFrame()

if "df" not in state:
    state.df = pd.DataFrame()

if "df_map" not in state:
    state.df_map = pd.DataFrame()

df_map_0 = state.df_map
#df_0 = pd.DataFrame(state.df_map2)
df_select = state.df

df_select0 = df_select.rename(
    columns={'家賃': '家賃[万円]', '面積': '面積[m^2]', '徒歩時間': '駅徒歩時間[分]', 'アクセス': '区'})
df_select0['区'] = "品川"
tx0 = ['家賃[万円]', '面積[m^2]', '築年数', '階数', '駅徒歩時間[分]', '区', '間取り']
tx10 = ['面積[m^2]', '築年数', '階数', '駅徒歩時間[分]', '区', '間取り']
select_columns5 = tx10

################################################################################################################################################
# csvファイルの読み込み
# pd.DataFrame(pre_data[1:], columns=col_name)  # 一段目をカラム、以下データフレームで取得
pre_df = pd.read_csv("realestateinfo_test2_ishida91.csv")
pre_df = pre_df.rename(columns={
                       '面積': '面積[m^2]', '家賃': '家賃[万円]', '敷金': '敷金[万円]', '礼金': '礼金[万円]', '駅徒歩時間': '駅徒歩時間[分]'})
select_columns_num = ['面積[m^2]', '家賃[万円]', '築年数', '階数', '駅徒歩時間[分]']
pre0_df = pre_df[select_columns_num]

# object →　数字の変換 新しくスプシから取得する際には全てObjectになっているため。
for column in pre0_df:
    pre0_df[column] = pd.to_numeric(pre0_df[column], errors='coerce')

pre_df[select_columns_num] = pre0_df

df_select_comp = df_select0[tx0]
df_select_dummy = pre_df[tx0]
df_select_dummy0 = df_select_dummy[:200]

pd_recc0 = pd.concat([df_select_comp, df_select_dummy0])

# -------------------------------------------------------------------------------------

st.title("お得度表示・おススメ物件")
st.markdown("---")
image_col5, text_col5, gra_col5 = st.columns([2, 2, 3], gap="medium")

image_col5.image(f"{df_map_0['画像']}", use_column_width=True)

df_0 = pd.DataFrame(state.df_map2)
text_col5.subheader(f"● {df_0.columns[0]}")
text_col5.dataframe(state.df_map2, width=500, height=458)


# 学習までのデータ準備
test0 = pd_recc0  # 比較用
test0[select_columns5] = test0[select_columns5].fillna(-99)
X_test, y_test = pd.get_dummies(test0[select_columns5]), test0['家賃[万円]']

# 評価データに対する予測を行い、その結果を変数predに代入してください。
rf = load('rf_model-TK-slim.joblib2.cmp')
pred = rf.predict(X_test)

# グラフの可視化
fig5 = px.scatter(x=y_test, y=pred,
                  title="  x軸：家賃[万円]　VS　　y軸：予測家賃[万円]",
                  range_x=[0, 50],
                  range_y=[0, 50],
                  )

pred0 = pd.DataFrame(pred, columns=['pred'])
y_test = y_test.reset_index(drop=True)
pd_recc = pd.concat([df_select0, pred0], axis=1)
pd_recc['お得度'] = pd_recc['pred'] - pd_recc['家賃[万円]']

# ----------------------------------------------

st.markdown("---")
y0 = pd_recc[pd_recc['ID'] == df_map_0['ID']]['お得度']
y1 = round(y0.iloc[0], 1)


se50 = gra_col5.subheader(f"●お得度:家賃 {y1} 万円")
gra_col5.plotly_chart(fig5, use_container_width=True)

pd_recc_comp = pd_recc[:df_select.shape[0]]
pd_recc_comp = pd_recc_comp.sort_values(by="お得度", ascending=False)

se90 = st.subheader("お得物件の表示：")

pd_recc_comp5 = pd_recc_comp.head(5)
pd_recc_comp5 = pd_recc_comp5 .reset_index()

cl1, cl2, cl3, cl4, cl5 = st.columns([1, 1, 1, 1, 1], gap="medium")
cl1.write(f"①{pd_recc_comp5['名称'][0]}")
cl2.write(f"②{pd_recc_comp5['名称'][1]}")
cl3.write(f"③{pd_recc_comp5['名称'][2]}")
cl4.write(f"④{pd_recc_comp5['名称'][3]}")
cl5.write(f"⑤{pd_recc_comp5['名称'][4]}")

cl1, cl2, cl3, cl4, cl5 = st.columns([1, 1, 1, 1, 1], gap="medium")
cl1.write(f"・お得度:{round(pd_recc_comp5['お得度'][0],1)}万円")
cl2.write(f"・お得度:{round(pd_recc_comp5['お得度'][1],1)}万円")
cl3.write(f"・お得度:{round(pd_recc_comp5['お得度'][2],1)}万円")
cl4.write(f"・お得度:{round(pd_recc_comp5['お得度'][3],1)}万円")
cl5.write(f"・お得度:{round(pd_recc_comp5['お得度'][4],1)}万円")

if cl1.button(f"MAP確認.{1}"):
    J = 1
if cl2.button(f"MAP確認.{2}"):
    J = 1
if cl3.button(f"MAP確認.{3}"):
    J = 1
if cl4.button(f"MAP確認.{4}"):
    J = 1
if cl5.button(f"MAP確認.{5}"):
    J = 1

cl1, cl2, cl3, cl4, cl5 = st.columns([1, 1, 1, 1, 1], gap="medium")
for i, row in pd_recc_comp5.iterrows():
    table_index = ["住所", "家賃[万円]", "間取り", "面積[m^2]", '最寄駅',
                   '駅徒歩[分]', '築年数', '階数', '構造', '敷金[万円]', '礼金[万円]', '管理費[万円]', 'お得度[万円]']
    table = [row['アドレス'], row['家賃[万円]'], row['間取り'], row['面積[m^2]'], row['最寄駅'],
             row['駅徒歩時間[分]'], row['築年数'], row['階数'], row['構造'], row['敷金'], row['礼金'], row['管理費'], round(row['お得度'], 1)]

    df_table5[f"物件情報{i+1}"] = pd.DataFrame(
        data=np.array(table), index=table_index
    )

    if i == 0:
        cl1.dataframe(df_table5[f"物件情報{i+1}"], width=500, height=492)
    if i == 1:
        cl2.dataframe(df_table5[f"物件情報{i+1}"], width=500, height=492)
    if i == 2:
        cl3.dataframe(df_table5[f"物件情報{i+1}"], width=500, height=492)
    if i == 3:
        cl4.dataframe(df_table5[f"物件情報{i+1}"], width=500, height=492)
    if i == 4:
        cl5.dataframe(df_table5[f"物件情報{i+1}"], width=500, height=492)
