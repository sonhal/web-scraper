"""
Script for searching UiO courses for course titles matching the search query
"""



from bs4 import BeautifulSoup
import requests
import re
import sys

UIO_URL = "https://www.uio.no"


def get_matching_courses_description_links(query, course_list):
    """
    Filters out the courses with titles matching the query text

    :param query: text to search for in course title
    :param course_list: list of course page html elements
    :return: mapping of course name and link to description
    """

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
    """
    Fetches html elements containing UiO course titles and links to descriptions

    :return: list of UiO course page html elements
    """
    with requests.request("get", "https://www.uio.no/studier/program/") as page:
        soup = BeautifulSoup(page.content, features="html.parser")
        course_list = soup.find_all("li", id=re.compile('^vrtx-program-[0-9]*'))

    return course_list


def get_course_description(url):
    """
    Fetches the desctiption text form the link page

    :param url: url to course description page
    :return: str with course description if successful
    """

    try:
        course_page = requests.request("get", url).content
        course_soup = BeautifulSoup(course_page, features="html.parser")
        courses_description = course_soup.find("div", attrs={"class": "vrtx-introduction"})
        return courses_description.find("p").contents[0]

    except Exception:
        return "[Page could not be found]"


def print_result(course_result_map):
    """
    Prints the result data to stdout

    :param course_result_map: Mapping of course name and the tuple containing link to description page and description
    :return: None
    """
    for course, (link, desc) in course_result_map.items():
        print()
        print(f"[{course}]")
        print(f"Link: {link}")
        print(f"Description: {desc}")
        print("_" * 50)


def create_result_map(course_link_map):
    """
    Creates the result dictionary with course name and description link and description text

    :param course_link_map: mapping of course name and link to description
    :return: mapping of key: course name and value: (description link, description text)
    """
    page_desc_map = {}
    for course, link in course_link_map.items():
        page_desc_map[course] = (link, get_course_description(link)) # dict with a tuple of link, description as value
    return page_desc_map


def get_cli_argument():
    """
    Returns the first argument from the user

    :return: str of the first argument
    """
    return sys.argv[1]


if __name__ == "__main__":
    query = get_cli_argument() # get the user query text
    course_list = get_page_courses() # get list of html elements from all UiO courses
    course_link_map = get_matching_courses_description_links(query, course_list) # create dict of course name and link to dessctiption
    result_map = create_result_map(course_link_map) # add the description text from the link to the dict
    print_result(result_map) # print result to the terminal/commandline




