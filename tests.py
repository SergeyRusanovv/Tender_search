import unittest
from unittest.mock import patch
from with_class import GetLinksFromPageTask, GetPrintXmlTask


class TestTasks(unittest.TestCase):

    @patch("with_class.requests.get")
    @patch("with_class.BeautifulSoup")
    def test_get_links_from_page_task(self, mock_bs, mock_requests):
        mock_bs_instance = mock_bs.return_value
        mock_bs_instance.find_all.return_value = [
            {"href": "https://example.com/view.html?id=1"},
            {"href": "https://example.com/someotherlink"},
            {"href": "https://example.com/view.html?id=2"}
        ]

        mock_requests_instance = mock_requests.return_value
        mock_requests_instance.text = "<html><a href='https://example.com/view.html?id=1'></a><a href='https://example.com/someotherlink'></a><a href='https://example.com/view.html?id=2'></a></html>"

        task = GetLinksFromPageTask()
        links = task.run("https://example.com")

        self.assertEqual(links, ["https://example.com/view.html?id=1", "https://example.com/view.html?id=2"])

    @patch("with_class.requests.get")
    def test_get_print_xml_task(self, mock_requests):
        mock_requests_instance = mock_requests.return_value
        mock_requests_instance.text = "<xml>test</xml>"

        task = GetPrintXmlTask()
        result = task.run("https://example.com/view.html?id=1")

        self.assertEqual(result, ["https://example.com/view.html?id=1 - None"])
