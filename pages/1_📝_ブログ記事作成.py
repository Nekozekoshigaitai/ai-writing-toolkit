import streamlit as st

from utils.gemini_client import generate_text
from utils.ui import render_sidebar

st.set_page_config(page_title="ブログ記事作成", page_icon="📝", layout="wide")
render_sidebar()

st.title("📝 ブログ記事作成")
st.write("テーマや条件を入力すると、ブログ記事の下書きを生成します。")

with st.form("blog_form"):
    topic = st.text_input("記事のテーマ・タイトル案", placeholder="例: 在宅勤務の生産性を上げる5つの習慣")
    audience = st.text_input("想定読者（任意）", placeholder="例: 20代の会社員、副業に興味がある人")

    col1, col2 = st.columns(2)
    with col1:
        tone = st.selectbox("文体・トーン", ["丁寧・解説調", "フレンドリー", "専門的・硬め", "カジュアル"])
    with col2:
        length = st.selectbox("記事の長さ", ["短め（600字程度）", "標準（1200字程度）", "長め（2000字程度）"])

    keywords = st.text_input("含めたいキーワード（任意・カンマ区切り）", placeholder="例: リモートワーク, 集中力, タイムマネジメント")
    outline_only = st.checkbox("まず見出し構成（アウトライン）だけ生成する")
    extra_instructions = st.text_area("その他の指示（任意）", placeholder="例: 結論を先に書く、体験談を交える、など")

    submitted = st.form_submit_button("生成する", type="primary")

if submitted:
    if not topic.strip():
        st.error("記事のテーマを入力してください。")
    else:
        prompt_parts = [
            "あなたはプロのブログライターです。以下の条件に沿って日本語でブログ記事を書いてください。",
            f"- テーマ: {topic}",
        ]
        if audience.strip():
            prompt_parts.append(f"- 想定読者: {audience}")
        prompt_parts.append(f"- 文体・トーン: {tone}")
        prompt_parts.append(f"- 長さ: {length}")
        if keywords.strip():
            prompt_parts.append(f"- 含めたいキーワード: {keywords}")
        if extra_instructions.strip():
            prompt_parts.append(f"- その他の指示: {extra_instructions}")

        if outline_only:
            prompt_parts.append("- 出力形式: 本文ではなく、見出し（H2/H3）構成のアウトラインのみをMarkdownの箇条書きで出力してください。")
        else:
            prompt_parts.append(
                "- 出力形式: Markdown形式。タイトル（H1）、導入文、見出し（H2/H3）付きの本文、まとめの順で構成してください。"
            )

        prompt = "\n".join(prompt_parts)

        try:
            with st.spinner("記事を生成しています..."):
                result = generate_text(prompt, temperature=0.8)
        except Exception as e:
            st.error(f"生成に失敗しました: {e}")
        else:
            st.subheader("生成結果")
            st.markdown(result)
            st.download_button(
                "Markdownでダウンロード",
                data=result,
                file_name="blog_draft.md",
                mime="text/markdown",
            )
