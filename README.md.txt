# 🎭 역할 기반 AI 챗봇 (Role-based Streamlit Chatbot)

이 프로젝트는 Streamlit과 OpenAI API를 사용하여 특정 페르소나(역할)를 가진 AI와 대화할 수 있는 간단한 챗봇 애플리케이션입니다.

## 🛠️ 사용 기술

* **프론트엔드/UI:** Streamlit (Python)
* **백엔드/AI:** OpenAI API (GPT-3.5)

## 🚀 배포 준비 사항

**🚨 중요:** API 키는 절대 GitHub에 올리지 마세요.

1.  **API 키 발급:** OpenAI에서 `sk-`로 시작하는 API 키를 발급받으세요.
2.  **Streamlit Cloud Secrets 설정:** 앱 배포 시 **'Secrets'** 설정에 다음 형식으로 키를 입력합니다.
    ```
    [openai]
    api_key = "발급받은 실제 API 키"
    ```
3.  **라이브러리 확인:** `requirements.txt`에 `streamlit`과 `openai==1.14.3`가 있는지 확인합니다.