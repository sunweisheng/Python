import json

import requests

def fetch_documents(base_url, department, min_score):
    documents = None
    params = {
        "department": department,
        "min_score": min_score,
    }
    try:
        req = requests.get(base_url,params=params, timeout=5)
        req.raise_for_status()
        documents = req.json()
    except json.decoder.JSONDecodeError as e:
        print(f"JSON解释失败：{e.msg}")
        return None
    except requests.exceptions.Timeout as e:
        print(f"请求超时：{e}")
        return None
    except requests.exceptions.HTTPError as e:
        print(f"HTTP 错误：{e}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"请求异常：{e}")
        return None
    if not isinstance(documents, list):
        print("资料文件格式错误!")
        return None
    return documents



print(fetch_documents("http://127.0.0.1:8000/api/documents","财务",80))