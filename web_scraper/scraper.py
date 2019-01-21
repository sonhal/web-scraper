from bs4 import BeautifulSoup
import requests
import re

uio_url = "https://www.uio.no"

with requests.request("get", "https://www.uio.no/studier/program/") as page:
    soup = BeautifulSoup(page.content, "html")


    courses_descriptions = []
    couse_list = soup.find_all("li", id=re.compile('^vrtx-program-[0-9]*'))
    for el in couse_list:
        try:
            link = el.find("h2").find("a")
            course_page = requests.request("get", uio_url + link["href"]).content
            course_soup = BeautifulSoup(course_page, "html")
            courses_description = course_soup.find("div", attrs={"class": "vrtx-introduction"})
            courses_descriptions.append(courses_description)
        except Exception:
            pass

    for page in courses_descriptions:
        print(page)



