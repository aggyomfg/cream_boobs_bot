import sys
import asyncio
import telepot
from telepot.aio.loop import MessageLoop
from telepot.aio.helper import InlineUserHandler, AnswererMixin
from telepot.aio.delegate import per_inline_from_id, create_open, pave_event_space
import random
import json
import requests

"""
$ python3.5 main.py <token>
It answering inline query and getting chosen inline boobs.
"""


class InlineHandler(InlineUserHandler, AnswererMixin):
    def __init__(self, *args, **kwargs):
        super(InlineHandler, self).__init__(*args, **kwargs)

    def on_inline_query(self, msg):
        def compute_answer():
            query_id, from_id, query_string = telepot.glance(msg, flavor='inline_query')
            print(self.id, ':', 'Inline Query:', query_id, from_id, query_string)
            photos = []
            boobs_count = 30
            boobs_photos = get_random_boobs(boobs_count)
            for x in range(0, boobs_count):
                photos.append({'type': 'photo', 'id': random.getrandbits(64), 'thumb_url': str(boobs_photos[x]),
                               'photo_url': str(boobs_photos[x]), 'photo_width': 40, 'photo_height': 40})
            return photos

        self.answerer.answer(msg, compute_answer)

    def on_chosen_inline_result(self, msg):
        from pprint import pprint
        pprint(msg)
        result_id, from_id, query_string = telepot.glance(msg, flavor='chosen_inline_result')
        print(self.id, ':', 'Chosen Inline Result:', result_id, from_id, query_string)


def get_random_boobs(count):
    boobs = []
    response = requests.get('http://api.oboobs.ru/boobs/1/' + str(count) + '/random')
    if response.status_code == 200:
        print(response.status_code, ' OK')
        for entry in range(0, count):
            boobs.append('http://media.oboobs.ru/' + json.loads(response.text)[entry]['preview'])
    else:
        print('Error! Answer is: ', response.status_code)
    return boobs

TOKEN = sys.argv[1]

bot = telepot.aio.DelegatorBot(TOKEN, [
    pave_event_space()(
        per_inline_from_id(), create_open, InlineHandler, timeout=10),
])
loop = asyncio.get_event_loop()

loop.create_task(MessageLoop(bot).run_forever())
print('Listening ...')

loop.run_forever()
