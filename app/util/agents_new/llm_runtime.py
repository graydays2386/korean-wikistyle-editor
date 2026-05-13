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
        print("Model:", model_id)
        self.processor = AutoProcessor.from_pretrained(model_id)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_id,
            quantization_config=quantization_config,
            device_map={"": 0},
        )
        print("모델 4bit 퀀텀화 완료")

    def generate_chat(
        self,
        messages: list[dict],
        max_new_tokens: int = 1024,
        temperature: float = 0.0,
        top_p: float = 1.0,
        do_sample: bool = False,
    ) -> str:
        formatted_prompt = self.processor.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True,
        )

        inputs = self.processor(
            text=formatted_prompt,
            return_tensors="pt",
        ).to(self.model.device)

        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=max_new_tokens,
                temperature=temperature,
                top_p=top_p,
                do_sample=do_sample,
            )

        input_length = inputs.input_ids.shape[1]
        response = self.processor.decode(
            outputs[0][input_length:],
            skip_special_tokens=True,
        )

        return response.strip()