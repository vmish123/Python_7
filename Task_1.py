import requests


def fetch_map_image(task_name: str, ll: str, spn: str, l_type: str) -> None:
    # Формирует URL-запрос к Yandex Static Maps API,
    # выводит его в консоль и скачивает изображение.

    # Собираем URL
    url = f"https://static-maps.yandex.ru/1.x/?ll={ll}&spn={spn}&l={l_type}"
    print(f"{task_name}:\nСсылка: {url}")

    response = requests.get(url)

    # Для карты (map) Yandex возвращает PNG, для спутника (sat) - JPG
    ext = "jpg" if l_type == "sat" else "png"
    filename = f"{task_name.split(')')[0].strip()}.{ext}"

    with open(filename, "wb") as file:
        file.write(response.content)

    print(f"Изображение сохранено как '{filename}'\n")


def main():
    # Словарь с параметрами:
    # ll - долгота,широта; spn - масштаб; l - слой (map/sat)
    tasks = {
        "a) Крупномасштабная схема с КемГУ": {
            "ll": "86.092477,55.351107", "spn": "0.005,0.005", "l": "map"
        },
        "b) Схема района": {
            "ll": "86.171865,55.341302", "spn": "0.05,0.05", "l": "map"
        },
        "c) Схема города": {
            "ll": "86.141089,55.344517", "spn": "0.3,0.3", "l": "map"
        },
        "d) Спутниковый снимок Эйфелевой башни": {
            "ll": "2.294481,48.858370", "spn": "0.005,0.005", "l": "sat"
        },
        "e) Спутниковый снимок Авачинского вулкана": {
            "ll": "158.833484,53.255750", "spn": "0.1,0.1", "l": "sat"
        },
        "f) Спутниковый снимок озера Байкал": {
            "ll": "108.000000,53.500000", "spn": "10.0,10.0", "l": "sat"
        },
        "g) Спутниковый снимок космодрома Байконур": {
            "ll": "63.305243,45.964585", "spn": "0.05,0.05", "l": "sat"
        }
    }

    for name, params in tasks.items():
        fetch_map_image(name, params["ll"], params["spn"], params["l"])


main()
