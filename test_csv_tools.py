"""CSV读取与JSON保存的学习示例：每个测试独立准备临时文件。"""

import pytest

from csv_tools import load_documents_csv
from document_tools import load_documents, save_documents


def test_load_documents_csv_normal(tmp_path):
    """正常读取：检查内容、行顺序，以及布尔值和整数类型。"""
    # 1. 准备：tmp_path是pytest为本次测试提供的临时目录。
    file_path = tmp_path / "documents.csv"
    csv_content = (
        "title,department,approved,score\n"
        "报销流程,财务,True,92\n"
        "发票说明,财务,True,80\n"
        "付款规则,财务,False,95\n"
    )
    file_path.write_text(csv_content, encoding="utf-8")

    # 2. 执行：调用我们要检查的函数。
    documents = load_documents_csv(file_path)

    # 3. 检查：先手工写出正确结果，再与实际返回值比较。
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
        {
            "title": "付款规则",
            "department": "财务",
            "approved": False,
            "score": 95,
        },
    ]
    assert documents == expected

    # 专门确认False是布尔值，而非字符串"False"或整数0。
    assert documents[2]["approved"] is False
    assert isinstance(documents[1]["score"], int)


def test_load_documents_csv_header_only(tmp_path):
    """只有表头时，应返回空列表。"""
    file_path = tmp_path / "documents.csv"
    file_path.write_text(
        "title,department,approved,score\n",
        encoding="utf-8",
    )

    documents = load_documents_csv(file_path)

    assert documents == []


def test_load_documents_csv_missing_score_column(tmp_path):
    """缺少score列时，应报错并指出缺少的字段。"""
    file_path = tmp_path / "documents.csv"
    csv_content = (
        "title,department,approved\n"
        "报销流程,财务,True\n"
    )
    file_path.write_text(csv_content, encoding="utf-8")

    # 这里预期函数抛出ValueError，且错误说明中包含score。
    # 如果没有抛出异常，或者异常不符合要求，测试就会失败。
    with pytest.raises(ValueError, match="score"):
        load_documents_csv(file_path)


def test_load_documents_csv_invalid_score(tmp_path):
    """分数不是整数，或者不在0～100之间时，应报错。"""
    file_path = tmp_path / "documents.csv"
    invalid_scores = ["abc", "80.5", "-1", "101"]

    # 每次写入一种错误分数，再检查函数是否拒绝它。
    for invalid_score in invalid_scores:
        csv_content = (
            "title,department,approved,score\n"
            f"报销流程,财务,True,{invalid_score}\n"
        )
        file_path.write_text(csv_content, encoding="utf-8")

        with pytest.raises(ValueError, match="score"):
            load_documents_csv(file_path)


def test_load_documents_csv_invalid_approved(tmp_path):
    """审核状态为无法识别的文字时，应报错。"""
    file_path = tmp_path / "documents.csv"
    csv_content = (
        "title,department,approved,score\n"
        "报销流程,财务,unknown,92\n"
    )
    file_path.write_text(csv_content, encoding="utf-8")

    with pytest.raises(ValueError, match="approved"):
        load_documents_csv(file_path)


def test_load_documents_csv_missing_file(tmp_path):
    """不创建这个文件，检查读取时是否抛出FileNotFoundError。"""
    file_path = tmp_path / "missing.csv"

    with pytest.raises(FileNotFoundError):
        load_documents_csv(file_path)


def test_load_documents_csv_score_boundaries(tmp_path):
    """0分和100分都属于合法范围。"""
    file_path = tmp_path / "documents.csv"
    csv_content = (
        "title,department,approved,score\n"
        "零分资料,财务,True,0\n"
        "满分资料,财务,False,100\n"
    )
    file_path.write_text(csv_content, encoding="utf-8")

    documents = load_documents_csv(file_path)

    assert documents[0]["score"] == 0
    assert documents[1]["score"] == 100
    assert documents[1]["approved"] is False


def test_csv_to_json_round_trip(tmp_path):
    """CSV转JSON后，中文可读，重新读取的内容一致。"""
    csv_path = tmp_path / "documents.csv"
    json_path = tmp_path / "documents.json"
    csv_content = (
        "title,department,approved,score\n"
        "报销流程,财务,True,92\n"
        "付款规则,财务,False,95\n"
    )
    csv_path.write_text(csv_content, encoding="utf-8")

    documents = load_documents_csv(csv_path)
    save_documents(documents, json_path)

    # 检查JSON文件中的中文是直接可读的。
    content = json_path.read_text(encoding="utf-8")
    assert "报销流程" in content

    # 检查完整读回结果，而不只检查文件是否存在。
    loaded_documents = load_documents(json_path)
    assert loaded_documents == documents
    assert loaded_documents[1]["approved"] is False
