from chatbot import *
from streamlit_app import run_streamlit_app
from gemma_model import load_gemma_model
from config.settings import HUGGINGFACE_API_TOKEN
import huggingface_hub
import streamlit as st


if __name__ == "__main__":
    # HuggingFace 로그인
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

    # 상태 기록 변수
    if 'status' not in st.session_state:
        st.session_state.status = 0


    # user : 시험 내용 입력
    if st.session_state.status == 0:
        if "exam_content" not in st.session_state:
            st.session_state["exam_content"] = None
        if st.session_state["exam_content"] is None: # 시험 내용 입력을 기다림
            st.session_state["exam_content"] = st.chat_input("시험 내용을 입력하세요.")
        if st.session_state["exam_content"]: # 사용자가 입력을 하면 다음 단계로 진행
            st.session_state["chat_session"].append({"role":"user", "text":st.session_state["exam_content"]})
            st.session_state.status = 1
    

    # ai : 질문 생성
    if st.session_state.status == 1:
        with st.chat_message("ai"):
            message_placeholder = st.empty() # DeltaGenerator 반환
            with st.spinner("질문 생성 중입니다."):
                quiz = chatbot.ask_question(st.session_state["exam_content"])
                st.markdown(quiz)
            st.session_state["chat_session"].append({"role":"ai", "text":quiz})
        st.session_state.status = 2
    

    # user : 답변 입력
    if st.session_state.status == 2:
        if "answer" not in st.session_state:
            st.session_state["answer"] = None
        if st.session_state["answer"] is None: # 메시지 입력을 기다림
            st.session_state["answer"] = st.chat_input("문제에 답하시오.")
        if st.session_state["answer"]: # 사용자가 입력을 하면 다음 단계로 진행
            with st.chat_message("user"):
                st.markdown(st.session_state["answer"])
            st.session_state["chat_session"].append({"role": "user", "text": st.session_state["answer"]})
            st.session_state.status = 3
        

    # ai : 피드백 생성
    if st.session_state.status == 3:
        with st.chat_message("ai"):
            message_placeholder = st.empty() # DeltaGenerator 반환
            with st.spinner("피드백 생성 중입니다."):
                feedback = chatbot.ask_question(st.session_state["answer"])
                st.markdown(feedback)
            st.session_state["chat_session"].append({"role":"ai", "text":feedback})
            st.session_state["answer"] = None
        st.session_state.status = 4
        if st.button("문제 생성"):
            pass