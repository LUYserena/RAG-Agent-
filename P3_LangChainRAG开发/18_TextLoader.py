from langchain_community.document_loaders import TextLoader
from langchain_text_splitter import RecursiveCharacterTextSplitter
loader = TextLoader(file_path="./data/stu.txt", encoding="utf-8")

docs = loader.load()

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500, #每个文本块的最大长度
    chunk_overlap=50, #文本块之间的重叠长度
    seperators=["\n\n", "\n", ",", ".", "。", "!"], #文本自然段落分隔的依据符号
    length_function=len #计算文本长度的函数，默认为len，也可以自定义函数
)

split_docs = splitter.split_documents(docs)
print(len(split_docs))

for docs in split_docs:
    print(docs)