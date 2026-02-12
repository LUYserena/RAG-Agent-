from langchain_community.document_loaders import JSONLoader

# loader = JSONLoader(file_path="./data/stu.json",
#                     jq_schema=".",
#                     text_content=False #默认为True，为False代表抽取的内容不是字符串
# )

loader = JSONLoader(file_path="./data/stu_json_lines.json",
                    jq_schema=".name",
                    text_content=False, #默认为True，为False代表抽取的内容不是字符串
                    json_lines=True #默认为False，代表文件是一个完整的JSON对象，为True代表文件是JSON Lines格式，每行一个JSON对象
)

document = loader.load()
print(document)