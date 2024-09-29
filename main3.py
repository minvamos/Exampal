from chatbot import *
from streamlit_app import run_streamlit_app
from gemma_model import load_gemma_model
from config.settings import HUGGINGFACE_API_TOKEN
import huggingface_hub
import streamlit as st


if __name__ == "__main__":
    # # HuggingFace 로그인
    # huggingface_hub.login()

    # Gemma 모델 로드
    print('모델 로드하는 중...')
    print('='*50)
    model = load_gemma_model()

    # 챗봇 초기화
    print('챗봇 초기화하는 중...')
    print('='*50)
    chatbot = init_chatbot(model)

    ############ Streamlit 앱 실행
    print('streamlit 앱 실행!')
    print('='*50)

    st.title("시험 문제 생성 및 정답 검증 챗봇")

    # 대화 내역 초기화
    if "chat_session" not in st.session_state:    
        st.session_state["chat_session"] = []

    # 대화 내역 출력
    for content in st.session_state.chat_session:
        with st.chat_message("ai" if content['role'] == "model" else "user"):
            st.markdown(content['text'])

    # 모델이 답변을 해야하는 상황인지 아닌지?
    if 'generating_question' not in st.session_state:
        st.session_state.generating_question = False

    # 메시지 입력
    if "prompt" not in st.session_state:
        st.session_state["prompt"] = None

    if st.session_state["prompt"] is None: # 메시지 입력을 기다림
        st.session_state["prompt"] = st.chat_input("메시지를 입력하세요.")
        
    if st.session_state["prompt"]: # 사용자가 입력을 하면 다음 단계로 진행
        st.session_state.generating_question = True
        with st.chat_message("user"):
            st.markdown(st.session_state["prompt"])
        st.session_state["chat_session"].append({"role": "user", "text": st.session_state["prompt"]})
    
    # ai
    if st.session_state.generating_question:
        with st.chat_message("ai"):
            message_placeholder = st.empty() # DeltaGenerator 반환
            with st.spinner("메시지 처리 중입니다."):
                response = chatbot.ask_question(st.session_state["prompt"])
                st.session_state["prompt"] = None
                st.markdown(response)
            st.session_state["chat_session"].append({"role":"ai", "text":response})
        st.session_state.generating_question = False