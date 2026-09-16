"""ページ共通のサイドバーUI。"""
import streamlit as st

from .gemini_client import DEFAULT_MODEL, MODEL_OPTIONS, get_api_key


def render_sidebar() -> None:
    with st.sidebar:
        st.header("⚙️ 設定")

        api_key_input = st.text_input(
            "Gemini APIキー",
            type="password",
            value=st.session_state.get("gemini_api_key", ""),
            help="環境変数 GEMINI_API_KEY が設定済みなら空欄のままで構いません。",
        )
        if api_key_input:
            st.session_state["gemini_api_key"] = api_key_input.strip()
            if not api_key_input.strip().isascii():
                st.error(
                    "APIキーに日本語や全角文字が含まれているようです。"
                    "キーの前後に余分な文字が入っていないか確認し、貼り付け直してください。"
                )

        current_model = st.session_state.get("gemini_model", DEFAULT_MODEL)
        model = st.selectbox(
            "使用モデル",
            options=MODEL_OPTIONS,
            index=MODEL_OPTIONS.index(current_model) if current_model in MODEL_OPTIONS else 0,
        )
        st.session_state["gemini_model"] = model

        if get_api_key():
            st.success("APIキー設定済み")
        else:
            st.warning("APIキー未設定です。上欄に入力するか .env に GEMINI_API_KEY を設定してください。")

        st.divider()
        st.caption(
            "個人利用専用のローカルアプリです。入力したAPIキーはブラウザセッション内でのみ保持され、"
            "外部やサーバーには保存されません。"
        )
