from linebot import LineBotApi
from linebot.exceptions import LineBotApiError

from API_key import Token
# LineBotApiのインスタンスを作成
line_bot_api = LineBotApi(Token)

def get_account_name(user_id):
    try:
        # プロフィール情報を取得
        profile = line_bot_api.get_profile(user_id)
        account_name = profile.display_name
        return profile
    except LineBotApiError as e:
        # エラーハンドリング
        print(e)
        return None

if __name__=="__main__":
    id="Uf6e2c78c0239e0dd23dd613776284c06"
    print(get_account_name(id))