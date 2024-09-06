import streamlit as st

def run_streamlit_app(chatbot):
    st.title("시험 문제 생성 및 정답 검증 챗봇")
    
    # 사용자로부터 시험 내용을 입력받음
    exam_content = st.text_area("시험 내용을 입력하세요:")
    
    # 버튼 클릭 상태 추적
    if 'generating_question' not in st.session_state:
        st.session_state.generating_question = False

    if st.button("문제 생성", disabled=st.session_state.generating_question):
        if exam_content:
            st.session_state.generating_question = True
            with st.spinner("질문 생성 중..."):
                question = chatbot.ask_question(exam_content)
                st.session_state.generating_question = False
                st.write(f"생성된 문제: {question}")

                # 사용자의 답변 입력
                user_answer = st.text_input("답변을 입력하세요:")
                
                if st.button("답변 확인"):
                    if user_answer:
                        is_correct, correct_answer = chatbot.evaluate_user_answer(user_answer)
                        if is_correct:
                            st.write("정답입니다!")
                        else:
                            st.write(f"오답입니다. 정답은: {correct_answer}")
        else:
            st.warning("시험 내용을 입력해 주세요.")
