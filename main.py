from api_app import router
from csv_tools import load_documents_csv
from document_tools import *
from fastapi import FastAPI

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

print("通过CSV文件：")
documents = load_documents_csv("data/documents.csv")
print("存文件：")
save_documents(documents,"~/Documents/GitHub/Python/test.json")
print("读文件：")
print(load_documents("~/Documents/GitHub/Python/test.json"))

api = FastAPI()
api.include_router(router, prefix="/api", tags=["Documents"])
