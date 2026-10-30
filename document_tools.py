import json
import os

def add_document(documents, title, department, approved, score):
    if documents is None:
        raise ValueError("documents参数为空！")
    if not title:
        raise ValueError("title参数为空！")
    if not department:
        raise ValueError("department参数为空！")
    if approved is None:
        raise ValueError("approved参数为空！")
    if score is None:
        raise ValueError("score参数为空！")
    documents.append({"title": title, "department": department, "approved":approved, "score": score})
    return documents[-1]

def find_document(documents, title):
    if documents is None:
        raise ValueError("documents参数为空！")
    if not title:
        raise ValueError("title参数为空！")
    if not documents:
        return None
    if "title" not in documents[0].keys():
        raise ValueError("documents列表字典缺少必要的Key：title")
    if "department" not in documents[0].keys():
        raise ValueError("documents列表字典缺少必要的Key：department")
    if "approved" not in documents[0].keys():
        raise ValueError("documents列表字典缺少必要的Key：approved")
    if "score" not in documents[0].keys():
        raise ValueError("documents列表字典缺少必要的Key：score")
    re = {}
    for doc in documents:
        if doc["title"] == title:
            re["title"] = doc["title"]
            re["department"] = doc["department"]
            re["approved"] = doc["approved"]
            re["score"] = doc["score"]
            return re
    return None

def filter_documents(documents, department, min_score):
    if documents is None:
        raise ValueError("documents参数为空！")
    if not department:
        raise ValueError("department参数为空！")
    if min_score is None:
        raise ValueError("min_score参数为空！")
    if len(documents) == 0:
        return documents
    required_fields = ["title", "department", "approved", "score"]
    re_list = []
    for doc in documents:
        for field in required_fields:
            if field not in doc:
                raise ValueError(f"documents列表字典缺少必要的Key：{field}")
        if doc["department"] == department and doc["score"] >= min_score and doc["approved"]:
            re_list.append(doc)
    return re_list

def save_documents(documents, file_path):
    if documents is None:
        documents = []
    file = open(os.path.expanduser(file_path),"w",encoding="utf-8")
    file.write(json.dumps(documents,ensure_ascii=False))
    file.close()

def load_documents(file_path):
    if file_path is None:
        return None
    fp = os.path.expanduser(file_path)
    file = None
    try:
        file = open(fp, "r", encoding="utf-8")
        documents = json.loads(file.read())
    except FileNotFoundError:
        print("资料文件不存在!")
        return None
    except json.JSONDecodeError:
        print("资料文件内容损坏!")
        return None
    finally:
        if file is not None:
            file.close()
    if not isinstance(documents, list):
        print("资料文件格式错误!")
        return None
    return documents
