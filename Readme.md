<h3>Сайт государственных закупок (ЕИС), главная страница поиска тендеров: https://zakupki.gov.ru/epz/order/extendedsearch/results.html , с постраничной разбивкой по 10 тендеров.</h3>

<p>Нужно реализовать программу на Python, которая обходит первые две страницы по 44ФЗ:</p>
<ul>
    <li>https://zakupki.gov.ru/epz/order/extendedsearch/results.html?fz44=on&pageNumber=1 </li>
    <li>https://zakupki.gov.ru/epz/order/extendedsearch/results.html?fz44=on&pageNumber=2</li>
</ul>
<p>При обходе, у каждого элемента списка (тендера), нужно собирать ссылку на его печатную форму:</p>

<p>
Эти ссылки имеют вид https://zakupki.gov.ru/epz/order/notice/printForm/view.html?regNumber=0338300047924000057. Заменив view.html на viewXml.html, получим ссылку на печатную XML-форму (https://zakupki.gov.ru/epz/order/notice/printForm/viewXml.html?regNumber=0338300047924000057). 
</p>
<p>Распарсив этот XML, для каждого тендера нужно получить значение XML-поля publishDTInEIS, или None в случае его отсутствия.
Для простоты, результат вывести прямо в консоль (например, обычным print()), в виде пары “ссылка на печатную форму”-”дата публикации”.</p>
Рекомендуемый стек:

    • Python3
    • пакет Requests - https://docs.python-requests.org/en/latest/ для сетевых запросов
    • пакет BeautifulSoup - https://beautiful-soup-4.readthedocs.io/en/latest/ для парсинга HTML и получения ссылок на печатные формы
    • пакет XmlToDict - https://github.com/martinblech/xmltodict для парсинга XML
