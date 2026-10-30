from document_tools import *

documents = [
    {"title": "报销流程", "department": "财务", "approved": True, "score": 92},
    {"title": "发票说明", "department": "财务", "approved": True, "score": 80},
    {"title": "付款规则", "department": "财务", "approved": False, "score": 95},
    {"title": "入职指南", "department": "人事", "approved": True, "score": 76},
    {"title": "账号申请", "department": "技术", "approved": True, "score": 88},
]

print(add_document(documents,"测试标题","测试部门",True,85))

print(find_document(documents,"测试标题"))

print(filter_documents(documents,"财务",80))

print("存文件：")
save_documents(documents,"~/Documents/GitHub/Python/test.json")
print("读文件：")
print(load_documents("~/Documents/GitHub/Python/test.json"))