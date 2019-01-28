from bs4 import BeautifulSoup
import requests
import re
import sys

UIO_URL = "https://www.uio.no"


def get_matching_courses_description_links(query, course_list):

    course_name_and_link = {}

    for course in course_list:
        try:
            link = course.find("h2").find("a")
        except Exception:
            continue
        link_text= link.contents[0]
        if query in link_text.lower():
            course_name_and_link[link_text] = UIO_URL + link["href"]

    return course_name_and_link



def get_page_courses():
    with requests.request("get", "https://www.uio.no/studier/program/") as page:
        soup = BeautifulSoup(page.content, features="html.parser")
        couse_list = soup.find_all("li", id=re.compile('^vrtx-program-[0-9]*'))

    return couse_list


def get_course_description(url):

    try:
        course_page = requests.request("get", url).content
        course_soup = BeautifulSoup(course_page, features="html.parser")
        courses_description = course_soup.find("div", attrs={"class": "vrtx-introduction"})
        return courses_description.find("p").contents[0]

    except Exception:
        return "[Page could not be found]"


def print_result(page_desc_map):
    for course, (link, desc) in page_desc_map.items():
        print()
        print(f"[{course}]")
        print(f"Link: {link}")
        print(f"Description: {desc}")
        print("_" * 50)


def create_result_map(course_link_map):
    page_desc_map = {}
    for course, link in course_link_map.items():
        page_desc_map[course] = (link, get_course_description(link)) # dict with a tuple of link, description as value
    return page_desc_map


def get_cli_argument():
    return sys.argv[1]


if __name__ == "__main__":
    query = get_cli_argument()
    course_list = get_page_courses()
    course_link_map = get_matching_courses_description_links(query, course_list)
    result_map = create_result_map(course_link_map)
    print_result(result_map)




