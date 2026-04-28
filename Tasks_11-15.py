import random
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup


def task_11():
    # Выводит на экран все ссылки со страницы,
    # ориентируясь на атрибут href у тега a.
    print("11) Парсинг ссылок")
    url = "http://olympus.realpython.org/profiles"
    response = requests.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')

    for a_tag in soup.find_all('a', href=True):
        # urljoin склеивает базовый URL с относительным путем (href)
        full_link = urljoin(url, a_tag['href'])
        print(full_link)


def task_12():
    # Собирает всех авторов цитат с многостраничного сайта
    # и выводит их, отсортировав по убыванию количества цитат.
    print("\n12) Авторы по количеству цитат")
    url = "https://quotes.toscrape.com/"
    authors_counts = {}

    # Парсим все страницы, пока есть кнопка "Next"
    while url:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Находим всех авторов на текущей странице
        for author_tag in soup.select('.author'):
            author_name = author_tag.text.strip()
            authors_counts[author_name] = authors_counts.get(author_name, 0) + 1

        # Ищем кнопку перехода на следующую страницу
        next_btn = soup.select_one('li.next > a')
        if next_btn:
            url = urljoin("https://quotes.toscrape.com/", next_btn['href'])
        else:
            url = None

    # Сортируем словарь по значениям (количеству цитат) в порядке убывания
    sorted_authors = sorted(
        authors_counts.items(),
        key=lambda item: item[1],
        reverse=True
    )

    for author, count in sorted_authors:
        print(f"{author}: {count} цитат(ы)")


def task_13():
    # Выводит пять случайных цитат с многостраничного сайта.
    print("\n13) 5 случайных цитат")
    url = "https://quotes.toscrape.com/"
    all_quotes = []

    while url:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        for quote_block in soup.select('.quote'):
            text = quote_block.select_one('.text').text
            author = quote_block.select_one('.author').text
            all_quotes.append(f"{text} — {author}")

        next_btn = soup.select_one('li.next > a')
        url = urljoin("https://quotes.toscrape.com/", next_btn['href']) if next_btn else None

    # Выбираем 5 случайных цитат из собранного списка
    random_selection = random.sample(all_quotes, min(5, len(all_quotes)))
    for idx, quote in enumerate(random_selection, 1):
        print(f"{idx}. {quote}")


def task_14():
    # Принимает от пользователя теги и выводит все цитаты с этими тегами.
    print("\n14) Поиск цитат по тегам")
    user_input = input("Введите теги через пробел: ")

    # Очищаем ввод и переводим в нижний регистр
    target_tags = set(
        tag.lower().strip()
        for tag in user_input.split()
        if tag.strip()
    )

    if not target_tags:
        print("Теги не введены.")
        return

    url = "https://quotes.toscrape.com/"
    matching_quotes = []

    while url:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        for quote_block in soup.select('.quote'):
            tags_on_quote = set(tag.text.lower() for tag in quote_block.select('.tag'))

            # Если все введенные теги (target_tags) присутствуют в тегах цитаты
            if target_tags.issubset(tags_on_quote):
                text = quote_block.select_one('.text').text
                author = quote_block.select_one('.author').text
                matching_quotes.append(f"{text} — {author}")

        next_btn = soup.select_one('li.next > a')
        url = urljoin("https://quotes.toscrape.com/", next_btn['href']) if next_btn else None

    if matching_quotes:
        for q in matching_quotes:
            print(q)
    else:
        print("Цитаты с такими тегами не найдены.")


def task_15():
    print("Сайт не существует")


def main():
    task_11()
    task_12()
    task_13()
    task_14()


main()
