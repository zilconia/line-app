import openai
from typing import Optional, Union, List
from API_key import GPT_key

# すべての変数を初期化
def reset_variables():
    global conversation_history
    global context
    global preprocessed_input
    global gpt_response
    global parsed_output
    global final_output
    global input_text

    conversation_history = []
    context = ""
    preprocessed_input = ""
    gpt_response = ""
    parsed_output = ""
    final_output = ""
    input_text = ""

# Preprocess the input text and context for the GPTAPI
def preprocess_input(conversation_history: List[str], context: str) -> str:
    # 過去ログを設定？
    conversation_text = f"投稿: {conversation_history}" 
    # 命令内容を設定して送信
    # prompt = f"あなたは投稿を判断するシステムに組み込まれている。状況は「友人と会話している状況」である。次に入力しようとしている投稿を入力するため、それに暴言があるか否か判断せよ。 暴言がない投稿の場合は「0」のみを返せ。また投稿の履歴も残すため、その会話の流れからも判断せよ。暴言があるとされた投稿の場合は先頭に暴言のレベルを示す数値（1-10）を置き、その後ろにシステムからの返答を返せ。数値が10に近いほどより暴言があるものとする（例：数値,システムからの返答）。システムの返答はそれが暴言のある投稿であると判断した理由を示し、その代わりのより良いコミュニケーションを生じさせるような提案をせよ。"
    # prompt = f"あなたは投稿を判断するシステムに組み込まれている。状況は{context}である。次に入力しようとしている投稿を入力するため、それに問題があるか否か判断せよ。問題がない投稿の場合は「0」のみを返せ。問題があるとされた投稿の場合は先頭に問題のレベルを示す数値（1-10）を置き、その後ろにシステムからの返答を返せ。数値が高いほどより問題があるものとする（例：数値,システムからの返答）。システムの返答はそれが問題のある投稿であると判断した理由を示し、その代わりのより良いコミュニケーションを生じさせるような提案をせよ。"
    # prompt = f"挨拶と、その前にランダムな一桁の数値を示せ（例：数値,挨拶）"
    prompt = f"今から整数を入力する。入力された数値をカンマ区切りで二つ返せ"
    print(conversation_text)
    return prompt

# Call the GPTAPI with the preprocessed input
def call_gpt_api(input_text: str, model: str = "text-davinci-003") -> str:
    response = openai.Completion.create(
        engine=model,
        prompt=input_text,
        max_tokens=200,
        n=1,
        stop=None,
        temperature=0,
    )
    print(f"call：{input_text}")

    return response.choices[0].text.strip()
"""
# Call the GPTAPI with the preprocessed input
def call_gpt_api(input_text: str, model: str = "3.5-turbo") -> str:
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Enter an integer x after this post. Once entered, output in the form 'x,x'"},
            {"role": "user", "content": input_text}
        ]
    )
    # print(response.choices[0].message['content'])
    # print(f"call：{input_text}")

    return response.choices[0].message['content']
"""

# Parse the GPTAPI response to determine if there is any malicious content
def parse_gpt_response(response: str) -> Union[str, int]:
    if response == "0":
        return 0
    else:
        return response

# Process the parsed output to return None if no malicious content is detected
def process_output(output: Union[str, int], threshold: int = 0) -> Optional[str]:
    print(output)
    if output == 0:
        return 0,None
    else:
        malicious_level, reason = output.split(",", 1)
        if __name__ == "__main__":
            # デバックのため数値と理由を表示
            print("_debug_malicious_level:", malicious_level)
            print("_debug_reason:", reason)
        
        # 危険度に応じて返答する機能
        if int(malicious_level) > threshold:
            return malicious_level,reason
        else:
            return malicious_level,None

# Main function to continuously monitor conversation
def main(input_text):
    openai.api_key = GPT_key
    reset_variables()
    # print("Enter 'q' to quit the conversation monitoring.")
    
    conversation_history = input_text
    """
    input_text = input("Enter the text you want to analyze: ")
    
    if input_text.lower() == "q":
        break
    """
    # conversation_history.append(input_text)
    context = "数字を返せ"
        
    preprocessed_input = preprocess_input(conversation_history, context)
    gpt_response = call_gpt_api(preprocessed_input)
    parsed_output = parse_gpt_response(gpt_response)
    level_output,final_output = process_output(parsed_output)
    """
    if final_output:
        print("Reason for maliciousness:", final_output)
    else:
        pass
    """
    #print(f"内容：{final_output}")
    return level_output,final_output

# 直接起動したときのデバッグ用
if __name__ == "__main__":
    main("おはよう")
