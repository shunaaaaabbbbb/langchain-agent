import streamlit as st

from agent import create_agent, get_agent_response

st.set_page_config(page_title="LangChain Agent Chat", page_icon="🤖", layout="wide")

st.title("🤖 LangChain Agent Chat")

# セッション状態の初期化
if "agent" not in st.session_state:
    st.session_state.agent = create_agent()
if "messages" not in st.session_state:
    st.session_state.messages = []

# チャット履歴の表示
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ユーザー入力
if prompt := st.chat_input("質問を入力してください"):
    # ユーザーメッセージの追加
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # エージェントの応答
    with st.chat_message("assistant"):
        with st.spinner("考え中..."):
            response = get_agent_response(st.session_state.agent, prompt)
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
