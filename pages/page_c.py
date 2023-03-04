import streamlit as st
import pandas as pd
import plotly.express as px
from matplotlib import pyplot as plt
import japanize_matplotlib
from joblib import load
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error as MSE

japanize_matplotlib.japanize()

# セッションステートを取得
state = st.session_state

if "df" not in state:
    state.df = pd.DataFrame()

if "df_map" not in state:
    state.df_map = pd.DataFrame()

df_map_0 = state.df_map
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

st.title("おススメ物件比較")
st.markdown("---")

image_col, info_col, sele_col = st.columns([2, 3, 2], gap="medium")
image_col.image(f"{df_map_0['画像']}", use_column_width=True)
se90 = info_col.write(df_map_0)

st.markdown("---")
text_col5, gra_col5 = st.columns([1, 2], gap="medium")

if text_col5.button('物件おススメ診断'):
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
    gra_col5.plotly_chart(fig5, use_container_width=True)
    pred0 = pd.DataFrame(pred, columns=['pred'])
    y_test = y_test.reset_index(drop=True)
    pd_recc = pd.concat([df_select0, pred0], axis=1)
    pd_recc['お得度'] = pd_recc['pred'] - pd_recc['家賃[万円]']

    # ----------------------------------------------


else:
    st.write('予測・比較グラフを出すには、ボタンを押してね。')

st.markdown("---")

y0 = pd_recc[pd_recc['ID'] == df_map_0['ID']]['お得度']
y1 = round(y0[0], 1)
se90 = text_col5.subheader(f"家賃 {y1} 万円お得")

pd_recc_comp = pd_recc[:df_select.shape[0]]
pd_recc_comp = pd_recc_comp.sort_values(by="お得度", ascending=False)

se90 = st.subheader("お得物件の表示")
se90 = st.write(pd_recc_comp.head(5))
