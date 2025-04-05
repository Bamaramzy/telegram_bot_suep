from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

model_name = "microsoft/DialoGPT-medium"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

chat_history_ids = None
MAX_HISTORY_TOKENS = 800

def chat_with_gf(prompt: str) -> str:
    global chat_history_ids

    if prompt.lower() in ["reset", "clear", "new chat"]:
        chat_history_ids = None
        return "Alright! Let's start fresh ❤️"

    system_prompt = "You are a loving, caring, sweet, and romantic virtual girlfriend. "
    full_prompt = system_prompt + prompt

    new_input = tokenizer(full_prompt + tokenizer.eos_token, return_tensors='pt')

    if chat_history_ids is not None:
        bot_input_ids = torch.cat([chat_history_ids, new_input["input_ids"]], dim=-1)
        if bot_input_ids.shape[-1] > MAX_HISTORY_TOKENS:
            chat_history_ids = None
            bot_input_ids = new_input["input_ids"]
    else:
        bot_input_ids = new_input["input_ids"]

    chat_history_ids = model.generate(
        bot_input_ids,
        max_length=1000,
        pad_token_id=tokenizer.eos_token_id
    )

    output = tokenizer.decode(
        chat_history_ids[:, bot_input_ids.shape[-1]:][0],
        skip_special_tokens=True
    )
    return output