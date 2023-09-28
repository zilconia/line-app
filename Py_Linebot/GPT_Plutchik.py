import openai
from API_key import GPT_key # chatGPT のAPIキーを外部ファイルからインポート

def main(user_message):
    openai.api_key = GPT_key
    # Define the initial conversation context
    # situation = "非常に仲が良くかなりの悪口が許される友人と会話している状況"
    # situation = "非常に仲が良くかなりの悪口が許される友人と会話している状況"
    # relationship = "友人"
    # age_a = 20
    # age_b = 20
    # gender_a = "男性"
    # gender_b = "男性"

    flag = [
       "恍惚：255,255,0","喜び：255,255,70","平穏：255,255,140",
       "感嘆：0,140,0","信頼：70,255,70","容認：140,255,140",
       "恐怖：0,70,0","恐れ：0,140,0","心配：140,200,140",
       "驚嘆：0,70,255","驚き：70,140,255","動揺：140,200,255",
       "悲痛：0,0.255","悲しみ：70,70,255","憂い：140,140,255",
       "憎悪：255,0,255","嫌悪：255,100,255","退屈：255,200,255",
       "憤怒：140,0,0","怒り：255,0,0","煩さ：255,140,140",
       "警戒：255,70,0","予期：255,140,70","興味：255,200,140",
    ]
    
    context = [
        {"role": "system", "content": f"あなたは投稿を判断するシステムに組み込まれている。次の発言者である者の投稿を入力するため、その投稿の感情をプルチックの感情の輪を元にして判断せよ。 \n【プルチックの感情の輪とその色(R,G,B)は以下の通りである。】\n"}]
    
    for i in flag: # 指定した条件を「content」内に蓄積させていく。
        context[0]["content"] += f"{flag.index(i)+1},{i} "
    
    # context.append({"role": "user", "content": user_message})
    for i in user_message: # メッセージの履歴と入力内容を追加
        context.append(i)
        # if user_message.index(i) == 0 and len(user_message) > 1:
        #     context[0]["content"] += "\n「履歴」"
        # elif user_message.index(i) == (len(user_message)-1):
        #     context[0]["content"] += "\n「投稿内容」"
        # context[0]["content"] += f"\n{i} "
    
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
