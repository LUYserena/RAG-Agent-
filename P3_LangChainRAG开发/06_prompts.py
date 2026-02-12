from langchain_core.prompts import PromptTemplate
from langchain_community.llms.tongyi import Tongyi
prompt_template = PromptTemplate.from_template(
    "我的邻居姓{last_name}, 刚生了个{gender}, 你能帮我想个名字吗？简单回答"
)

#调用format方法传入变量值，得到最终的提示词
prompt_text = prompt_template.format(last_name="孙", gender="女")

model = Tongyi(model="qwen-max")
res = model.invoke(input=prompt_text)
print(res)

chain = prompt_template | model

res = chain.invoke(input={"last_name": "李", "gender": "男"})
print(res)
