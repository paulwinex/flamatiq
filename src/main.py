from dramatiq_abort.middleware import AbortMode
from flask import Flask, redirect
from dramatiq.results import Results, errors
from dramatiq.brokers.redis import RedisBroker
from dramatiq.results.backends import RedisBackend
from flask_dramatiq import Dramatiq
from dramatiq.middleware import default_middleware
from periodiq import PeriodiqMiddleware, cron
from dramatiq import set_broker
from dramatiq.encoder import PickleEncoder
from dramatiq_abort import Abortable, backends, abort, Abort
import os


# SETUP

REDIS_HOST = os.getenv('REDIS_HOST') or (os.getenv('APP_NAME')+'-redis' if os.getenv('APP_NAME') else None) or 'localhost'
BROKER_URL = f"redis://{REDIS_HOST}:6379/0"

periodiq_mw = PeriodiqMiddleware()
abort_mw = Abortable(backend=backends.RedisBackend.from_url(BROKER_URL))
result_backend = RedisBackend(url=BROKER_URL, encoder=PickleEncoder)
result_mw = Results(backend=result_backend)
middlewares = [m() for m in default_middleware] + [periodiq_mw, abort_mw, result_mw]
redis_broker = RedisBroker(url=BROKER_URL, middleware=[result_mw, abort_mw])
set_broker(redis_broker)

app = Flask(__name__)
app.config['DRAMATIQ_BROKER'] = 'dramatiq.brokers.redis:RedisBroker'
app.config['DRAMATIQ_BROKER_URL'] = BROKER_URL
dq = Dramatiq(app, middleware=middlewares)


# TASKS
@dq.actor()
def simple_tasks():
    print(f'{">"*10} Simple task executed!')


@dq.actor(periodic=cron('* * * * *'))
def daily_tasks():
    # call every minute
    print(f"{'>'*10} Periodic task executed!")


@dq.actor(abortable=True)
def long_task():
    import time
    try:
        # YOUR STUFF #############
        for i in range(10):
            print(i, flush=True)
            time.sleep(1)
        ##########################
    except Abort:
        print('CANCELED', flush=True)
        raise


@dq.actor(store_results=True)
def compute_with_result():
    import time, random
    time.sleep(3)
    return random.randrange(0, 100)

# VIEWS


index_link = '<a href="/">Index</a><br><br>'


@app.route("/")
def index():
    return index_link+'<a href="/start">Start simple task</a> <br> '\
                      '<a href="/start_long">Start abortable task</a> <br> ' \
                      '<a href="/compute">Start task with result</a>'


@app.route("/start")
def simple():
    simple_tasks.send()
    return redirect("/", code=302)


@app.route("/start_long")
def start():
    message = long_task.send()
    print('Started long task', message.message_id, flush=True)
    return index_link+f'Started: {message.message_id} <br><a href="/stop/{message.message_id}">STOP</a>'


@app.route("/stop/<task_id>")
def stop(task_id):
    print('STOP TASK', task_id, flush=True)
    abort(task_id, mode=AbortMode.ABORT)
    return index_link+'Canceled'


@app.route("/compute")
def start_with_result():
    message = compute_with_result.send()
    print('Started task with result', message.message_id, flush=True)
    return index_link+f'Started: {message.message_id} <br><a href="/result/{message.message_id}">Check Result</a>'


@app.route("/result/<task_id>")
def get_result(task_id):
    # restore message
    message = compute_with_result.message().copy(message_id=task_id)
    try:
        # try to get result
        res = message.get_result(block=False)
    except errors.ResultMissing:
        res = 'Not ready...'
    return index_link+f'Result: {res}'
