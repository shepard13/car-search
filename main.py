import json
from bottle import run, get, error, request, template, default_app
from paste import httpserver
import psycopg2

application = default_app()
conn = psycopg2.connect("dbname=car-search user=root password=Ek9z32CDUg5xXOmoLYdo host=db")
cur = conn.cursor()
cur.execute("""SELECT * from "cars" """)
rows = cur.fetchall()
print(rows)


def get_file_content():
    with open('data.json', 'r') as f:
        cont = f.read()
        datastore = json.loads(cont)

    return datastore


def get_car(rows, number):
    cars = []
    for car in rows:
        if number in car['n']:
            cars.append(car)
    return cars


def delite_from_bookmark(number):
    bookmark_list = read_from_bookmark()
    for i, car in enumerate(bookmark_list):
        if car['n'] == number:
            bookmark_list.pop(i)


def write_to_bookmark(bookmark):
    with open('bookmark.json', 'w') as data_file:
        json.dump(bookmark, data_file)


def read_from_bookmark():
    with open('bookmark.json') as data_file:
        cars = json.load(data_file)

    return cars


# {'br': 'ПА  004', 'y': '2015', 'col': 'ЗЕЛЕНИЙ', 'n': 'АЕ3999ХМ'}
@get('/cars/')
def search():
    return template('index.html')


@get('/cars/add-bookmark/<c>')
def add_bookmark(c):
    bookmark_list = read_from_bookmark()
    bookmark_list.append(c)
    write_to_bookmark(bookmark_list)
    return template('bookmarks.html', cars=bookmark_list)

@get('/cars/dell-from-bookmark/<c>')
def delite_from_bookmark(c):
    bookmark_list = read_from_bookmark()
    for i, car in enumerate(bookmark_list):
        if car['n'] in c['n']:
            bookmark_list.pop(i)
    return template('bookmarks.html', cars=bookmark_list)


@get('/cars/bookmarks/')
def show_bookmarks():
    cars = read_from_bookmark()
    return template('bookmarks.html', cars=cars)


@get('/cars/get_cars/')
def get_cars():
    number = request.query.number
    cars = get_car(rows, number)
    return template('result_of_search.html', cars=cars)


# @error(404)
# def error404(error):
#     return template('error404.html')
#
#
# @error(408)
# def error408(error):
#     return template('error408.html')
#

if __name__ == '__main__':
    httpserver.serve(application, host='0.0.0.0', port=80)
