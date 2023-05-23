import requests
import time
from bs4 import BeautifulSoup

session = requests.session()
num = 1
# URL = "https://syllabus.sfc.keio.ac.jp/courses?button=&locale=ja&search%5Bobjective%5D=&search%5Bsemester%5D=&search%5Bsfc_guide_title%5D=&search%5Bsub_semester%5D=&search%5Bsummary%5D=&search%5Bteacher_name%5D=&search%5Btitle%5D=&search%5Byear%5D=2022&page="
URL = input("URL:")

time_start = time.time()

with open("syllabus.csv", "w", buffering=1) as f:
    f.write("科目名, 分野, K-Number\n")
    while num <= 111:
        num += 1

        result = session.get(URL+str(num))
        result.encoding = result.apparent_encoding

        soup = BeautifulSoup(result.text, "html.parser")
        list_items = soup.find_all("li")

        for list_item in list_items:
            heading = list_item.find("h2")
            definition_descriptions = list_item.find_all("dd")

            if heading is None:
                continue

            name = heading.get_text().replace(" ", "")
            field = definition_descriptions[3].get_text().replace(" ", "")
            k_number = definition_descriptions[5].get_text().replace(" ", "")

            if "研究プロジェクト科目" in field:
                continue

            f.write(f"{name}, {field}, {k_number}\n")

time_stop = time.time()

elapsed_time = time_stop-time_start
print(f"経過時間は{elapsed_time}秒です。")
