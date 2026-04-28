import math
import requests

GEOCODE_API_KEY = "6fbfb3e4-1f3a-4421-9d32-58d02b4edacf"
GEOCODE_URL = "https://geocode-maps.yandex.ru/1.x/"
STATIC_MAPS_URL = "https://static-maps.yandex.ru/1.x/"


def fetch_geocoder(query: str, kind: str = None) -> dict:
    # Отправляет запрос к Геокодеру и возвращает JSON-ответ.
    params = {
        "apikey": GEOCODE_API_KEY,
        "geocode": query,
        "format": "json"
    }
    if kind:
        params["kind"] = kind

    response = requests.get(GEOCODE_URL, params=params)
    response.raise_for_status()
    return response.json()


def get_geo_object(query: str) -> dict:
    # Извлекает первый найденный GeoObject из ответа геокодера.
    data = fetch_geocoder(query)

    return data['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']


def get_coordinates(query: str) -> tuple:
    # Возвращает координаты (долгота, широта) по строке запроса.
    geo_obj = get_geo_object(query)

    if not geo_obj:
        return 0.0, 0.0
    lon, lat = map(float, geo_obj['Point']['pos'].split())
    return lon, lat


def download_static_map(params: dict, filename: str) -> None:
    # Скачивает и сохраняет изображение карты Yandex Static API.

    response = requests.get(STATIC_MAPS_URL, params=params)
    response.raise_for_status()

    with open(filename, "wb") as f:
        f.write(response.content)

    print(f"Изображение сохранено: {filename}")


def lonlat_distance(a: tuple, b: tuple) -> float:
    # Вычисляет расстояние между двумя точками в метрах на сферической Земле.
    # a и b - кортежи (долгота, широта).
    degree_to_meters_factor = 111 * 1000  # 111 километров в метрах

    a_lon, a_lat = a
    b_lon, b_lat = b

    radians_lat = math.radians((a_lat + b_lat) / 2.)
    lat_diff = b_lat - a_lat
    lon_diff = (b_lon - a_lon) * math.cos(radians_lat)

    return math.sqrt(lat_diff ** 2 + lon_diff ** 2) * degree_to_meters_factor


def task_3():
    print("3) Исторический музей Москвы")
    geo_obj = get_geo_object("Москва, Красная площадь, 1")

    address = geo_obj['metaDataProperty']['GeocoderMetaData']['Address']['formatted']
    lon, lat = geo_obj['Point']['pos'].split()

    print(f"Полный адрес: {address}")
    print(f"Координаты: долгота {lon}, широта {lat}")


def task_4():
    print("\n4) Области городов")
    cities = ["Барнаул", "Мелеуз", "Йошкар-Ола"]

    for city in cities:
        geo_obj = get_geo_object(city)
        components = geo_obj['metaDataProperty']['GeocoderMetaData']['Address']['Components']

        # Ищем компонент уровня 'province' (область, край, республика)
        province = "Не определено"
        for comp in components:
            if comp['kind'] == 'province':
                province = comp['name']
                break

        print(f"{city}: {province}")


def task_5():
    print("\n5) Индекс МУРа")

    # Используем сразу kind=house, чтобы точно получить дом с индексом
    data = fetch_geocoder("Москва, Петровка, 38", kind="house")

    geo_obj = data['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']
    postal_code = geo_obj['metaDataProperty']['GeocoderMetaData']['Address'].get('postal_code')

    print(f"Почтовый индекс: {postal_code}")


def task_6():
    print("\n6) Спутниковый снимок Австралии")
    # Для целого континента берем центр материка и большой масштаб
    params = {
        "ll": "133.775136,-25.274398",
        "spn": "40.0,40.0",
        "l": "sat"
    }

    download_static_map(params, "australia.jpg")


def task_7():
    print("\n7) Карта Кемерово с метками")
    places = [
        "Кемерово ЖД Вокзал",
        "Кемерово кардиологический диспансер",
        "Кемерово музей Красная Горка",
        "Кемерово Парк Победы им. Жукова"
    ]

    pts = []
    for place in places:
        lon, lat = get_coordinates(place)
        # Формат маркера: долгота,широта,стиль
        pts.append(f"{lon},{lat},pm2rdm")

    params = {
        "l": "map",
        "pt": "~".join(pts)  # Метки соединяются символом тильды ~
    }
    download_static_map(params, "kemerovo_markers.png")


def task_8():
    print("\n8) Маршрут по Кемеровской области")
    route = ["Кемерово", "Ленинск-Кузнецкий", "Новокузнецк", "Шерегеш"]

    coords = []
    for city in route:
        lon, lat = get_coordinates(city)
        coords.append(f"{lon},{lat}")

    params = {
        "l": "map",
        # Ломаная линия задается параметром pl. Формат: долгота,широта,долгота,широта
        "pl": ",".join(coords)
    }
    download_static_map(params, "kuzbass_route.png")


def task_9():
    print("\n9) Самый южный город")
    user_input = input("Введите список городов через запятую: ")

    cities = [city.strip() for city in user_input.split(",")]
    southernmost_city = None
    min_lat = float('inf')  # Чем меньше широта, тем южнее

    for city in cities:
        lon, lat = get_coordinates(city)
        if lat != 0.0 and lat < min_lat:
            min_lat = lat
            southernmost_city = city

    print(f"Самый южный город из списка: {southernmost_city}")


def task_10():
    print("\n10) Длина пути и карта")
    # Последовательность точек:
    # Томск -> Новосибирск -> Омск
    points = [
        (84.948197, 56.484640),
        (82.920430, 55.030199),
        (73.368599, 54.989342)
    ]

    total_length = 0.0
    for i in range(len(points) - 1):
        total_length += lonlat_distance(points[i], points[i + 1])

    print(f"Общая длина пути: {total_length / 1000:.2f} км")

    # Формируем строку для линии
    pl_coords = []
    for lon, lat in points:
        pl_coords.append(f"{lon},{lat}")

    # Средняя точка
    mid_index = len(points) // 2
    mid_lon, mid_lat = points[mid_index]

    params = {
        "l": "map",
        "pl": ",".join(pl_coords),
        "pt": f"{mid_lon},{mid_lat},pm2blm"  # Синяя метка в средней точке
    }
    download_static_map(params, "path_with_marker.png")


def main():
    task_3()
    task_4()
    task_5()
    task_6()
    task_7()
    task_8()
    task_9()
    task_10()


main()
