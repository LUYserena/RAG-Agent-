from langchain_community.document_loaders import PyPDFLoader

loader = PyPDFLoader(
    file_path="./data/stu.pdf",
    mode = "single",
    #默认page模式，每个页面形成一个Document文档对象
    # single模式，不管有多少也，只返回一个Document对象
    password = None #如果PDF文件有密码，可以在这里设置
    )


for doc in loader.lazy_load():
    print(doc)