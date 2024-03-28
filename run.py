from celery import group
from with_class import get_links_from_page, get_print_xml
# from with_func import get_links_from_page, get_print_xml

if __name__ == '__main__':

    urls = [
        "https://zakupki.gov.ru/epz/order/extendedsearch/results.html?fz44=on&pageNumber=1",
        "https://zakupki.gov.ru/epz/order/extendedsearch/results.html?fz44=on&pageNumber=2"
    ]

    links_group = group(get_links_from_page.s(url) for url in urls)
    links_results = links_group.delay()

    all_links = links_results.get()

    xml_group = group(get_print_xml.s(link) for link in all_links[0])

    xml_results = xml_group.delay()

    for result in xml_results.get():
        for res in result:
            print(res)

# command: celery -A with_class/with_func worker --loglevel=info
