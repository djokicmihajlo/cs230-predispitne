import hashlib

from flask import Flask, render_template, request

app = Flask(__name__)
MAX_TEXT_LENGTH = 255


@app.route('/', methods=['GET', 'POST'])
def index():
    text = ''
    hashed_text = None
    error = None

    if request.method == 'POST':
        text = request.form.get('text', '')

        if len(text) > MAX_TEXT_LENGTH:
            error = 'Tekst ne sme imati vise od 255 karaktera.'
        else:
            hashed_text = hashlib.sha256(text.encode('utf-8')).hexdigest()

    return render_template(
        'index.html',
        text=text,
        hashed_text=hashed_text,
        error=error,
        max_text_length=MAX_TEXT_LENGTH,
    )


if __name__ == '__main__':
    app.run(debug=True)
