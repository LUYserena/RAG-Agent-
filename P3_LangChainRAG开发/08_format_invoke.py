from langchain_core.prompts import FewShotPromptTemplate, PromptTemplate, ChatPromptTemplate, HumanMessagePromptTemplate

'''
PromptTemplate -> StringPromptTemplate -> BasePromptTemplate -> RunnableSerializable -> Runnable
FewShotPromptTemplate -> -> StringPromptTemplate -> BasePromptTemplate -> RunnableSerializable -> Runnable
ChatPromptTemplate -> BaseChatPromptTemplate -> BasePromptTemplate -> RunnableSerializable -> Runnable
'''

template = PromptTemplate.from_template("我的邻居是{lastname}最喜欢的是：{hobby}")

res = template.format(lastname="张三", hobby="打篮球")
print(res, type(res))

res2 = template.invoke({"lastname":"周杰伦", "hobby":"周杰伦"})
print(res2, type(res2))