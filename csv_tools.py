import csv
import os


def load_documents_csv(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(file_path)
    with open(file_path, 'r', encoding='utf-8') as docreader:
        dic = csv.DictReader(docreader)
        fn_list = dic.fieldnames
        if not fn_list:
            raise ValueError("CSV文件缺少表头！")
        fns = ["title","department","approved","score"]
        re:list = []
        for fn in fns:
            if fn not in fn_list:
                raise ValueError(f"缺少必要的字段:{fn}")
        for row in dic:
            for key in fn_list:
                score:int
                approved: bool
                if key == "score":
                    try:
                        score = int(row[key])
                    except ValueError:
                        raise ValueError("score需要是数字")
                    if score < 0 or score > 100:
                        raise ValueError("score需要在0-100之间")
                    row[key] = score
                elif key == "approved":
                    if row[key].title() == "False":
                        approved = False
                    elif row[key].title() == "True":
                        approved = True
                    else:
                        raise ValueError("approved只能是False或True")
                    row[key] = approved
            re.append(row)
        return re


