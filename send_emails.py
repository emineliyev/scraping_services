import os, sys
import django
import datetime  # Это биб-ка

from django.core.mail import EmailMultiAlternatives  # Это биб-ка

from django.contrib.auth import get_user_model  # Это импорт модели админ-ра


projects = os.path.dirname(os.path.abspath('manage.py'))  # Это для запуска Django
sys.path.append(projects)  # Это для запуска Django
os.environ["DJANGO_SETTINGS_MODULE"] = "mysite.settings"  # Это для запуска Django

django.setup()  # Это для запуска Django

from crab.models import Vacancy, Error, Url  # Это модели из прилож-я
from mysite.settings import EMAIL_HOST_USER  # Это из settings
ADMIN_USER = EMAIL_HOST_USER

today = datetime.date.today()
subject = f"{today} tarixi üzrə vakansiyaların siyahısı"
text_content = "{today} tarixi üzrə vakansiyaların göndərilməsi"
from_email = EMAIL_HOST_USER

empty = '<h2>Təəsüb ki, Sizin istəkləriniz üzrə bu gün məlumat yoxdu.</h2>'


User = get_user_model()
qs = User.objects.filter(send_email=True).values('city', 'category', 'email')
users_dict = {}

for i in qs:
    users_dict.setdefault((i['city'], i['category']), [])
    users_dict[(i['city'], i['category'])].append(i['email'])

if users_dict:
    params = {'city_id__in': [], 'category_id__in': []}
    for pair in users_dict.keys():
        params['city_id__in'].append(pair[0])
        params['category_id__in'].append(pair[1])
    qs = Vacancy.objects.filter(**params, create_at=today).values()
    vacancies = {}
    # for i in qs:
    #     vacancies.setdefault((i['city_id'], i['category_id']), [])
    #     vacancies[(i['city_id'], i['category_id'])].append(i)
    # for keys, emails in users_dict.items():
    #     rows = vacancies.get(keys, [])
    #     html = ''
    #     for row in rows:
    #         html += f'<h4><a target="_blank" href="{ row["url"] }" class="btn btn-primary">{ row["title"] }</a></h4>'
    #         html += f'<p>{row["description"]}</p>'
    #         html += f'<p>{row["company"]}</p><br><hr>'
    #     _html = html if html else empty
    #     for email in emails:
    #         to = email
    #         msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    #         msg.attach_alternative(_html, "text/html")
    #         msg.send()

qs = Error.objects.filter(create_at=today)
subject = ''
text_content = ''
to = ADMIN_USER
_html = ''

if qs.exists():
    error = qs.first()
    data = error.data.get('errors', [])
    for i in data:
        _html += f'<p><a href="{ i["url"] }">Error: { i["title"] }</a></p>'
    subject = f'{today} tarixi üzrə scrapinq xətaları'
    text_content = "Scrapinq xətaları"
    data = error.data.get('user_data')
    if data:
        _html += '<hr>'
        _html += '<h2>Istifadəçilərin müraciəti</h2>'
    for i in data:
        _html += f'<p>Şəhər: {i["city"]}, Kateqoriya: {i["category"]}, Email: {i["email"]}</p>'
    subject = f'{today} tarixi üzrə istifadəçilərin müraciəti.'
    text_content = "İstifadəçilərin müraciəti."


qs = Url.objects.all().values('city', 'category')
urls_dict = {(i['city'], i['category']): True for i in qs}
urls_errors = ''

for keys in users_dict.keys():
    if keys not in urls_dict:
        if keys[0] and keys[1]:
            urls_errors += f'<p>{keys[0]} şəhər və {keys[1]} kateqoriya üçün urllər mövcud deyil!</p>'

if urls_errors:
    subject += 'Mövcud olmayan urllər'
    _html += urls_errors

if subject:
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(_html, "text/html")
    msg.send()


