import torch
from transformers import AutoProcessor, AutoModelForCausalLM, BitsAndBytesConfig

class Gemma4Env:
    def __init__(self):
        # 4비트 양자화 설정 적용
        quantization_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_compute_dtype=torch.float16,
            bnb_4bit_use_double_quant=True,
            bnb_4bit_quant_type="nf4"
        )
        
        model_id = "google/gemma-4-E4B-it"
        
        # 프로세서 및 모델 로드 (전체 모델을 0번 GPU에 강제 할당)
        self.processor = AutoProcessor.from_pretrained(model_id)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_id,
            quantization_config=quantization_config,
            device_map={"": 0} 
        )

    def process_text(self, text: str) -> str:
        # 모델 추론을 위한 프롬프트 구성
        messages = [
            {"role": "user", "content": f"다음 한국어 텍스트를 자연스러운 문장 단위로 분리해 주세요. 부가적인 설명이나 인사말 없이 분리된 결과만 출력하십시오.\n\n텍스트: {text}"}
        ]
        
        formatted_prompt = self.processor.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True
        )
        
        inputs = self.processor(text=formatted_prompt, return_tensors="pt").to(self.model.device)
        
        # 텍스트 생성 추론 실행
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=1024,
                temperature=0.1,
                top_p=0.95,
                do_sample=True
            )
        
        # 결과 디코딩 및 반환
        input_length = inputs.input_ids.shape[1]
        response = self.processor.decode(outputs[0][input_length:], skip_special_tokens=True)
        
        return response.strip()