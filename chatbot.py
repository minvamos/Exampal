from transformers import pipeline  # Hugging Face의 pipeline을 사용
import torch  # 필요 시 GPU/CPU 체크 또는 텐서 연산에 사용 가능
import streamlit as st

# 홀로코스트 또는 쇼아는 아돌프 히틀러의 나치 독일이 주도하고 그 협력자들이 동참하여 벌인 유대인에 대한 제노사이드를 뜻한다
class Chatbot:
    def __init__(self, model):
        self.model = model
        self.history = []

    def add_to_history(self, role, message):
        """
        역할에 따라 사용자의 입력 또는 모델의 응답을 기록.
        """
        if role == "user":
            self.history.append(f"<start_of_turn>user\n{message}<end_of_turn>\n")
        else:
            self.history.append(f"<start_of_turn>model\n{message}<end_of_turn>\n")

    def get_full_history(self):
        """
        대화 히스토리를 반환.
        """
        return "".join(self.history)

    def ask_question(self, exam_content):
        """
        시험 내용을 기반으로 Gemma 모델로 질문 생성.
        """
        prompt_template = """You are a teacher. Make a quiz based on what's in here.

        Context:
        {}
        
        Please distribute the questions appropriately among the content provided and ensure that a total of 8 questions are generated, not more or less than 8, just 8.
        """

        prompt = f"{prompt_template.format(exam_content)}"
        print(f"Prompt: {prompt}")
        print('-'*50)
        # TextGenerationPipeline은 텍스트만 반환함으로 딕셔너리 형태가 아님
        generated_output = self.model(prompt, max_length=300, truncation=True)
        print(f"Generated Output: {generated_output}")
        print('-'*50)
        model_question = generated_output[0]['generated_text'][len(prompt):]
        self.add_to_history("model", model_question)
        return model_question

    def evaluate_user_answer(self, user_answer):
        """
        사용자의 답변을 받아 Gemma 모델로 정답 여부 검증.
        """
        correct_answer_prompt = "Provide the correct answer based on the previous question."
        
        # 모델을 사용해 정답을 생성
        correct_answer = self.model(correct_answer_prompt, max_length=100)
        print(correct_answer)
        print('-'*50)

        # 간단한 유사도 검증 로직 추가 가능
        is_correct = self.check_similarity(user_answer, correct_answer[0]['generated_text'])
        
        self.add_to_history("model", correct_answer[0]['generated_text'])
        return is_correct, correct_answer[0]['generated_text']

    def check_similarity(self, user_answer, correct_answer):
        """
        사용자의 답변과 정답 간의 유사도를 체크하는 함수.
        간단한 문자열 비교 방식이거나, 임베딩을 사용할 수 있음.
        """
        return user_answer.strip().lower() == correct_answer.strip().lower()


@st.cache_resource
def init_chatbot(_model):
    chatbot = Chatbot(_model)
    return chatbot