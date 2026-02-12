import json

d = {
    "name": "Alice",
    "age": 30,
    "gender": "男"
}

s = json.dumps(d, ensure_ascii=False)
print(s)  # {"name": "Alice", "age": 30, "gender: "男"}

#列表转json字符串
l = [
    {
    "name": "Alice",
    "age": 30,
    "gender": "男"
    },
    {
    "name": "Jack",
    "age": 30,
    "gender": "男"
    },
        {
    "name": "Serena",
    "age": 18,
    "gender": "女"
    }
]

s = json.dumps(l, ensure_ascii=False)
print(s)

#json字符串转字典
json_str = '{"name": "Alice", "age": 30, "gender": "男"}'

json_array_str = '[{"name": "Alice", "age": 30, "gender": "男"}, {"name": "Jack", "age": 30, "gender": "男"}, {"name": "Serena", "age": 18, "gender": "女"}]'

res_dict = json.loads(json_str)
print(res_dict, type(res_dict))

res_list = json.loads(json_array_str)
print(res_list, type(res_list))