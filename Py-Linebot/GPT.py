import openai
from typing import Optional, Union, List

# Set your API key
openai.api_key = "YOU-GPT-KEY"

# すべての変数を初期化
def reset_variables():
    global conversation_history
    global context
    global preprocessed_input
    global gpt_response
    global parsed_output
    global final_output

    conversation_history = []
    context = ""
    preprocessed_input = ""
    gpt_response = ""
    parsed_output = ""
    final_output = ""

# Preprocess the input text and context for the GPTAPI
def preprocess_input(conversation_history: List[str], context: str) -> str:
    # 過去ログを設定？
    conversation_text = "\n".join([f"投稿: {text}" for text in conversation_history])
    # 命令内容を設定して送信
    prompt = f"挨拶と、その前にランダムな一桁の数値を示せ（例：数値,挨拶）"
    return prompt

# Call the GPTAPI with the preprocessed input
def call_gpt_api(input_text: str, model: str = "text-davinci-003") -> str:
    response = openai.Completion.create(
        engine=model,
        prompt=input_text,
        max_tokens=200,
        n=1,
        stop=None,
        temperature=0.5,
    )

    return response.choices[0].text.strip()

# Parse the GPTAPI response to determine if there is any malicious content
def parse_gpt_response(response: str) -> Union[str, int]:
    if response == "0":
        return 0
    else:
        return response

# Process the parsed output to return None if no malicious content is detected
def process_output(output: Union[str, int], threshold: int = 9) -> Optional[str]:
    if output == 0:
        return None
    else:
        malicious_level, reason = output.split(",", 1)
        # デバックのため数値と理由を表示
        print("_debug_malicious_level:", malicious_level)
        print("_debug_reason:", reason)
        # デバックはここまで
        """
        if int(malicious_level) > threshold:
            return reason
        else:
            return None
        """
        return reason

# Main function to continuously monitor conversation
def main(input_text):
    reset_variables()
    # print("Enter 'q' to quit the conversation monitoring.")
    
    conversation_history = []
    """
    input_text = input("Enter the text you want to analyze: ")
    
    if input_text.lower() == "q":
        break
    """
    conversation_history.append(input_text)
    context = "挨拶を返す"
        
    preprocessed_input = preprocess_input(conversation_history, context)
    gpt_response = call_gpt_api(preprocessed_input)
    parsed_output = parse_gpt_response(gpt_response)
    final_output = process_output(parsed_output)

    if final_output:
        print("Reason for maliciousness:", final_output)
    else:
        pass
    #print(f"内容：{final_output}")
    return final_output

if __name__ == "__main__":
    main("こんにちは")
