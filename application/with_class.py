from pyexpat import ExpatError
from typing import List, Dict, Any
import requests
from bs4 import BeautifulSoup
import xmltodict
import celery
from celery import Celery
from requests import Response

app = Celery("tasks", broker="redis://localhost:6379", backend="redis://localhost:6379")


class GetLinksFromPageTask(celery.Task):
    """Задача для сбора ссылок с каждой страницы"""
    def run(self, url: str):
        response: Response = requests.get(url)
        soup: BeautifulSoup = BeautifulSoup(response.text, "html.parser")
        links: List[str] = []
        for link in soup.find_all("a", attrs={"target": "_blank"}):
            tender_link: str = link.get("href")
            if tender_link is None:
                continue
            if "view.html" not in tender_link:
                continue
            links.append(tender_link)
        return links


class GetPrintXmlTask(celery.Task):
    """Задача для парсинга печатных XML-форм"""
    def run(self, link: str):
        link: str = f"https://zakupki.gov.ru{link}"
        xml_link: str = link.replace("view.html", "viewXml.html")
        response: Response = requests.get(xml_link)
        xml_content: str = response.text
        returns: List[str] = list()
        if xml_content:
            try:
                xml_dict: Dict[str, Any] = xmltodict.parse(xml_content)
                stack: List[Dict] = [xml_dict]
                while stack:
                    current: Dict[str, Any] = stack.pop()
                    for key, value in current.items():
                        if key == "publishDTInEIS":
                            returns.append(f"{link} - {value}")
                        if isinstance(value, dict):
                            stack.append(value)
                    returns.append(f"{link} - None")
            except ExpatError:
                pass
        return returns


get_links_from_page = app.register_task(GetLinksFromPageTask())
get_print_xml = app.register_task(GetPrintXmlTask())
