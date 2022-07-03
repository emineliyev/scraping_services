import asyncio
import codecs
import os, sys
import datetime as dt

from django.contrib.auth import get_user_model
from django.db import DatabaseError

projects = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(projects)
os.environ["DJANGO_SETTINGS_MODULE"] = "mysite.settings"

import django

django.setup()

from crab.parser import *
from django.contrib.auth.models import User

from crab.models import City, Category, Vacancy, Error, Url

User = get_user_model()

parser = (
    (boss, 'boss'),
    (elan, 'elan'),
)
jobs, errors = [], []


def get_settings():
    qs = User.objects.filter(send_email=True).values()
    settings_list = set((q['city_id'], q['category_id']) for q in qs)
    return settings_list


def get_urls(_settings):
    qs = Url.objects.all().values()
    url_dict = {(q['city_id'], q['category_id']): q['url_data'] for q in qs}
    urls = []
    for pair in _settings:
        if pair in url_dict:
            tmp = {}
            tmp['city'] = pair[0]
            tmp['category'] = pair[1]
            tmp['url_data'] = url_dict[pair]
            urls.append(tmp)
    return urls


async def func_main(value):
    func, url, city, category = value
    job, err = await loop.run_in_executor(None, func, url, city, category)
    errors.extend(err)
    jobs.extend(job)

settings = get_settings()
url_list = get_urls(settings)

loop = asyncio.new_event_loop()
tmp_task = [(func, data['url_data'][key], data['city'], data['category'])
            for data in url_list
            for func, key in parser]

tasks = asyncio.wait([loop.create_task(func_main(f)) for f in tmp_task])

# for data in url_list:
#     for func, key in parser:
#         url = data['url_data'][key]
#         j, e = func(url, city=data['city'], category=data['category'])
#         jobs += j
#         errors += e

loop.run_until_complete(tasks)
loop.close()
for job in jobs:
    v = Vacancy(**job)
    try:
        v.save()
    except DatabaseError:
        pass

if errors:
    qs = Error.objects.filter(create_at=dt.date.today())
    if qs.exists():
        err = qs.first()
        err.data.update({'errors': errors})
        err.save()
    else:
        error = Error(data=f'errors: {errors}').save()

# h = codecs.open('work.txt', 'w', 'utf-8')
# h.write(str(jobs))
# h.close()
