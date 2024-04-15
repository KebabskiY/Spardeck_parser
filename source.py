from bs4 import BeautifulSoup as bs
import requests

from credentials import s_login, s_password, s_site, s_url_auth, s_url


def parsing():

    site = s_site
    url_auth = s_url_auth

    session = requests.Session()

    r = session.get(url_auth)
    soup = bs(r.content, 'html.parser')

    csrf = soup.find('input', {'name': '__RequestVerificationToken'})['value']

    data = {'__RequestVerificationToken': csrf,
            'UserName': s_login,
            'Password': s_password,
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
                print("----", place, "----")
                flag = 1
            else:
                flag = 0
        if len(shiptds) > 1 and flag == 1:
            name = shiptds[1].find('a').text
            detail = site + shiptds[1].find('a').get('href')
            shiptype = shiptds[1].find('small').text.replace(".", "")
            date = shiptds[2].find('div').text.strip()
            operation = shiptds[2].text.strip().split()[0]
            if 'Швартовка' in operation:
                birth = shiptds[4].text.replace("- ", "-").strip().split()[0]
            else:
                birth = shiptds[3].text.replace("- ", "-").strip().split()[0]
            detail_page = session.get(detail)
            soup_detail = bs(detail_page.text, 'html.parser')
            length = (float(soup_detail.find(title='Длина судна')
                            .text.replace(",", ".")))
            if length >= 170:
                print(f'{shiptype} {name} -- Длина: {length} -- {date} '
                      f'-- {operation} -- {birth}')


if __name__ == '__main__':
    parsing()
    input()
