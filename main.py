import json
from bottle import run, get, error, request, template, default_app
from paste import httpserver
import psycopg2

application = default_app()

connection = psycopg2.connect(dbname='car-search',
                              user='root',
                              password='Ek9z32CDUg5xXOmoLYdo',
                              host='db',
                              port='5432')

cursor = connection.cursor()


def db_get_cars(number):
    # TODO: SQL escaping
    cursor.execute(f"""SELECT * FROM public.cars WHERE "plate-number" LIKE '%{number}%';""")

    return cursor.fetchall()


def db_get_bookmarked_cars():
    cursor.execute("""SELECT * FROM public.cars WHERE "bookmarked" IS TRUE;""")

    return cursor.fetchall()


def db_add_bookmark(plate_number):
    cursor.execute("""UPDATE public.cars SET "bookmarked" = TRUE WHERE "plate-number" = %s;""", (plate_number,))

    connection.commit()


def db_delete_bookmark(plate_number):
    cursor.execute("""UPDATE public.cars SET "bookmarked" = FALSE WHERE "plate-number" = %s;""", (plate_number,))

    connection.commit()


@get('/cars/')
def search():
    return template('index.html')


@get('/cars/add-bookmark/')
def add_bookmark():
    number = request.query.plate_number
    db_add_bookmark(number)

    cars = db_get_bookmarked_cars()
    return template('bookmarks.html', cars=cars)


@get('/cars/dell-from-bookmark/')
def delete_from_bookmark():
    number = request.query.plate_number
    db_delete_bookmark(number)
    cars = db_get_bookmarked_cars()

    return template('bookmarks.html', cars=cars)


@get('/cars/bookmarks/')
def show_bookmarks():
    cars = db_get_bookmarked_cars()
    return template('bookmarks.html', cars=cars)


@get('/cars/get_cars/')
def get_cars():
    number = request.query.number

    cars = db_get_cars(number)

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