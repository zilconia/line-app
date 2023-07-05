// 「厳密モード」で、jsファイルを実行。
"use strict";

// note.js で使用するツールの呼び出し。
// Webアプリケーションフレームワーク「Express」を読み込む。
const express = require("express");
// LineBot を Node.js で実装するためのSDK「line/bot-sdk」を読み込む。
const line = require("@line/bot-sdk");

// ローカルサーバーで使用するポート番号の設定
const PORT = process.env.PORT || 5000;

/* LineBotのAPIをセットする。
 「チャネルシークレット」== channelSecret
 「チャネルアクセストークン」== channelAccessToken */
const config = {
  channelSecret: "", 
  channelAccessToken: ""
};

// Express を格納。
const app = express();

/*「Express」の機能である、Post関数を呼び出して使用する。
あああ
*/
app.post("/webhook", line.middleware(config), (req, res) => {
  console.log(req.body.events);
  Promise.all(req.body.events.map(handleEvent)).then((result) =>
    res.json(result)
  );
});

const client = new line.Client(config);

async function handleEvent(event) {
  if (event.type !== "message" || event.message.type !== "text") {
    return Promise.resolve(null);
  };

// mes => 出力に関係している。
//変更前
  let mes = { type: "text", text: event.message.text };
/*変更後　　2箇所に画像のURLを入れる
    let mes = {
                type: "image", 
                originalContentUrl: "https://assets.st-note.com/production/uploads/images/20724948/rectangle_large_type_2_ebc45bb792e72e0c88458104d21977b7.jpg",
                previewImageUrl: "https://assets.st-note.com/production/uploads/images/20724948/rectangle_large_type_2_ebc45bb792e72e0c88458104d21977b7.jpg"
               }
  */
  return client.replyMessage(event.replyToken, mes);
}

app.listen(PORT);
console.log(`Server running at ${PORT}`);