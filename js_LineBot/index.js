"use strict";

const express = require("express");
const line = require("@line/bot-sdk");
const PORT = process.env.PORT || 8000;

const config = {
  channelSecret: "794dd836d5cb9682dc11b6c60896cf7a", 
  channelAccessToken: "jUoJ1XL6FZNlq/IXD7nuFOymzdqCVCOO+VhEp70csUsFrHxsvTqsjSdTf/l1YwPjKX+vxLOTmzlnf1J3rj76C4nFQRWc0DPKvBY90xJFvO2+3xhWwAng1jrGqBZOx7lmFupp704EvTjKhZWrMQxGDwdB04t89/1O/w1cDnyilFU="
};

const app = express();

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