from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

model_name = "microsoft/DialoGPT-medium"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

chat_history_ids = None
MAX_HISTORY_LENGTH = 1000

def reset_history():
    global chat_history_ids
    chat_history_ids = None

def chat_with_gf(prompt: str) -> str:
    global chat_history_ids

    new_input_ids = tokenizer.encode(prompt + tokenizer.eos_token, return_tensors='pt')

    if chat_history_ids is not None:
        bot_input_ids = torch.cat([chat_history_ids, new_input_ids], dim=-1)
        if bot_input_ids.shape[-1] > MAX_HISTORY_LENGTH:
            bot_input_ids = bot_input_ids[:, -MAX_HISTORY_LENGTH:]  
    else:
        bot_input_ids = new_input_ids

    chat_history_ids = model.generate(
        bot_input_ids,
        max_length=MAX_HISTORY_LENGTH,
        pad_token_id=tokenizer.eos_token_id
    )

    response = tokenizer.decode(
        chat_history_ids[:, bot_input_ids.shape[-1]:][0],
        skip_special_tokens=True
    )

    return response