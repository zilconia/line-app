import openai
from API_key import GPT_key

def main(user_message):
    openai.api_key = GPT_key
    # Define the initial conversation context
    # situation = "非常に仲が良くかなりの悪口が許される友人と会話している状況"
    situation = "友人が会話している状況"

    context = [
        {"role": "system", "content": f"あなたは会話を判断するシステムに組み込まれている。状況は「{situation}」である。次に入力しようとしている会話を入力するため、それに問題があるか否か判断せよ。 問題がない会話の場合は「0」のみを返せ。 また会話の履歴も残すため、その会話の流れからも判断せよ。問題があるとされた会話の場合は先頭に問題の性質を示す数値（1-10）を置き、その後ろにシステムからの返答を返せ。（例：数値,システムからの返答）。システムの返答はそれが問題のある会話であると判断した理由を示し、その代わりのより良いコミュニケーションを生じさせるような提案をせよ。問題の性質は以下の通りに種類分けするものとする。1.人を批判する 2.悪口や中傷 3.嫌悪や軽蔑 4.コミュニケーションが破綻するもの 5.性的 6.不快感を与えるもの 7.迷惑をかける 8.相手の気分を害する 9.苦痛・苦悩 10.信頼性・不確実性"},
    ]

    # while True:
    # Get the user's message from the command line
    # user_message = input()

    # Add the user's message to the conversation context
    """
    c=0
    if type(user_message)!=str:
        try:
            c=len(user_message)
        except TypeError:
            
        context.append({"role": "user", "content": user_message})
    else:     
        for i in range(user_message):
            context.append({"role": "user", "content": user_message[i]})
    """
    for i in user_message:
        context.append({"role": "user", "content": f"{i}"})
    
    # Create a chat completion with the gpt-3.5-turbo model
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=context,
        temperature=1,
        top_p=0.8
    )

    # Print the assistant's response
    print(response['choices'][0]['message']['content'])

    # Add the assistant's response to the conversation context
    context.append({"role": "assistant", "content": response['choices'][0]['message']['content']})
    # Check if the response content is '0'
    if response['choices'][0]['message']['content'].strip() != '0':
        # Print the assistant's response
        return response['choices'][0]['message']['content']

    
