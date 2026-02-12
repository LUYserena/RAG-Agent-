from langchain_community.document_loaders import CSVLoader

loader = CSVLoader(file_path="./data/stu.csv",
                   encoding="utf-8", 
                   csv_args={"delimiter": ",",
                             "quotechar": '"',
                             #如果数据原来没有表头可以使用，否则不需要
                             "fieldnames": ["id", "name", "age"]})

#批量加载 .load -> [Document, Document, Document] 文档对象列表
documents = loader.load()

print(documents)

#懒加载 .lazy_load() -> Iterable[Document] 可迭代的文档对象
for document in loader.lazy_load():
    print(document)