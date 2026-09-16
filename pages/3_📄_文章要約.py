import streamlit as st

from utils.gemini_client import generate_text
from utils.ui import render_sidebar

st.set_page_config(page_title="文章要約", page_icon="📄", layout="wide")
render_sidebar()

st.title("📄 文章要約")
st.write("長い文章を貼り付けると、指定した形式・長さで要約します。")

uploaded_file = st.file_uploader("テキストファイルをアップロード（任意）", type=["txt", "md"])
default_text = ""
if uploaded_file is not None:
    default_text = uploaded_file.read().decode("utf-8", errors="ignore")

with st.form("summarize_form"):
    source_text = st.text_area("要約したい文章", value=default_text, height=280)

    col1, col2 = st.columns(2)
    with col1:
        summary_length = st.selectbox("要約の長さ", ["一言で（1文）", "短め（3行程度）", "標準（5〜7行）", "詳しく（元の1/3程度）"])
    with col2:
        summary_format = st.radio("出力形式", ["箇条書き", "文章"], horizontal=True)

    submitted = st.form_submit_button("要約する", type="primary")

if submitted:
    if not source_text.strip():
        st.error("要約したい文章を入力してください。")
    else:
        prompt = (
            "あなたは優秀な編集者です。以下の文章を日本語で要約してください。\n"
            f"- 要約の長さ: {summary_length}\n"
            f"- 出力形式: {summary_format}\n"
            "- 元の文章の重要なポイントや数値、固有名詞は落とさないようにしてください。\n\n"
            "【要約対象の文章】\n"
            f"{source_text}"
        )

        try:
            with st.spinner("要約しています..."):
                result = generate_text(prompt, temperature=0.3)
        except Exception as e:
            st.error(f"生成に失敗しました: {e}")
        else:
            st.subheader("要約結果")
            st.markdown(result)
            st.download_button(
                "テキストでダウンロード",
                data=result,
                file_name="summary.txt",
                mime="text/plain",
            )
