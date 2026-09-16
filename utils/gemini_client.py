"""Gemini APIとの通信をまとめたモジュール。"""
import os

import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import errors as genai_errors
from google.genai import types

load_dotenv()

MODEL_OPTIONS = [
    "gemini-3.8-flash",
    "gemini-3.7-flash",
    "gemini-3.6-flash",
    "gemini-3.5-flash",
    "gemini-3.5-flash-lite",
    "gemini-3.1-pro-preview",
]
DEFAULT_MODEL = "gemini-3.8-flash"


def get_api_key() -> str | None:
    """セッションに入力されたキー、なければ環境変数から取得する。"""
    key = st.session_state.get("gemini_api_key") or os.environ.get("GEMINI_API_KEY")
    return key.strip() if key else key


def get_model() -> str:
    return st.session_state.get("gemini_model", DEFAULT_MODEL)


@st.cache_resource(show_spinner=False)
def _get_client(api_key: str) -> genai.Client:
    # 503(混雑)や429(レート制限)などの一時的なエラーは自動的にリトライする。
    retry_options = types.HttpRetryOptions(
        attempts=5,
        initial_delay=1.0,
        max_delay=20.0,
        exp_base=2,
        http_status_codes=[408, 429, 500, 502, 503, 504],
    )
    return genai.Client(api_key=api_key, http_options=types.HttpOptions(retry_options=retry_options))


def generate_text(prompt: str, system_instruction: str | None = None, temperature: float = 0.7) -> str:
    """Geminiにプロンプトを送り、生成テキストを返す。"""
    api_key = get_api_key()
    if not api_key:
        raise RuntimeError("Gemini APIキーが設定されていません。サイドバーから入力してください。")
    if not api_key.isascii():
        raise RuntimeError(
            "Gemini APIキーに日本語や全角文字など使用できない文字が含まれています。"
            "キーを貼り付ける際に余分な文字（全角スペースなど）が混ざっていないか確認し、"
            "サイドバーで入力し直してください。"
        )

    client = _get_client(api_key)
    config = types.GenerateContentConfig(
        temperature=temperature,
        system_instruction=system_instruction,
    )
    try:
        response = client.models.generate_content(
            model=get_model(),
            contents=prompt,
            config=config,
        )
    except genai_errors.ServerError as e:
        raise RuntimeError(
            "Geminiサーバーが混雑しているため、複数回リトライしましたが生成に失敗しました。"
            "しばらく時間をおくか、サイドバーで別のモデルを選んでもう一度お試しください。"
        ) from e
    except genai_errors.ClientError as e:
        if e.code == 429:
            raise RuntimeError(
                "リクエスト数の上限（レート制限）に達しました。しばらく時間をおいてからお試しください。"
            ) from e
        raise
    return response.text or ""
