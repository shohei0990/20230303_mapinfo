import streamlit as st
import pandas as pd

# セッションステートを取得
state = st.session_state

if "df" not in state:
    state.df = pd.DataFrame()

st.title('賃貸一覧')
st.markdown("---")

df_select = state.df
df_select_image = df_select[:20]

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
