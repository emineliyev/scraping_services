import requests
import codecs
from bs4 import BeautifulSoup as BS

__all__ = ('boss', 'elan')

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:47.0) Gecko/20100101 Firefox/47.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
}


def boss(url, city=None, category=None):
    jobs = []
    errors = []
    domain = 'https://boss.az'
    if url:
        resp = requests.get(url, headers=headers)
        if resp.status_code == 200:
            soup = BS(resp.content, 'html.parser')
            div_list = soup.find_all('div', attrs={'class': 'results'})
            if div_list:
                div_item = soup.find_all('div', attrs={'class': 'results-i'})
                for div in div_item:
                    link = div.find('a', attrs={'class': 'results-i-link'})['href']  # Link
                    title = div.find('h3')  # Basliq
                    company = div.find('a', attrs={'class': 'results-i-company'}).text  # Sirket
                    description = div.p.text  # Is haqqinda
                    salary = div.find('div', attrs={'class': 'salary'}).text  # Maas
                    # city = div.find('div', attrs={'class': 'results-i-secondary'}).contents[0]  # Seher
                    # div_secondary = div.find('div', attrs={'class': 'results-i-secondary'}).a
                    # category = div_secondary.find_next_sibling("a").text  # Kateqoriya
                    jobs.append({
                        'url': domain + link,
                        'title': title.text,
                        'company': company,
                        'description': description,
                        'salary': salary,
                        'city_id': city,
                        'category_id': category

                    })
            else:
                errors.append({'url': url, 'title': "Teg div mövcud deyil"})

        else:
            errors.append({'url': url, 'title': "Səhifə cavab vermir"})
    return jobs, errors


def elan(url, city=None, category=None):
    jobs = []
    errors = []
    domain = 'https://www.hellojob.az'
    if url:
        resp = requests.get(url, headers=headers)
        if resp.status_code == 200:
            soup = BS(resp.content, 'html.parser')
            div_list = soup.find_all('div', attrs={'class': 'inner-more-data'})
            if div_list:
                div_item = soup.find_all('div', attrs={'class': 'card_box'})
                for div in div_item:
                    title = div.find('h3')
                    company = div.find('p', attrs={'class': 'company_name'}).text
                    salary = div.find('span', attrs={'class': 'salary'}).text
                    link = div.find('a', attrs={'class': 'full'})['href']
                    jobs.append({
                        'title': title.text,
                        'company': company,
                        'salary': salary,
                        'url': domain + link,
                        'city_id': city,
                        'category_id': category
                    })
            else:
                errors.append({'url': url, 'title': "Teg div mövcud deyil"})

        else:
            errors.append({'url': url, 'title': "Səhifə cavab vermir"})

    return jobs, errors


# if __name__ == '__main__':
#     url = 'https://boss.az/vacancies?utf8=%E2%9C%93&search%5Bcompany_id%5D=&search%5Bcategory_id%5D=48&search%5Bregion_id%5D=1&search%5Bsalary%5D=&search%5Beducation_id%5D=&search%5Bexperience_id%5D=&search%5Bkeyword%5D=&commit=Axtar'
#     jobs, errors = boss(url)
#     h = codecs.open('work.txt', 'w', 'utf-8')
#     h.write(str(jobs))
#     h.close()
