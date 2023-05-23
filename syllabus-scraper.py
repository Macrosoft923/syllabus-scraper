import requests
import time
from bs4 import BeautifulSoup
from tqdm import tqdm

session = requests.session()
num = 1

URL = input("URL: ")
# URL = "https://syllabus.sfc.keio.ac.jp/courses?button=&locale=ja&search%5Bobjective%5D=&search%5Bsemester%5D=&search%5Bsfc_guide_title%5D=&search%5Bsub_semester%5D=&search%5Bsummary%5D=&search%5Bteacher_name%5D=&search%5Btitle%5D=&search%5Byear%5D=2023&page="

with open("syllabus.csv", "w", buffering=1) as f:
    time_start = time.time()

    response = session.get(URL + "1")
    soup_ = BeautifulSoup(response.text, "html.parser")

    division = soup_.find("div", class_="result-count")
    strong = division.find("strong")

    found_items = strong.get_text().replace(" ", "")
    items = int(found_items) / 25

    progress_bar = tqdm(total=int(items))
    f.write("科目名, 分野, K-Number\n")
    while num <= items:
        num += 1

        result = session.get(URL + str(num))
        result.encoding = result.apparent_encoding

        soup = BeautifulSoup(result.text, "html.parser")
        list_items = soup.find_all("li")

        progress_bar.update(1)

        for list_item in list_items:
            heading = list_item.find("h2")
            definition_descriptions = list_item.find_all("dd")

            if heading is None:
                continue

            name = heading.get_text().replace(" ", "")
            field = definition_descriptions[3].get_text().replace(" ", "")
            k_number = definition_descriptions[5].get_text().replace(" ", "")

            if any(keyword in field for keyword in ["研究プロジェクト科目", "特別研究（博士）", "研究指導科目"]):
                continue

            f.write(f"{name}, {field}, {k_number}\n")

progress_bar.close()

time_stop = time.time()
elapsed_time = time_stop-time_start

print(f"経過時間は{elapsed_time}秒です。")
