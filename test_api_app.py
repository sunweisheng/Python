"""FastAPI接口测试学习示例：检查状态码、返回内容与资料变化。"""

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

import api_app


@pytest.fixture
def client(monkeypatch):
    """每个测试开始前，准备一份独立资料和一个测试客户端。"""
    # @pytest.fixture告诉pytest：这个函数用于准备测试。
    # 测试函数声明client参数时，pytest会先执行这里。
    documents = [
        {
            "title": "报销流程",
            "department": "财务",
            "approved": True,
            "score": 92,
        },
        {
            "title": "发票说明",
            "department": "财务",
            "approved": True,
            "score": 80,
        },
        {
            "title": "付款规则",
            "department": "财务",
            "approved": False,
            "score": 95,
        },
        {
            "title": "入职指南",
            "department": "人事",
            "approved": True,
            "score": 76,
        },
        {
            "title": "零分资料",
            "department": "财务",
            "approved": True,
            "score": 0,
        },
    ]

    # 临时替换接口使用的资料，测试结束后pytest会自动恢复。
    # 每次执行这个准备函数，都会创建一份新的documents列表。
    monkeypatch.setattr(api_app, "documents", documents)

    # 创建测试应用，挂载你实际编写的路由，保留/api前缀。
    # main.py中还有旧练习的文件写入，这里直接使用api_app的路由。
    app = FastAPI()
    app.include_router(api_app.router, prefix="/api")

    # TestClient直接调用应用，无须先启动服务器。
    with TestClient(app) as test_client:
        # 先把客户端交给测试；测试结束后退出with，关闭客户端。
        yield test_client


def test_read_documents(client):
    """查询财务80分资料：保留达标且已审核的资料。"""
    # 1. 执行：通过params传入部门和最低分。
    response = client.get(
        "/api/documents",
        params={"department": "财务", "min_score": 80},
    )

    # 2. 检查状态码，确认请求成功。
    assert response.status_code == 200

    # 3. 检查完整内容和顺序，恰好80分的资料也必须包含。
    expected = [
        {
            "title": "报销流程",
            "department": "财务",
            "approved": True,
            "score": 92,
        },
        {
            "title": "发票说明",
            "department": "财务",
            "approved": True,
            "score": 80,
        },
    ]
    assert response.json() == expected


def test_read_documents_default_min_score(client):
    """省略最低分时，使用默认值0，已审核的零分资料也能查到。"""
    response = client.get(
        "/api/documents",
        params={"department": "财务"},
    )

    assert response.status_code == 200

    titles = []
    for document in response.json():
        titles.append(document["title"])

    assert titles == ["报销流程", "发票说明", "零分资料"]


def test_read_documents_no_matches(client):
    """没有匹配资料时，仍返回200，但列表为空。"""
    response = client.get(
        "/api/documents",
        params={"department": "不存在的部门", "min_score": 80},
    )

    assert response.status_code == 200
    assert response.json() == []


def test_read_documents_invalid_parameters(client):
    """部门缺失或为空、最低分无效时，都返回422。"""
    invalid_parameters = [
        {},
        {"department": ""},
        {"department": "财务", "min_score": "abc"},
        {"department": "财务", "min_score": -1},
        {"department": "财务", "min_score": 101},
    ]

    for params in invalid_parameters:
        response = client.get("/api/documents", params=params)

        assert response.status_code == 422
        # FastAPI的校验错误会在detail中说明位置和原因。
        detail = response.json()["detail"]
        assert detail
        assert detail[0]["loc"][0] == "query"


def test_read_document_by_title(client):
    """按完整标题查询，不受审核状态限制。"""
    response = client.get("/api/documents/付款规则")

    assert response.status_code == 200
    assert response.json() == {
        "title": "付款规则",
        "department": "财务",
        "approved": False,
        "score": 95,
    }


def test_read_document_not_found(client):
    """不存在的标题返回404，并说明资料不存在。"""
    response = client.get("/api/documents/不存在的资料")

    assert response.status_code == 404
    assert "不存在" in response.json()["detail"]


def test_add_document(client):
    """新增返回201，且随后能通过另一个接口查到。"""
    new_document = {
        "title": "测试资料",
        "department": "技术",
        "approved": True,
        "score": 88,
    }

    # json参数把这个Python字典作为JSON请求体提交。
    response = client.post("/api/documents", json=new_document)

    assert response.status_code == 201
    assert response.json() == new_document

    # 继续查询，确认资料确实加入了共用的内存列表。
    query_response = client.get("/api/documents/测试资料")

    assert query_response.status_code == 200
    assert query_response.json() == new_document


def test_add_duplicate_document(client):
    """已有标题不能重复新增，也不能覆盖原资料。"""
    duplicate_document = {
        "title": "报销流程",
        "department": "财务",
        "approved": True,
        "score": 10,
    }

    response = client.post("/api/documents", json=duplicate_document)

    assert response.status_code == 409
    assert "已经存在" in response.json()["detail"]

    query_response = client.get("/api/documents/报销流程")

    assert query_response.status_code == 200
    assert query_response.json()["score"] == 92


def test_add_document_missing_fields(client):
    """逐个省略必需字段，检查是否返回422并指出缺少的字段。"""
    new_document = {
        "title": "测试资料",
        "department": "技术",
        "approved": True,
        "score": 88,
    }
    required_fields = ["title", "department", "approved", "score"]

    for field in required_fields:
        # 复制一份再删除字段，保留完整样本供下一轮使用。
        invalid_document = new_document.copy()
        del invalid_document[field]

        response = client.post("/api/documents", json=invalid_document)

        assert response.status_code == 422
        detail = response.json()["detail"]
        assert detail[0]["loc"] == ["body", field]


def test_add_document_invalid_fields(client):
    """空标题、空部门、非法审核状态或分数，都应返回422。"""
    new_document = {
        "title": "测试资料",
        "department": "技术",
        "approved": True,
        "score": 88,
    }
    invalid_values = [
        ("title", ""),
        ("department", ""),
        ("approved", "unknown"),
        ("score", "abc"),
        ("score", -1),
        ("score", 101),
    ]

    for field, value in invalid_values:
        invalid_document = new_document.copy()
        invalid_document[field] = value

        response = client.post("/api/documents", json=invalid_document)

        assert response.status_code == 422
        detail = response.json()["detail"]
        assert detail[0]["loc"] == ["body", field]


def test_add_document_score_boundaries(client):
    """新增时，0分和100分都属于合法范围。"""
    for score in (0, 100):
        new_document = {
            "title": f"边界资料{score}",
            "department": "测试部门",
            "approved": True,
            "score": score,
        }

        response = client.post("/api/documents", json=new_document)

        assert response.status_code == 201
        assert response.json() == new_document
