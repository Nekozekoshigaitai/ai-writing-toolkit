import streamlit as st

from utils.gemini_client import generate_text
from utils.ui import render_sidebar

st.set_page_config(page_title="タイトル案生成", page_icon="💡", layout="wide")
render_sidebar()

st.title("💡 タイトル案生成")
st.write("記事の内容やテーマを入力すると、タイトル候補を複数生成します。")

with st.form("title_form"):
    content = st.text_area(
        "記事のテーマ・概要・本文など",
        height=200,
        placeholder="例: リモートワークで集中力を維持するための5つの習慣について書いた記事",
    )
    num_titles = st.slider("生成するタイトル数", min_value=3, max_value=10, value=5)
    styles = st.multiselect(
        "重視したいスタイル（任意）",
        ["SEOを意識する", "キャッチーで目を引く", "疑問形にする", "数字を入れる", "簡潔・シンプル"],
    )
    submitted = st.form_submit_button("タイトル案を生成する", type="primary")

if submitted:
    if not content.strip():
        st.error("記事のテーマや内容を入力してください。")
    else:
        prompt_parts = [
            "あなたは優秀なコピーライター兼SEOエディターです。以下の内容をもとに、記事のタイトル案を"
            f"{num_titles}個、日本語で考えてください。",
        ]
        if styles:
            prompt_parts.append(f"重視するスタイル: {', '.join(styles)}")
        prompt_parts.append("番号付きの箇条書きで、タイトル案のみを出力してください。")
        prompt_parts.append("\n【記事の内容】")
        prompt_parts.append(content)

        prompt = "\n".join(prompt_parts)

        try:
            with st.spinner("タイトル案を生成しています..."):
                result = generate_text(prompt, temperature=0.9)
        except Exception as e:
            st.error(f"生成に失敗しました: {e}")
        else:
            st.subheader("生成結果")
            st.markdown(result)
