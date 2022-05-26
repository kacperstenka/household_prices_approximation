import requests
import webbrowser
from bs4 import BeautifulSoup

URL = "https://www.otodom.pl/pl/oferty/sprzedaz/dom/wroclaw"
page = requests.get(URL)

#
link_base = []
URL_full = []

#bazy do danych na temat ofert
price_data = []
terrain_area_data = []
house_area_data = []
market_data = []
no_rooms_data = []
building_type_data = []
no_floors_data = []

URL_2 = "https://www.otodom.pl/"

soup = BeautifulSoup(page.content, "html.parser")

#sprawdzenie ile jest stron z ofertami
n_o_pages_text = str(soup.find_all("script", id='__NEXT_DATA__'))
n_o_pages = n_o_pages_text.find('"totalPages":')
n_o_pages = n_o_pages_text[n_o_pages+len('"totalPages":'):n_o_pages+len('"totalPages":')+2]

#uzupełnianie linków do przełączania koljenych stron
URL_add = 'https://www.otodom.pl/pl/oferty/sprzedaz/dom/wroclaw?page='

for i in range(1):#(int(n_o_pages)): #obejrzenie wszystkich ofert ze strony

    link = str(soup.find_all("a", class_="css-rvjxyq es62z2j14"))
    link.find('href="')
    for x in soup.find_all("a", class_="css-rvjxyq es62z2j14"):
        x = str(x)
        x.find('href="')
        x = x[90:180]
        x_end = x.index('"')
        x = x[:x_end]
        link_base.append(x)
        URL_full.append(URL_2+x)
     
    #URL = "https://www.otodom.pl/pl/oferty/sprzedaz/dom/wroclaw"
    
    #soup = BeautifulSoup(page.content, "html.parser")
    for x in range (len(soup.find_all("a", class_="css-rvjxyq es62z2j14"))):
        
        content = requests.get(URL_full[x])
        soup2 = BeautifulSoup(content.content, "html.parser")
        
        #link2 = soup.find("script", id="__NEXT_DATA__")['terrain_area']
        link2 = str(soup2.find_all('script', id="__NEXT_DATA__"))
        #link2 = link2[-50001:-1]
        
        #szukanie i zapisywanie danych do baz
        price_text = '"key":"price","value":"'
        price = (link2.find(price_text))
        price_data.append((link2[price+len(price_text):price+len(price_text)+8]))
        price_data[-1] = price_data[-1][0:price_data[-1].find('"')]
        #W PRZYPADKU BRAKU CENY W ZMIENNEJ price_data OFERTA NIE POSIADA CENY (W OFERCIE WIDNIEJE "ZAPYTAJ O CENĘ")
        
        terrain_area_text = '"key":"terrain_area","value":"'
        terrain_area = (link2.find(terrain_area_text))
        terrain_area_data.append(link2[terrain_area+len(terrain_area_text):terrain_area+len(terrain_area_text)+3])
        if terrain_area_data[-1][0] == 'u':
            terrain_area_data[-1] = 'no info'
        #W PRZYPADKU BRAKU INFORMACJI O ROZMIARZE DZIAŁKI (W OFERCIE WIDNIEJE "ZAPYTAJ O CENĘ") WPISUJEMY "no info"
        
        house_area_text = '"key":"m","value":"'
        house_area = (link2.find(house_area_text))
        house_area_data.append(link2[house_area+len(house_area_text):house_area+len(house_area_text)+3])
        # NA RAZIE NIE WIDZĘ BŁĘDÓW
        
        market_text = '"key":"market","value":"'
        market = (link2.find(market_text))
        market_data.append(link2[market+len(market_text):market+len(market_text)+10])
        market_data[-1] = market_data[-1][0:market_data[-1].find('"')]
        # PO ZNALEZIENIU '"' ZOSTAWIA "primary" BEZ SMIECI
        
        no_rooms_text = '"key":"rooms_num","value":"'
        no_rooms = (link2.find(no_rooms_text))
        no_rooms_data.append(link2[no_rooms+len(no_rooms_text):no_rooms+len(no_rooms_text)+1])
        if no_rooms_data[-1][0] == 'm':
            no_rooms_data[-1] = '>10'
        # W PRZYPADKU WYSTĄPIENIA "m" OZNACZA TO WIĘCEJ NIŻ 10
        
        building_type_text = '"key":"building_type","value":"'
        building_type = (link2.find(building_type_text))
        building_type_data.append(link2[building_type+len(building_type_text):building_type+len(building_type_text)+15])
        if building_type_data[-1][0:2] == 's"':
            building_type_data[-1] = 'no info'
        else:
            building_type_data[-1] = building_type_data[-1][0:building_type_data[-1].find('"')]
        # WARUNEK IF... GDY BRAK INFORMACJI, OSTATNIA LINIJKA DO CZYSZCZENIA SMIECI
        
        no_floors_text = '"label":"floors_num","values":'
        no_floors = (link2.find(no_floors_text))
        no_floors_data.append(link2[no_floors+len(no_floors_text):no_floors+len(no_floors_text)+25])
        if no_floors_data[-1][0:2] == '[]':
            no_floors_data[-1] = 'no info' 
        else:
            no_floors_data[-1] = no_floors_data[-1][2:]
            no_floors_data[-1] = no_floors_data[-1][(no_floors_data[-1].find(':'))+2:no_floors_data[-1].find('"')]
        #MOTYW PODOBNY JAK WYŻEJ
        
    #utworzenie linku do kolejnej strony    
    URL = URL_add + str(i+1)
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")





    