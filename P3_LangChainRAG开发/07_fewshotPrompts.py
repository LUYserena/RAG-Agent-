from langchain_core.prompts import FewShotPromptTemplate, PromptTemplate
from langchain_community.llms.tongyi import Tongyi
#示例的模板
example_template = PromptTemplate.from_template("单词：{word}, 反义词：{antonym}")

#示例数据,要求是list内套字典
examples = [
    {"word": "高兴", "antonym": "难过"},
    {"word": "快速", "antonym": "缓慢"},
    {"word": "强大", "antonym": "脆弱"},
]

few_shot_template = FewShotPromptTemplate(
    example_prompt=example_template, #示例数据的模板
    examples=examples,        #示例数据列表
    prefix="告诉我词语的反义词，我提供如下的示例：",        #提示词前缀
    suffix="基于上述示例，告诉我, {input_word}的反义词是",        #提示词后缀
    input_variables=['input_word'], #输入变量列表,声明在前后缀中需要注入的变量名
)

prompt_text = few_shot_template.invoke({"input_word": "幸福"}).to_string()
print(prompt_text)

model = Tongyi(model="qwen-max")
res = model.invoke(input=prompt_text)
print(res)