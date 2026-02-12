from openai import OpenAI
import os
import json
#1.获取client对象

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

schema = ['日期', '股票名称', '开盘价', '收盘价', '成交量']

examples_data = [
    {
        "content": "2023-01-10, 股市震荡。股票强大科技A股今天开盘价100人币，一度涨至105人币，随后回落至98人币，最终以102人币收盘，成交量达到520000。 ",
        "answers": {
            "日期": "2023-01-10",
            "股票名称": "强大科技股",
            "开盘价": "100人民币",
            "收盘价": "102人民币",
            "成交量": "520000"
        }
    },
    {
        "content": "2024-05-16, 股市好。股票英伟达股票A股今天开盘价105美元，一度涨至109美元，随后回落至100美元，最终以116美元收盘，成交量达到3560000。 ",
        "answers": {
            "日期": "2024-05-16",
            "股票名称": "英伟达股票",
            "开盘价": "105美元",
            "收盘价": "116美元",
            "成交量": "3560000"
        }
    }
]

questions = [
    "2025-06-16, 股市好。股票智能教育AR公司A股今天开盘价66人民币，一度涨至70人民币，随后回落至65人民币，最终以68人民币收盘，成交量达到123000。",
    "2025-06-06, 股市好。股票智能服务AR公司A股今天开盘价200人民币，一度涨至211人民币，随后回落至201人民币，最终以206人民币收盘，成交量达到156000。"
]

messages = [
    {"role": "system", "content": f"你帮我完成信息抽取，我给你句子，你抽取{schema}信息，按JSON格式返回结果。如果某些信息不存在，用“无”表示。"},
]

for example in examples_data:
    messages.append({"role": "user", "content": example['content']})
    messages.append({"role": "assistant", "content": json.dumps(example['answers'], ensure_ascii=False)})
    
# for x in messages:
#     print(x)

for question in questions:
    response = client.chat.completions.create(
        model="qwen3-max",
        messages=messages + [{"role": "user", "content": f"按照示例，抽取这段文本的信息：{question}"}]
    )
    print(response.choices[0].message.content)