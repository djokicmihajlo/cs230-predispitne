import functools
import time

from flask import Flask, render_template, request

app = Flask(__name__)
cache = {}
last_call = None


def cache_interceptor(function):
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        global last_call

        key = (
            function.__name__,
            args,
            tuple(sorted(kwargs.items())),
        )

        if key in cache:
            last_call = {
                'source': 'Kes',
                'key': key,
            }
            return cache[key]

        result = function(*args, **kwargs)
        cache[key] = result
        last_call = {
            'source': 'Izracunato',
            'key': key,
        }
        return result

    return wrapper


@cache_interceptor
def expensive_square(number):
    time.sleep(1)
    return number * number


@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    number = ''
    error = None

    if request.method == 'POST':
        number = request.form.get('number', '').strip()

        try:
            parsed_number = int(number)
            result = expensive_square(parsed_number)
        except ValueError:
            error = 'Unesite ceo broj.'

    return render_template(
        'index.html',
        number=number,
        result=result,
        error=error,
        last_call=last_call,
        cache_size=len(cache),
        cache_items=cache.items(),
    )


@app.post('/clear')
def clear_cache():
    global last_call

    cache.clear()
    last_call = None
    return render_template(
        'index.html',
        number='',
        result=None,
        error='Kes je obrisan.',
        last_call=last_call,
        cache_size=len(cache),
        cache_items=cache.items(),
    )


if __name__ == '__main__':
    app.run(debug=True)
