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

    # 시험 내용을 입력했는지 안했는지?
    if 'question_exist' not in st.session_state:
        st.session_state.question_exist = False

    # 첫 질문인지 아닌지?
    if 'first_quiz' not in st.session_state:
        st.session_state.first_quiz = True

    # 유저가 답변을 해야되는 상황인지 아닌지?
    if 'user_answer_waiting' not in st.session_state:
        st.session_state.user_answer_waiting = True

    # 모델이 답변을 해야하는 상황인지 아닌지?
    if 'generating_question' not in st.session_state:
        st.session_state.generating_question = False

    # 모델이 피드백을 해야하는 상황인지 아닌지?
    if 'generating_feedback' not in st.session_state:
        st.session_state.generating_feedback = False


    # user : 시험 내용 입력 
    if st.session_state.first_quiz == True:
        if "exam_content" not in st.session_state:
            st.session_state["exam_content"] = None
        if st.session_state["exam_content"] is None: # 시험 내용 입력을 기다림
            st.session_state["exam_content"] = st.chat_input("시험 내용을 입력하세요.")
        if st.session_state["exam_content"]: # 사용자가 입력을 하면 다음 단계로 진행
            st.session_state.question_exist = True
    else:
        st.session_state.generating_question = True

    # ai : 질문 생성
    if (st.session_state.question_exist and st.session_state.first_quiz) or st.session_state.generating_question:
        with st.chat_message("ai"):
            message_placeholder = st.empty() # DeltaGenerator 반환
            with st.spinner("질문 생성 중입니다."):
                quiz = chatbot.ask_question(st.session_state["exam_content"])
                st.markdown(quiz)
            st.session_state["chat_session"].append({"role":"ai", "text":quiz})
        st.session_state.generating_question = False
        st.session_state.first_quiz = False
        st.session_state.user_answer_waiting = True
    

    # user : 답변 입력
    if st.session_state.first_quiz == False and st.session_state.question_exist and st.session_state.user_answer_waiting:
        if "answer" not in st.session_state:
            st.session_state["answer"] = None
        if st.session_state["answer"] is None: # 메시지 입력을 기다림
            st.session_state["answer"] = st.chat_input("메시지를 입력하세요.")
        if st.session_state["answer"]: # 사용자가 입력을 하면 다음 단계로 진행
            st.session_state.generating_feedback = True
            with st.chat_message("user"):
                st.markdown(st.session_state["answer"])
            st.session_state["chat_session"].append({"role": "user", "text": st.session_state["answer"]})
            st.session_state.user_answer_waiting = False
        

    # ai : 피드백 생성
    if st.session_state.generating_feedback:
        with st.chat_message("ai"):
            message_placeholder = st.empty() # DeltaGenerator 반환
            with st.spinner("피드백 생성 중입니다."):
                feedback = chatbot.ask_question(st.session_state["answer"])
                st.markdown(feedback)
            st.session_state["chat_session"].append({"role":"ai", "text":feedback})
            st.session_state["answer"] = None
        st.session_state.generating_feedback = False
        if st.button("문제 생성", disabled=st.session_state.generating_question):
            pass