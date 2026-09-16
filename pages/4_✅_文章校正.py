import streamlit as st

from utils.gemini_client import generate_text
from utils.ui import render_sidebar

st.set_page_config(page_title="文章校正", page_icon="✅", layout="wide")
render_sidebar()

st.title("✅ 文章校正")
st.write("文章を貼り付けると、誤字脱字や表現をチェックし、修正案と変更点の説明を提示します。")

with st.form("proofread_form"):
    source_text = st.text_area("校正したい文章", height=280)
    check_points = st.multiselect(
        "チェック観点",
        ["誤字脱字", "文法・助詞の誤り", "敬語・言葉遣い", "分かりやすさ・簡潔さ", "論理の一貫性"],
        default=["誤字脱字", "文法・助詞の誤り", "敬語・言葉遣い"],
    )
    submitted = st.form_submit_button("校正する", type="primary")

if submitted:
    if not source_text.strip():
        st.error("校正したい文章を入力してください。")
    elif not check_points:
        st.error("チェック観点を1つ以上選択してください。")
    else:
        prompt = (
            "あなたはプロの校正者です。以下の文章を校正してください。\n"
            f"チェック観点: {', '.join(check_points)}\n\n"
            "出力は次の2つのセクションに分けてください。\n"
            "1. 「## 修正後の文章」: 修正を反映した文章全文\n"
            "2. 「## 主な変更点」: どこをどう直したか、箇条書きで簡潔に説明（変更がなければ「特に修正点はありません」と記載）\n\n"
            "【校正対象の文章】\n"
            f"{source_text}"
        )

        try:
            with st.spinner("校正しています..."):
                result = generate_text(prompt, temperature=0.3)
        except Exception as e:
            st.error(f"生成に失敗しました: {e}")
        else:
            st.subheader("校正結果")
            st.markdown(result)
            st.download_button(
                "テキストでダウンロード",
                data=result,
                file_name="proofread_result.txt",
                mime="text/plain",
            )
