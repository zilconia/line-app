import openai
from API_key import GPT_key # chatGPT のAPIキーを外部ファイルからインポート

def main(user_message):
    openai.api_key = GPT_key
    # Define the initial conversation context
    # situation = "非常に仲が良くかなりの悪口が許される友人と会話している状況"
    situation = "友人が会話している状況"

    context = [
        {"role": "system", "content": f"あなたは会話を判断するシステムに組み込まれている。状況は「{situation}」である。次に「履歴」「投稿内容」の順序で会話の流れを入力するため、入力された「投稿内容」に会話上の問題があるか否か判断せよ。問題がない会話の場合は「0」のみを返せ。問題があるとされた会話の場合は先頭に問題の性質を示す数値（1-10）を置き、その後ろにシステムからの返答を返せ。（例：数値,システムからの返答）。システムの返答はそれが問題のある会話であると判断した理由を示し、その代わりのより良いコミュニケーションを生じさせるような提案をせよ。問題の性質は以下の通りに種類分けするものとする。1.人を批判する 2.悪口や中傷 3.嫌悪や軽蔑 4.性的 5.迷惑をかける 6.苦痛・苦悩 7.個人情報の流出 8.誤解を招く発言 9.犯罪・不正行為 10.差別発言 11.皮肉 12.冗談・しゃれ 13.遠慮のない 14.狡猾 15.無神経・気が利かない 16.理解不能・不明瞭"},
    ]
    
    for i in user_message: # メッセージの履歴と入力内容を追加
        context[0]["content"] += f"\n{i} "
    
    # Create a chat completion with the gpt-3.5-turbo model
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=context,
        temperature=1,
        top_p=0.8
    )

    # 出力結果を表示
    print(response['choices'][0]['message']['content'])

    # Add the assistant's response to the conversation context
    context.append({"role": "assistant", "content": response['choices'][0]['message']['content']})
    
    # "0" 以外の、問題のあるコメントに対する出力であれば出力を返す。
    if response['choices'][0]['message']['content'].strip() != '0':
        return response['choices'][0]['message']['content']
    
if __name__ == "__main__":
    a=[]
    print("「ユーザー名:投稿内容」の形式で入力\n")
    for i in range(5):
        text=input("投稿内容を入力：")
        a.append(text)
    main(a)