import streamlit as st

from utils.gemini_client import generate_text
from utils.ui import render_sidebar

st.set_page_config(page_title="翻訳", page_icon="🌐", layout="wide")
render_sidebar()

st.title("🌐 翻訳")
st.write("文章を貼り付けると、指定した言語・トーンに翻訳します。")

LANGUAGES = ["日本語", "英語", "中国語（簡体字）", "韓国語", "フランス語", "スペイン語", "ドイツ語"]

with st.form("translate_form"):
    source_text = st.text_area("翻訳したい文章", height=250)

    col1, col2, col3 = st.columns(3)
    with col1:
        source_lang = st.selectbox("翻訳元の言語", ["自動検出"] + LANGUAGES)
    with col2:
        target_lang = st.selectbox("翻訳先の言語", LANGUAGES, index=1)
    with col3:
        style = st.selectbox("トーン", ["標準", "フォーマル・ビジネス", "カジュアル"])

    submitted = st.form_submit_button("翻訳する", type="primary")

if submitted:
    if not source_text.strip():
        st.error("翻訳したい文章を入力してください。")
    else:
        source_desc = "自動的に言語を判定し、" if source_lang == "自動検出" else f"{source_lang}から"
        prompt = (
            f"あなたはプロの翻訳者です。{source_desc}以下の文章を{target_lang}に翻訳してください。\n"
            f"トーン: {style}\n"
            "自然で、原文のニュアンスを損なわない訳文にしてください。翻訳結果のみを出力し、説明や前置きは不要です。\n\n"
            "【翻訳対象の文章】\n"
            f"{source_text}"
        )

        try:
            with st.spinner("翻訳しています..."):
                result = generate_text(prompt, temperature=0.3)
        except Exception as e:
            st.error(f"生成に失敗しました: {e}")
        else:
            st.subheader("翻訳結果")
            st.text_area("結果", value=result, height=250)
            st.download_button(
                "テキストでダウンロード",
                data=result,
                file_name="translation.txt",
                mime="text/plain",
            )
