from flask import Flask, flash, g, make_response, redirect, render_template, request
import os
from secrets import token_bytes

from .dfa import Dfa
from .utils import sign, verify, dump_dict, parse_dict

app = Flask(__name__)
app.secret_key = token_bytes(16)
KEY = token_bytes(16)
FLAG = os.getenv('FLAG') or 'TUDCTF{dummy_flag}'
DFA = Dfa({'s0', 's1', 's2'}, '01', {
    ('s0', '0'): 's0', ('s0', '1'): 's1',
    ('s1', '0'): 's2', ('s1', '1'): 's0',
    ('s2', '0'): 's1', ('s2', '1'): 's2'
}, 's0', {'s0'})


@app.before_request
def _():
    signature = request.cookies.get('signature')
    if signature is None:
        g.number = None
        return

    data = verify(KEY, signature)
    if data is None:
        g.number = None
        return
    
    try:
        g.number = int(parse_dict(data.decode('ibm437')).get('word'), 2)
    except ValueError:
        g.number = None


@app.get('/')
def index():
    ctx = {'number': g.number}
    return render_template('index.html', **ctx)


@app.post('/sign')
def sign_number():
    number = request.form.get('number')
    if number is None:
        flash(('error', 'Invalid request'))
        return redirect('/', 303)
    try:
        number = int(number)
    except ValueError:
        flash(('error', 'Input is not a number'))
        return redirect('/', 303)
    word = f'{number:b}'
    if not DFA.accepts(word):
        flash(('error', 'The DFA does not accept this word'))
        return redirect('/', 303)
    flash(('ok', 'The DFA accepts this word'))
    resp = make_response(redirect('/', 303))
    resp.set_cookie('signature', sign(KEY, dump_dict({'word': word}).encode('ibm437')))
    return resp


@app.post('/verify')
def verify_number():
    if g.number is None:
        return 'Invalid signature'

    if g.number % 3 == 0:
        flash(('ok', 'As expected'))
        return redirect('/', 303)
    else:
        flash(('ok', FLAG))
        return redirect('/', 303)


if __name__ == '__main__':
    app.run()
