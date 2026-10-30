import json

from document_tools import *
import pytest
from copy import deepcopy

documents = [
    {"title": "报销流程", "department": "财务", "approved": True, "score": 92},
    {"title": "发票说明", "department": "财务", "approved": True, "score": 80},
    {"title": "付款规则", "department": "财务", "approved": False, "score": 95},
    {"title": "入职指南", "department": "人事", "approved": True, "score": 76},
    {"title": "账号申请", "department": "技术", "approved": True, "score": 88},
]

def test_find_document():
    add_document(documents,"测试标题","测试部门",True,85)
    assert find_document(documents,"测试标题")["title"] == "测试标题"
def test_filter_documents():
    before = deepcopy(documents)
    re = filter_documents(documents,"财务",80)
    assert re == [documents[0], documents[1]]
    re = filter_documents(documents, "财务部", 0)
    assert len(re) == 0
    assert filter_documents([], "财务", 0) == []
    with pytest.raises(ValueError, match="title"):
        filter_documents(
            [{"department": "财务", "approved": True, "score": 92}],
            "财务部",
            0,
        )
    assert before == documents

def test_save_documents(tmp_path):
    save_documents(documents,tmp_path / "test.json")
    with open(os.path.expanduser(tmp_path / "test.json"), "r",encoding="utf-8") as f:
        content = f.read()
        assert "报销流程" in content
        assert json.loads(content) == documents


def test_load_documents(tmp_path):
    pa = os.path.expanduser(tmp_path / "test.json")
    if os.path.exists(pa):
        os.remove(pa)

    assert load_documents(pa) is None

    with open(pa, "w",encoding="utf-8") as f:
        f.write("abc")
    assert load_documents(pa) is None

    with open(pa, "w",encoding="utf-8") as f:
        f.write("{abc}")
    assert load_documents(pa) is None

    with open(pa, "w",encoding="utf-8") as f:
        f.write("{}")
    assert load_documents(pa) is None

    with open(pa, "w",encoding="utf-8") as f:
        f.write("[]")
    assert load_documents(pa) == []

    expected = deepcopy(documents)
    save_documents(expected, pa)

    assert load_documents(pa) == expected