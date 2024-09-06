from transformers import AutoTokenizer, pipeline
from config.settings import HUGGINGFACE_API_TOKEN

def load_gemma_model():
    # Hugging Face에서 Gemma 모델 불러오기
    model_name = "google/gemma-2b"
    
    # 토크나이저 생성
    tokenizer = AutoTokenizer.from_pretrained(model_name, return_token_type_ids=False)
    
    # 모델과 토크나이저를 사용하여 파이프라인 생성
    gemma_pipeline = pipeline(
        "text-generation", 
        model=model_name, 
        tokenizer=tokenizer,
        device=0 
    )
    
    return gemma_pipeline
