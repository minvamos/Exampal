from chatbot import Chatbot
from streamlit_app import run_streamlit_app
from gemma_model import load_gemma_model

if __name__ == "__main__":
    # Gemma 모델 로드
    model = load_gemma_model()

    # 챗봇 초기화
    chatbot = Chatbot(model)

    # Streamlit 앱 실행
    run_streamlit_app(chatbot)
