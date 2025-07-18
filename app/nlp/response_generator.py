import os
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, GenerationConfig
from safetensors.torch import load_file as safe_load
from app.config import Config

# Paths
BASE_MODEL_DIR = os.path.join(Config.BASE_DIR, 'models', 'deepseek_r1_distill_qwen_7b')
PEFT_MODEL_DIR = os.path.join(Config.BASE_DIR, 'models', 'train_2025-07-14-14-05-13')

# Device
device = 'cuda' if torch.cuda.is_available() else 'cpu'

def load_model(base_dir: str, peft_dir: str):

    # 1. 加载基础模型
    model = AutoModelForCausalLM.from_pretrained(
        base_dir,
        trust_remote_code=True,
        torch_dtype=torch.float16 if device=='cuda' else torch.float32,
        device_map='auto'
    )
    # 2. 查找 LoRA 权重文件 (.bin, .pt, .safetensors)
    weight_path = None
    for fname in ('adapter_model.safetensors', 'adapter_model.bin', 'pytorch_model.bin', 'pytorch_model.pt'):
        p = os.path.join(peft_dir, fname)
        if os.path.exists(p):
            weight_path = p
            break
    if weight_path is None:
        raise FileNotFoundError(f"在 {peft_dir} 中未找到 LoRA 权重文件 (.safetensors/.bin/.pt)")

    # 3. 加载权重
    if weight_path.endswith('.safetensors'):
        peft_weights = safe_load(weight_path, device=device)
    else:
        peft_weights = torch.load(weight_path, map_location=device)

    # 4. 清理前缀并注入模型
    new_state = {}
    for k, v in peft_weights.items():
        # 常见前缀
        nk = k
        for prefix in ('base_model.model.model.', 'base_model.', 'model.model.model.', 'model.'):  
            if nk.startswith(prefix):
                nk = nk[len(prefix):]
                break
        new_state[nk] = v
    # 仅加载匹配的参数
    model.load_state_dict(new_state, strict=False)
    model.eval()
    return model


def load_tokenizer(base_dir: str):
    tokenizer = AutoTokenizer.from_pretrained(
        base_dir,
        trust_remote_code=True,
        use_fast=False
    )
    return tokenizer


def build_prompt(history):
    prompt = ""
    for message in history:
        if message['role'] == 'user':
            prompt += f"### 用户: {message['content']}\n"
        else:
            prompt += f"### 模型: {message['content']}\n"
    prompt += "### 模型:"
    return prompt


def chat(model, tokenizer, history, max_new_tokens=512, temperature=0.8, top_p=0.9):

    history.append({'role': 'assistant', 'content': None})
    prompt = build_prompt(history[:-1])
    inputs = tokenizer(
        prompt,
        return_tensors='pt'
    ).to(device)

    generation_config = GenerationConfig(
        temperature=temperature,
        top_p=top_p,
        max_new_tokens=max_new_tokens,
        do_sample=True,
        pad_token_id=tokenizer.eos_token_id
    )

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            **generation_config.__dict__
        )

    response = tokenizer.decode(
        outputs[0][inputs['input_ids'].shape[-1]:],
        skip_special_tokens=True
    ).strip()

    history[-1]['content'] = response
    return response


# if __name__ == '__main__':
#     model = load_model(BASE_MODEL_DIR, PEFT_MODEL_DIR)
#     tokenizer = load_tokenizer(BASE_MODEL_DIR)
#
#     history = []
#     print("开始对话，输入 '退出' 以结束")
#     while True:
#         user_input = input("用户: ")
#         if user_input.lower() in ['退出', 'exit', 'quit']:
#             break
#         history.append({'role': 'user', 'content': user_input})
#         reply = chat(model, tokenizer, history)
#         print(f"模型: {reply}\n")
