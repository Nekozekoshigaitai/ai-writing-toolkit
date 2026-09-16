import streamlit as st

from utils.gemini_client import generate_text
from utils.ui import render_sidebar

st.set_page_config(page_title="メール返信作成", page_icon="✉️", layout="wide")
render_sidebar()

st.title("✉️ メール返信作成")
st.write("受信したメールと返信で伝えたい内容を入力すると、返信文の下書きを生成します。")

with st.form("email_form"):
    original_email = st.text_area("受信したメールの本文", height=200, placeholder="相手から届いたメールをそのまま貼り付けてください")
    key_points = st.text_area("返信で伝えたいこと", height=120, placeholder="例: 提案は魅力的だが予算が合わないので来月改めて相談したい")

    col1, col2 = st.columns(2)
    with col1:
        tone = st.selectbox("トーン", ["ビジネスフォーマル", "丁寧", "カジュアル・親しみやすい"])
    with col2:
        language = st.selectbox("言語", ["日本語", "英語"])

    sender_name = st.text_input("署名に使う名前（任意）", placeholder="例: 山田")

    submitted = st.form_submit_button("返信文を生成する", type="primary")

if submitted:
    if not original_email.strip() or not key_points.strip():
        st.error("受信メールの本文と、伝えたい内容の両方を入力してください。")
    else:
        prompt_parts = [
            "あなたは優秀なビジネスアシスタントです。以下の受信メールに対する返信メールの下書きを作成してください。",
            f"- 返信の言語: {language}",
            f"- トーン: {tone}",
            "",
            "【受信メール】",
            original_email,
            "",
            "【返信で伝えたい内容】",
            key_points,
        ]
        if sender_name.strip():
            prompt_parts.append(f"\n署名には「{sender_name}」という名前を使ってください。")
        prompt_parts.append("\n件名と本文を含む、そのまま送れる形式で出力してください。")

        prompt = "\n".join(prompt_parts)

        try:
            with st.spinner("返信文を生成しています..."):
                result = generate_text(prompt, temperature=0.6)
        except Exception as e:
            st.error(f"生成に失敗しました: {e}")
        else:
            st.subheader("生成結果")
            st.text_area("返信文", value=result, height=300)
            st.download_button(
                "テキストでダウンロード",
                data=result,
                file_name="email_reply.txt",
                mime="text/plain",
            )
