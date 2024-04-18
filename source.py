from bs4 import BeautifulSoup as bs
import requests

from credentials import s_site, s_url_auth, s_username, s_pass, s_url


def parsing():
    return_data = []
    site = s_site
    url_auth = s_url_auth
    try:
        requests.get(s_site, timeout=10)
        session = requests.Session()

        r = session.get(url_auth)
        soup = bs(r.content, 'html.parser')

        csrf = soup.find('input', {'name': '__RequestVerificationToken'})['value']

        data = {'__RequestVerificationToken': csrf,
                'UserName': s_username,
                'Password': s_pass,
                }
        r = session.post(url_auth, data=data)

        url = s_url
        main_page = session.get(url)
        soup_main = bs(main_page.text, 'html.parser')
        shiprows = soup_main.find_all('tr')
        flag = 0

        for shiptds in shiprows:
            shiptds = shiptds.find_all('td')
            if len(shiptds) == 1:
                place = shiptds[0].text.strip().split("|")[0]
                if (
                    "НМТП" in place
                    or "Шесхарис" in place
                    or "Лесной порт" in place
                    or "НЗТ" in place
                ):
                    return_data.append(f'\n ---- {place} ----')
                    flag = 1
                else:
                    flag = 0
            if len(shiptds) > 1 and flag == 1:
                name = shiptds[1].find('a').text
                detail = site + shiptds[1].find('a').get('href')
                date = shiptds[2].find('div').text.strip()
                operation = shiptds[2].text.strip().split()[0]
                if 'Швартовка' in operation:
                    birth = (shiptds[4].text.replace("- ", "-")
                             .strip().split()[0])
                else:
                    birth = (shiptds[3].text.replace("- ", "-")
                             .strip().split()[0])
                detail_page = session.get(detail)
                soup_detail = bs(detail_page.text, 'html.parser')
                length = (int(soup_detail.find(title='Длина судна')
                              .text.split(',')[0]))
                if length >= 170:
                    return_data.append(f'{name} — Длина: {length} м. — '
                                       f'{date} — {operation} — {birth} \n')

        return return_data
    except (requests.exceptions.Timeout
            and requests.exceptions.HTTPError
            and requests.exceptions.RequestException
            ):
        return_data.append('Отсутствует соединение с сервером. Попробуйте позже.')
        return return_data

print(*parsing(), sep='\n')
