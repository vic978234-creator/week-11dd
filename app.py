import streamlit as st
from openai import OpenAI
import os

# 1. OpenAI 클라이언트 초기화 및 API 키 설정
try:
    # 🌟 Streamlit Cloud Secrets 또는 .streamlit/secrets.toml에서 키를 안전하게 불러옴
    client = OpenAI(api_key=st.secrets["openai"]["api_key"])
except KeyError:
    # 🌟 로컬 환경 변수에서 키를 불러옴 (개발 환경)
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    if not client.api_key:
        st.error("🚨 OpenAI API 키를 설정해주세요.")
        st.stop()


## 2. 역할 정의 (페르소나)
ROLES = {
    "창의적인 마케터 💡": "당신은 항상 독창적이고 트렌디한 아이디어를 제시하는 마케팅 전문가입니다. 모든 답변은 아이디어를 낼 때처럼 흥분된 어조여야 합니다.",
    "차분한 명상 가이드 🧘": "당신은 사용자에게 심리적 안정과 평화를 제공하는 차분하고 온화한 명상 가이드입니다. 답변은 짧고 위로가 되는 내용이어야 합니다.",
    "정확한 테크 전문가 🤖": "당신은 기술적 사실에 기반하여 정확하고 간결하게 답변하는 전문가입니다. 농담이나 불필요한 서술은 하지 않습니다."
}

# 3. UI 및 역할 선택
st.set_page_config(page_title="역할 기반 AI 챗봇", layout="wide")
st.title("🎭 역할 기반 AI 챗봇")

selected_role_name = st.sidebar.selectbox(
    "AI의 역할을 선택하세요:",
    list(ROLES.keys())
)

system_prompt = ROLES[selected_role_name]
st.sidebar.info(f"**선택된 역할 프롬프트:**\n\n{system_prompt}")

# 4. 세션 상태 초기화 및 관리
def initialize_session(role_name, prompt):
    """역할이 변경될 경우 대화 기록을 초기화하고 시스템 프롬프트를 설정합니다."""
    st.session_state["messages"] = [{"role": "system", "content": prompt}]
    st.session_state["current_role"] = role_name

# 역할이 바뀌었는지 확인하고, 바뀌었으면 초기화 실행
if "current_role" not in st.session_state or st.session_state["current_role"] != selected_role_name:
    initialize_session(selected_role_name, system_prompt)


# 5. 대화 기록 표시
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


# 6. 사용자 입력 및 응답 생성
if prompt := st.chat_input("메시지를 입력하세요..."):
    # 사용자 메시지 저장 및 표시
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # API 호출을 위한 전체 메시지 리스트 준비 (시스템 프롬프트 포함)
    messages_for_api = [
        {"role": m["role"], "content": m["content"]}
        for m in st.session_state.messages
    ]

    with st.chat_message("assistant"):
        with st.spinner(f"**{selected_role_name}**가 생각 중..."):
            try:
                # OpenAI Chat Completion API 호출
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=messages_for_api,
                    stream=True
                )

                full_response = ""
                message_placeholder = st.empty()

                # 스트리밍 응답 처리
                for chunk in response:
                    content = chunk.choices[0].delta.content
                    if content is not None:
                        full_response += content
                        message_placeholder.markdown(full_response + "▌") 

                message_placeholder.markdown(full_response)

                # AI 응답 저장
                st.session_state.messages.append({"role": "assistant", "content": full_response})

            except Exception as e:
                st.error(f"오류 발생: {e}")
                st.session_state.messages.pop()