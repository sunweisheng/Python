class Document:
    def __init__(self,title,department,approved,score):
        self.title = title
        self.department = department
        self.approved = approved
        self.score = score

    def approve(self):
        self.approved = True

    def is_available(self,min_score):
        return self.approved and self.score >= min_score

doc_a = Document("测试标题A","测试部门A",False,85)
doc_b = Document("测试标题B","测试部门B",False,55)

print(f"标题:{doc_a.title},审核状态：{doc_a.approved}")
print(f"标题:{doc_b.title},审核状态：{doc_b.approved}")

doc_b.approve()

print(f"标题:{doc_a.title},审核状态：{doc_a.approved}")
print(f"标题:{doc_b.title},审核状态：{doc_b.approved}")

print(f"标题:{doc_a.title},是否可用：{doc_a.is_available(80)}")

doc_a.approve()

print(f"标题:{doc_a.title},是否可用：{doc_a.is_available(85)}")