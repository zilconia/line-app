import openai
import json

from Py_Linebot import API_key as api

openai.api_key = api.GPT_key

todo_list = ['todo']

def add_todo(todo):
    todo_list.append(todo)
    todo_info = {
        "status": "success",
        "todo": todo,
    }
    return json.dumps(todo_info)


def remove_todo(todo):
    todo_list.remove(todo)
    todo_info = {
        "status": "success",
        "todo": todo,
    }
    return json.dumps(todo_info)


# Step 1, ユーザクエリと同時にfunctionsパラメータに関数の説明を渡してモデルを呼び出し
def run_conversation():
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=[{"role": "user", "content": "ティッシュを買うのを追加して"}],
        functions=[
            {
                "name": "add_todo",
                "description": "Add a todo to the list",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "todo": {
                            "type": "string",
                            "description": "a todo to add",
                        },
                    },
                    "required": ["todo"],
                },
            },
            {
                "name": "remove_todo",
                "description": "Remove a todo from the list",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "todo": {
                            "type": "string",
                            "description": "a todo to remove",
                        },
                    },
                    "required": ["todo"],
                },
            },
        ],
        function_call="auto",
    )

    message = response["choices"][0]["message"]
    print(message)

    # Step 2, モデルが関数を呼び出そうとしているか否かを確認
    if message.get("function_call"):
        function_name = message["function_call"]["name"]

        todo = json.loads(message["function_call"]["arguments"])["todo"]

        # Step 3, 実際に関数を呼び出す
        if function_name == "add_todo":
            function_response = add_todo(todo=todo)
        elif function_name == "remove_todo":
            function_response = remove_todo(todo=todo)

        print(todo_list)


        # Step 4, 実行結果を元に最終的なレスポンスを得る
        second_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0613",
            messages=[
                {"role": "user", "content": "ティッシュを買うのを追加して"},
                message,
                {
                    "role": "function",
                    "name": function_name,
                    "content": function_response,
                },
            ],
        )
        return second_response


print(run_conversation()["choices"][0]["message"]["content"])
# 「ティッシュを買う」が追加されました。