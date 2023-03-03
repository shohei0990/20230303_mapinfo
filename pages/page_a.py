import streamlit as st
import pandas as pd

# セッションステートを取得
state = st.session_state

if "df" not in state:
    state.df = pd.DataFrame()

st.title('賃貸情報')
st.markdown("---")

df_select = state.df
df_select_image = df_select[:20]

image_col, info_col, sele_col = st.columns([2, 3, 2], gap="medium")
info_col.subheader(f"● {df_select_image['名称'][0]}")
image_col.image(f"{df_select_image ['画像'][0]}", use_column_width=True)

# st.write(m_data)
info_col.text(f"住所　：{df_select_image['アドレス'][0]}")
info_col.text(f"家賃　：{df_select_image['家賃'][0]}")
info_col.text(f"間取り：{df_select_image['間取り'][0]}")
info_col.text(f"面積　：{df_select_image['面積'][0]}")
info_col.text(f"最寄駅：{df_select_image['最寄駅'][0]}")
info_col.text(f"最寄駅：{df_select_image['徒歩時間'][0]}")
info_col.text(f"築年数：{df_select_image['築年数'][0]}")
info_col.text(f"階数　：{df_select_image['階数'][0]}")
info_col.text(f"構造　：{df_select_image['構造'][0]}")
info_col.text(f"敷金　：{df_select_image['敷金'][0]}")
info_col.text(f"礼金　：{df_select_image['礼金'][0]}")
info_col.text(f"管理費：{df_select_image['管理費'][0]}")
# info_col.text(f"オススメ度：{df_select['間取り']}")

st.markdown("---")

for i, row in df_select_image.iterrows():
    image_col, info_col, sele_col = st.columns([2, 3, 2], gap="medium")
    info_col.subheader(f"● {row['名称']}")
    image_col.image(f"{row['画像']}", use_column_width=True)

    # st.write(m_data)
    info_col.text(f"住所　：{row['アドレス']}")
    info_col.text(f"家賃　：{row['家賃']}")
    info_col.text(f"間取り：{row['間取り']}")
    info_col.text(f"面積　：{row['面積']}")
    info_col.text(f"最寄駅：{row['最寄駅']}")
    info_col.text(f"最寄駅：{row['徒歩時間']}")
    info_col.text(f"築年数：{row['築年数']}")
    info_col.text(f"階数　：{row['階数']}")
    info_col.text(f"構造　：{row['構造']}")
    info_col.text(f"敷金　：{row['敷金']}")
    info_col.text(f"礼金　：{row['礼金']}")
    info_col.text(f"管理費：{row['管理費']}")
    # info_col.text(f"オススメ度：{df_select['間取り']}")

    if sele_col.button(f"MAP確認{i}"):
        state.df_map = row

    st.markdown("---")

se90 = st.write(state.df)
se91 = st.write(state.df.shape)
