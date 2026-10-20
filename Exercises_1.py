documents = [
    {"title": "报销流程", "department": "财务", "approved": True, "score": 92},
    {"title": "发票说明", "department": "财务", "approved": True, "score": 80},
    {"title": "付款规则", "department": "财务", "approved": False, "score": 95},
    {"title": "入职指南", "department": "人事", "approved": True, "score": 76},
    {"title": "账号申请", "department": "技术", "approved": True, "score": 88},
    {"title": "请假制度", "department": "人事", "approved": False, "score": 60},
]
eligibility = []
for document in documents:
    if document["department"] == "财务" and  document["approved"] == True and document["score"] >= 80:
        eligibility.append(document["title"])
if not eligibility:
    print("没有符合条件的资料")
else:
    print(eligibility)
    print(len(eligibility))
eligibility = [document["title"] for document in documents if document["department"] == "财务" and  document["approved"] == True and document["score"] >= 80]
if not eligibility:
    print("没有符合条件的资料")
else:
    print(eligibility)
    print(len(eligibility))
for document in documents:
    if not document["approved"]:document["status"] = "待审核"
    else: document["status"] = "待完善" if document["score"] < 80 else "可用"
    print(document["title"],document["status"])
statistics = {}
for document  in documents:
    if document["department"] not in statistics:
        statistics[document["department"]]={"count":0,"approved":0,"available":0}
    if document["approved"] :  statistics[document["department"]]["approved"] += 1
    if document["approved"] and  document["score"] >= 80: statistics[document["department"]]["available"] += 1
    statistics[document["department"]]["count"] += 1
print(statistics)