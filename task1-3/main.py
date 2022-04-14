import requests
from os.path import join, exists
from pathlib import Path

# from - https://www.bbc.com/mediacentre/speeches/
# Array.prototype.slice.call(document.getElementsByClassName('link')).map(a => a.href)
from bs4 import BeautifulSoup

links = ['https://skorobogatov.livejournal.com/90782.html',
         'https://skorobogatov.livejournal.com/101374.html',
         'https://skorobogatov.livejournal.com/100934.html',
         'https://skorobogatov.livejournal.com/97311.html?utm_source=3userpost',
         'https://skorobogatov.livejournal.com/100840.html?utm_source=3userpost',
         'https://skorobogatov.livejournal.com/100532.html?utm_source=3userpost',
         'https://skorobogatov.livejournal.com/98436.html?utm_source=3userpost',
         'https://skorobogatov.livejournal.com/98565.html?utm_source=3userpost',
         'https://skorobogatov.livejournal.com/88635.html?utm_source=3userpost',
         'https://skorobogatov.livejournal.com/99701.html?utm_source=3userpost',
         'https://skorobogatov.livejournal.com/99299.html?utm_source=3userpost',
         'https://skorobogatov.livejournal.com/97937.html?utm_source=3userpost',
         'https://skorobogatov.livejournal.com/100154.html?utm_source=3userpost',
         'https://skorobogatov.livejournal.com/96558.html?utm_source=3userpost',
         'https://skorobogatov.livejournal.com/96174.html?utm_source=3userpost',
         'https://skorobogatov.livejournal.com/96438.html?utm_source=3userpost',
         'https://skorobogatov.livejournal.com/95471.html?utm_source=3userpost',
         'https://skorobogatov.livejournal.com/66867.html?utm_source=3userpost',
         'https://skorobogatov.livejournal.com/62709.html?utm_source=3userpost',
         'https://skorobogatov.livejournal.com/101418.html?utm_source=3userpost',
         'https://skorobogatov.livejournal.com/67835.html?utm_source=3userpost',
         'https://skorobogatov.livejournal.com/67128.html?utm_source=3userpost',
         'https://skorobogatov.livejournal.com/66134.html?utm_source=3userpost',
         'https://skorobogatov.livejournal.com/65566.html?utm_source=3userpost',
         'https://skorobogatov.livejournal.com/64697.html?utm_source=3userpost',
         'https://skorobogatov.livejournal.com/64158.html?utm_source=3userpost',
         'https://skorobogatov.livejournal.com/60971.html?utm_source=3userpost',
         'https://skorobogatov.livejournal.com/87010.html?utm_source=3userpost',
         'https://skorobogatov.livejournal.com/94631.html?utm_source=3userpost',
         'https://skorobogatov.livejournal.com/54891.html?utm_source=3userpost',
         'https://skorobogatov.livejournal.com/99395.html',
         'https://skorobogatov.livejournal.com/98436.html',
         'https://skorobogatov.livejournal.com/98277.html',
         'https://skorobogatov.livejournal.com/97784.html',
         'https://skorobogatov.livejournal.com/97087.html',
         'https://skorobogatov.livejournal.com/97014.html',
         'https://skorobogatov.livejournal.com/96558.html',
         'https://skorobogatov.livejournal.com/96438.html',
         'https://skorobogatov.livejournal.com/95768.html',
         'https://skorobogatov.livejournal.com/95705.html',
         'https://skorobogatov.livejournal.com/95010.html',
         'https://skorobogatov.livejournal.com/94890.html',
         'https://skorobogatov.livejournal.com/94440.html',
         'https://skorobogatov.livejournal.com/94158.html',
         'https://skorobogatov.livejournal.com/93923.html',
         'https://skorobogatov.livejournal.com/93197.html',
         'https://skorobogatov.livejournal.com/93039.html',
         'https://skorobogatov.livejournal.com/92761.html',
         'https://skorobogatov.livejournal.com/92445.html',
         'https://skorobogatov.livejournal.com/92178.html',
         'https://skorobogatov.livejournal.com/91950.html',
         'https://skorobogatov.livejournal.com/91698.html',
         'https://skorobogatov.livejournal.com/91418.html',
         'https://skorobogatov.livejournal.com/91161.html',
         'https://skorobogatov.livejournal.com/91021.html',
         'https://skorobogatov.livejournal.com/90149.html',
         'https://skorobogatov.livejournal.com/89861.html',
         'https://skorobogatov.livejournal.com/89620.html',
         'https://skorobogatov.livejournal.com/89222.html',
         'https://skorobogatov.livejournal.com/88913.html',
         'https://skorobogatov.livejournal.com/88442.html',
         'https://skorobogatov.livejournal.com/88208.html',
         'https://skorobogatov.livejournal.com/88039.html',
         'https://skorobogatov.livejournal.com/87110.html',
         'https://skorobogatov.livejournal.com/86584.html',
         'https://skorobogatov.livejournal.com/86149.html',
         'https://skorobogatov.livejournal.com/85562.html',
         'https://skorobogatov.livejournal.com/85404.html',
         'https://skorobogatov.livejournal.com/85237.html',
         'https://skorobogatov.livejournal.com/84784.html',
         'https://skorobogatov.livejournal.com/84709.html',
         'https://skorobogatov.livejournal.com/84413.html',
         'https://skorobogatov.livejournal.com/83974.html',
         'https://skorobogatov.livejournal.com/83858.html',
         'https://skorobogatov.livejournal.com/83353.html',
         'https://skorobogatov.livejournal.com/82954.html',
         'https://skorobogatov.livejournal.com/82780.html',
         'https://skorobogatov.livejournal.com/82461.html',
         'https://skorobogatov.livejournal.com/82377.html',
         'https://skorobogatov.livejournal.com/81971.html',
         'https://skorobogatov.livejournal.com/81809.html',
         'https://skorobogatov.livejournal.com/81627.html',
         'https://skorobogatov.livejournal.com/81278.html',
         'https://skorobogatov.livejournal.com/81022.html',
         'https://skorobogatov.livejournal.com/80805.html',
         'https://skorobogatov.livejournal.com/80564.html',
         'https://skorobogatov.livejournal.com/80301.html',
         'https://skorobogatov.livejournal.com/80105.html',
         'https://skorobogatov.livejournal.com/79624.html',
         'https://skorobogatov.livejournal.com/79603.html',
         'https://skorobogatov.livejournal.com/79228.html',
         'https://skorobogatov.livejournal.com/78914.html',
         'https://skorobogatov.livejournal.com/78778.html',
         'https://skorobogatov.livejournal.com/78561.html',
         'https://skorobogatov.livejournal.com/78277.html',
         'https://skorobogatov.livejournal.com/78076.html',
         'https://skorobogatov.livejournal.com/77353.html',
         'https://skorobogatov.livejournal.com/77140.html',
         'https://skorobogatov.livejournal.com/76815.html',
         'https://skorobogatov.livejournal.com/76645.html',
         'https://skorobogatov.livejournal.com/76390.html',
         'https://skorobogatov.livejournal.com/76207.html']

if __name__ == '__main__':
    i = 0
    Path('index.txt').touch()
    with open('index.txt', 'w') as index:
        for link in links:
            response = requests.get(link)
            soup = BeautifulSoup(response.text, 'html.parser')
            site = open(f"sites/{i}.txt", "w", encoding="utf-8")
            article = soup.find('article', {"class": "entry-content"}).get_text(separator=" ").strip()
            h1 = soup.select('h1')[0].text.strip()

            # записываем заголовок статьи и ее содержание
            site.write(f"{h1}\n{article}")
            site.close()
            index.write(f"{i} {link}\n")
            print(i)
            i += 1
    print('done')