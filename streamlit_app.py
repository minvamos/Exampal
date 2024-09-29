import streamlit as st

def run_streamlit_app(chatbot):
    st.title("시험 문제 생성 및 정답 검증 챗봇")
    
    # 사용자로부터 시험 내용을 입력받음
    exam_content = st.text_area("시험 내용을 입력하세요:")
    
    # 버튼 클릭 상태 추적
    if 'generating_question' not in st.session_state:
        st.session_state.generating_question = False
    if 'user_answer' not in st.session_state:
        st.session_state.user_answer = ""

    if st.button("문제 생성", disabled=st.session_state.generating_question):
        if exam_content:
            st.session_state.generating_question = True
            with st.spinner("질문 생성 중..."):
                question = chatbot.ask_question(exam_content)
                st.session_state.generating_question = False
                st.write(f"생성된 문제: {question}")

                # 사용자의 답변 입력
                st.session_state.user_answer = st.text_input("답변을 입력하세요:", value=st.session_state.user_answer)
                
                if st.button("답변 확인"):
                    if st.session_state.user_answer:
                        with st.spinner("정답 확인 중..."):  # 대기 스피너 추가
                            is_correct, correct_answer = chatbot.evaluate_user_answer(st.session_state.user_answer)
                            
                        # 정답 여부 출력
                        if is_correct:
                            st.write("정답입니다!")
                        else:
                            st.write(f"오답입니다. 정답은: {correct_answer}")
        else:
            st.warning("시험 내용을 입력해 주세요.")
