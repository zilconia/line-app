import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
# ライブラリ「SentencePiece」も必要になる
# ( T5Tokenizer で上記ライブラリが必要になるため。)

tokenizer = AutoTokenizer.from_pretrained("rinna/japanese-gpt-neox-3.6b-instruction-sft", use_fast=False)
model = AutoModelForCausalLM.from_pretrained("rinna/japanese-gpt-neox-3.6b-instruction-sft")

if torch.cuda.is_available():
    #model = model.to("cuda")
    model = model.to("cpu")

# 初期の会話プロンプト
conversation = [
    {
        "speaker": "システム",
        "text": "こんにちは、何をお手伝いできますか？"
    }
]

while True:
    # ユーザーからの入力を受け取る
    user_input = input("ユーザー: ")

    # ユーザーの発話を会話に追加する
    conversation.append({
        "speaker": "ユーザー",
        "text": user_input
    })

    # 入力プロンプトを作成する
    prompt = [
        f"{uttr['speaker']}: {uttr['text']}"
        for uttr in conversation
    ]
    prompt = "<NL>".join(prompt)
    prompt = (
        prompt
        + "<NL>"
        + "システム: "
    )

    # モデルによる応答を生成する
    token_ids = tokenizer.encode(prompt, add_special_tokens=False, return_tensors="pt")

    with torch.no_grad():
        output_ids = model.generate(
            token_ids.to(model.device),
            do_sample=True,
            max_new_tokens=128,
            temperature=0.7,
            pad_token_id=tokenizer.pad_token_id,
            bos_token_id=tokenizer.bos_token_id,
            eos_token_id=tokenizer.eos_token_id
        )

    output = tokenizer.decode(output_ids.tolist()[0][token_ids.size(1):])
    output = output.replace("<NL>", "\n")

    # システムの応答を表示する
    print("システム:", output)

    # システムの応答を会話に追加する
    conversation.append({
        "speaker": "システム",
        "text": output
    })