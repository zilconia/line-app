import openai
from API_key import GPT_key # chatGPT のAPIキーを外部ファイルからインポート

def main(user_message):
    openai.api_key = GPT_key
    # Define the initial conversation context
    # situation = "非常に仲が良くかなりの悪口が許される友人と会話している状況"
    situation = "非常に仲が良くかなりの悪口が許される友人と会話している状況"
    relationship = "友人"
    age_a = 20
    age_b = 20
    gender_a = "男性"
    gender_b = "男性"

    flag = [
       "人を批判する","悪口や中傷","嫌悪や軽蔑","性的",
       "迷惑をかける","苦痛・苦悩","個人情報の流出",
       "誤解を招く発言","犯罪・不正行為","差別発言",
       "皮肉","冗談・しゃれ","遠慮のない","狡猾",
       "無神経・気が利かない","理解不能・不明瞭"
    ]
    
    context = [
        {"role": "system", "content": f"あなたは会話を判断するシステムに組み込まれている。次の発言者である者の投稿を入力するため、その投稿に問題があるか否か判断せよ。問題がない投稿の場合は「0」のみを返せ。 また投稿の履歴も渡すため、その会話の流れからも判断せよ。発言者である者の投稿に問題があるとされた場合は先頭に問題の性質を示す種類分けされた番号を置き、その後ろにシステムからの返答を返せ。（例：数値,システムからの返答）。なお今のシステムでは過剰に反応しがちのため、それを抑制することに留意せよ。システムの返答はそれが問題のある会話であると判断した根拠を種類分けを元にして示し、その代わりのより良いコミュニケーションを生じさせるような提案をせよ。パラメータは以下の通りとする。【パラメータ】状況：{situation} 関係性：{relationship} 年齢：aが{age_a}歳、bが{age_b}歳 性別：aが{gender_a}、bが{gender_b}  【問題の性質は以下の通りに種類分けの番号を付与する】"},
    ]
    for i in flag: # 指定した条件を「content」内に蓄積させていく。
        context[0]["content"] += f"{flag.index(i)+1},{i} "
    
<<<<<<< HEAD
    
    for i in user_message: # メッセージの履歴と入力内容を追加
        # context.append({"role": "user", "content": i})
        
        if user_message.index(i) == 0 and len(user_message) > 1:
            context[0]["content"] += "\n「履歴」"
        elif user_message.index(i) == (len(user_message)-1):
            context[0]["content"] += "\n「投稿内容」"
        context[0]["content"] += f"\n{i} "
=======
    # context.append({"role": "user", "content": user_message})
    for i in user_message: # メッセージの履歴と入力内容を追加
        context.append(i)
        # if user_message.index(i) == 0 and len(user_message) > 1:
        #     context[0]["content"] += "\n「履歴」"
        # elif user_message.index(i) == (len(user_message)-1):
        #     context[0]["content"] += "\n「投稿内容」"
        # context[0]["content"] += f"\n{i} "
>>>>>>> d54b12c7d0939f963b575c8672f6efd5c7034fd7
    
    # ChatGPT-API へのデータ入力開始
    response = openai.ChatCompletion.create( 
        model="gpt-3.5-turbo", # 使用モデル名
        messages=context, # 入力メッセージ
        temperature=1, # 
        top_p=0.8 # 
    )

    # 出力結果を表示
    print(response['choices'][0]['message']['content'])

    # Add the assistant's response to the conversation context
    # context.append({"role": "assistant", "content": response['choices'][0]['message']['content']})

    # "0" 以外の、問題のあるコメントに対する出力であれば出力を返す。
    # if response['choices'][0]['message']['content'].strip() != '0':
    return response['choices'][0]['message']['content']
    
if __name__ == "__main__":
    a=[]
    print("「ユーザー名:投稿内容」の形式で入力\n「quit」で停止")
    while True:
        text=input("\n投稿内容を入力：")
        if text[0:4]=="quit":
            break
        a.append(text)
        if len(a)>=10:
            a.pop(0)
            a.pop(0)
<<<<<<< HEAD
        a.append(main(a))
=======
        a.append(main(a))
        print(a[len(a)-1])
>>>>>>> d54b12c7d0939f963b575c8672f6efd5c7034fd7
