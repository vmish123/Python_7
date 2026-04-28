import requests

API_KEY = "6fbfb3e4-1f3a-4421-9d32-58d02b4edacf"
BASE_URL = "https://geocode-maps.yandex.ru/1.x/"


def fetch_geocoder_data(geocode: str, kind: str = None) -> dict:
    # Формирует и отправляет HTTP-запрос к Yandex Geocoder API,
    # выводит ссылку на запрос и возвращает JSON-ответ в виде словаря.
    params = {
        "apikey": API_KEY,
        "geocode": geocode,
        "format": "json"
    }

    # Если передан параметр kind, добавляем его в запрос
    if kind:
        params["kind"] = kind

    # Формируем URL без отправки (для вывода на экран в чистом виде)
    req = requests.Request('GET', BASE_URL, params=params).prepare()
    print(f"Запрос: {req.url}")

    # Выполняем реальный запрос
    response = requests.Session().send(req)

    return response.json()


def get_coordinates(geocode: str) -> tuple:
    # Получает координаты объекта.
    # Возвращает кортеж из двух float: (долгота, широта).

    data = fetch_geocoder_data(geocode)
    # Парсим JSON-ответ Яндекса
    geo_object = data['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']
    # Позиция возвращается строкой "долгота широта"
    coords_str = geo_object['Point']['pos']
    lon, lat = map(float, coords_str.split())
    print(f"Координаты из JSON: долгота {lon}, широта {lat}")
    return lon, lat


def task_a():
    print("a) Якутск и Магадан")
    _, lat_yakutsk = get_coordinates("Якутск")
    _, lat_magadan = get_coordinates("Магадан")

    # Сравниваем широту
    if lat_yakutsk > lat_magadan:
        print("Ответ: Якутск находится севернее.\n")
    else:
        print("Ответ: Магадан находится севернее.\n")


def task_b():
    print("b) Кемерово и Торонто")
    _, lat_kemerovo = get_coordinates("Кемерово")
    _, lat_toronto = get_coordinates("Торонто")

    # Сравниваем широту
    if lat_kemerovo < lat_toronto:
        print("Ответ: Кемерово находится южнее.\n")
    else:
        print("Ответ: Торонто находится южнее.\n")


def task_c():
    print("c) К каким федеральным округам относятся города")
    cities = ["Хабаровск", "Уфа", "Нижний Новгород", "Калининград", "Кемерово"]

    for city in cities:
        data = fetch_geocoder_data(city)

        # Получаем все компоненты адреса (страна, округ, область, город и т.д.)
        components = data['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['metaDataProperty'][
            'GeocoderMetaData']['Address']['Components']

        district = "Федеральный округ не найден"
        for comp in components:
            # Ищем компонент, в названии которого есть словосочетание "федеральный округ"
            if 'федеральный округ' in comp['name'].lower():
                district = comp['name']
                break

        print(f"Ответ для '{city}': {district}\n")


def task_d():
    print("d) Почтовый индекс КемГУ")

    # 1. Пытаемся получить информацию по названию напрямую
    data = fetch_geocoder_data("КемГУ")

    geo_object = data['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']
    address = geo_object['metaDataProperty']['GeocoderMetaData']['Address']
    postal_code = address.get('postal_code')

    # 2. Если геокодер не вернул индекс для "организации", ищем "дом" по координатам КемГУ
    if not postal_code:
        print("Напрямую индекс не найден. Выполняем обратное геокодирование по координатам...")
        coords_str = geo_object['Point']['pos']
        lon, lat = coords_str.split()

        # Делаем запрос по координатам, фильтруя только здания (kind=house)
        house_data = fetch_geocoder_data(f"{lon},{lat}", kind="house")
        house_obj = house_data['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']
        house_address = house_obj['metaDataProperty']['GeocoderMetaData']['Address']

        postal_code = house_address.get('postal_code', 'Индекс так и не найден')

    print(f"Ответ: Почтовый индекс КемГУ: {postal_code}\n")


def main():
    task_a()
    task_b()
    task_c()
    task_d()


main()
