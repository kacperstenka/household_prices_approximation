import requests
import webbrowser
from bs4 import BeautifulSoup
import re
import csv

###
csv_name = 'NewDataset'
csv_path = f'C:/Users/Mati/Desktop/HousePrices/DataToSoup/{csv_name}.csv'
csv_name_links = 'LinkiDoStron'
csv_path_links = f'C:/Users/Mati/Desktop/HousePrices/DataToSoup/{csv_name_links}.csv'
small_flag = False
#Liczba probek zapisanych do pliku csv
number_of_samples = 10
###

URL = "https://www.otodom.pl/pl/oferty/sprzedaz/dom/wroclaw"
page = requests.get(URL)

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
construction_status_data = []
build_year_data = []
building_material_data = []
roof_type_data = []
heating_type_data = []
extras_data = []
security_data = []
media_data = []



URL_2 = "https://www.otodom.pl/"

soup = BeautifulSoup(page.content, "html.parser")

#sprawdzenie ile jest stron z ofertami
n_o_pages_text = str(soup.find_all("script", id='__NEXT_DATA__'))
n_o_pages = n_o_pages_text.find('"totalPages":')
n_o_pages = n_o_pages_text[n_o_pages+len('"totalPages":'):n_o_pages+len('"totalPages":')+2]

#uzupełnianie linków do przełączania kolejnych stron
URL_add = 'https://www.otodom.pl/pl/oferty/sprzedaz/dom/wroclaw?page='
for i in range(int(n_o_pages)): #obejrzenie wszystkich ofert ze strony
    link = str(soup.find_all("li", class_="css-p74l73 es62z2j19"))
    link.find('href="')
    remove_first_step = 0
    for x in soup.find_all("li", class_="css-p74l73 es62z2j19"):
        if remove_first_step > 0:
            x = str(x)
            x = x[0:180] #narrow the found text
            x_start = x.index('href="') #after this expression we can find the link
            x_end = x.index('"><aside') #expression right after the link
            x = x[x_start+7:x_end] #link
            link_base.append(x)
            URL_full.append(URL_2+x)
        remove_first_step = 1
     
    #URL = "https://www.otodom.pl/pl/oferty/sprzedaz/dom/wroclaw"
    
    #soup = BeautifulSoup(page.content, "html.parser")
    for x in range (len(soup.find_all("li", class_="css-p74l73 es62z2j19")) - 1):
        content = requests.get(URL_full[x])
        soup2 = BeautifulSoup(content.content, "html.parser")
        
        link2 = str(soup2.find_all('script', id="__NEXT_DATA__"))
        
        #szukanie i zapisywanie danych do baz
        price_text = '"key":"price","value":"'
        price = (link2.find(price_text))
        price_data.append((link2[price+len(price_text):price+len(price_text)+12]))
        if len(price_data[-1]) != 0:
            if price_data[-1][0].isdigit():
                price_data[-1] = price_data[-1][0:price_data[-1].find('"')]
            else:
                price_data[-1] = 'no info'
        else:
            price_data[-1] = 'no info'
        #W PRZYPADKU BRAKU CENY W ZMIENNEJ price_data OFERTA NIE POSIADA CENY (W OFERCIE WIDNIEJE "ZAPYTAJ O CENĘ")




        terrain_area_text = '"key":"terrain_area","value":"'
        terrain_area = (link2.find(terrain_area_text))
        terrain_area_data.append(link2[terrain_area+len(terrain_area_text):terrain_area+len(terrain_area_text)+4])
        if len(terrain_area_data[-1]) != 0:
            if terrain_area_data[-1][0] == 'u':
                terrain_area_data[-1] = 'no info'
            else:
                terrain_area_data[-1] = terrain_area_data[-1][0:terrain_area_data[-1].find('"')]
        else:
            terrain_area_data[-1] = 'no info'
        #W PRZYPADKU BRAKU INFORMACJI O ROZMIARZE DZIAŁKI (W OFERCIE WIDNIEJE "ZAPYTAJ O CENĘ") WPISUJEMY "no info"
        
        house_area_text = '"key":"m","value":"'
        house_area = (link2.find(house_area_text))
        house_area_data.append(link2[house_area+len(house_area_text):house_area+len(house_area_text)+4])
        house_area_data[-1] = house_area_data[-1][0:house_area_data[-1].find('"')]
        if len(house_area_data[-1]) == 0:
            house_area_data[-1] = 'no info'
        # NA RAZIE NIE WIDZĘ BŁĘDÓW
        
        market_text = '"key":"market","value":"'
        market = (link2.find(market_text))
        market_data.append(link2[market+len(market_text):market+len(market_text)+10])
        market_data[-1] = market_data[-1][0:market_data[-1].find('"')]
        if len(market_data[-1]) == 0:
            market_data[-1] = 'no info'        
        # PO ZNALEZIENIU '"' ZOSTAWIA "primary" BEZ SMIECI
        
        no_rooms_text = '"key":"rooms_num","value":"'
        no_rooms = (link2.find(no_rooms_text))
        no_rooms_data.append(link2[no_rooms+len(no_rooms_text):no_rooms+len(no_rooms_text)+1])
        if len(no_rooms_data[-1]) != 0:
            if no_rooms_data[-1][0] == 'm':
                no_rooms_data[-1] = '>10'
        else:
            no_rooms_data[-1] = 'no info'
        # W PRZYPADKU WYSTĄPIENIA "m" OZNACZA TO WIĘCEJ NIŻ 10
        
        building_type_text = '"key":"building_type","value":"'
        building_type = (link2.find(building_type_text))
        building_type_data.append(link2[building_type+len(building_type_text):building_type+len(building_type_text)+15])
        if len(building_type_data[-1]) != 0:
            if building_type_data[-1][0:2] == 's"':
                building_type_data[-1] = 'no info'
            else:
                building_type_data[-1] = building_type_data[-1][0:building_type_data[-1].find('"')]
        else:
            building_type_data[-1] = 'no info'
        # WARUNEK IF... GDY BRAK INFORMACJI, OSTATNIA LINIJKA DO CZYSZCZENIA SMIECI
        
        no_floors_text = '"label":"floors_num","values":'
        no_floors = (link2.find(no_floors_text))
        no_floors_data.append(link2[no_floors+len(no_floors_text):no_floors+len(no_floors_text)+25])
        if len(no_floors_data[-1]) != 0:
            if no_floors_data[-1][0:2] == '[]':
                no_floors_data[-1] = 'no info' 
            else:
                no_floors_data[-1] = no_floors_data[-1][2:]
                no_floors_data[-1] = no_floors_data[-1][(no_floors_data[-1].find(':'))+2:no_floors_data[-1].find('"')]
        else:
            no_floors_data[-1] = 'no info'
        #MOTYW PODOBNY JAK WYŻEJ
        
        construction_status_text = '"key":"construction_status","value":"'
        construction_status = (link2.find(construction_status_text))
        construction_status_data.append(link2[construction_status+len(construction_status_text):construction_status+len(construction_status_text)+20])
        if len(construction_status_data[-1]) != 0:
            construction_status_data[-1] = construction_status_data[-1][0:construction_status_data[-1].find('"')]
        if len(construction_status_data[-1]) == 0:
            construction_status_data[-1] = 'no info'
        #MOTYW PODOBNY JAK WYŻEJ
           
        build_year_text = '"key":"build_year","value":"'
        build_year = (link2.find(build_year_text))
        build_year_data.append((link2[build_year+len(build_year_text):build_year+len(build_year_text)+6]))
        if len(build_year_data[-1]) != 0:
            if build_year_data[-1][0].isdigit():
                build_year_data[-1] = build_year_data[-1][0:build_year_data[-1].find('"')]
            else:
                build_year_data[-1] = 'no info'
        else:
            build_year_data[-1] = 'no info'
        #MOTYW PODOBNY JAK WYŻEJ
        
        building_material_text = '"Building_material":["'
        building_material = (link2.find(building_material_text))
        building_material_data.append(link2[building_material+len(building_material_text):building_material+len(building_material_text)+20])
        if len(building_material_data[-1]) != 0:
            building_material_data[-1] = building_material_data[-1][0:building_material_data[-1].find('"')]
        if len(building_material_data[-1]) == 0:
            building_material_data[-1] = 'no info'
        #MOTYW PODOBNY JAK WYŻEJ
        
        roof_type_text = '"Roof_type":["'
        roof_type = (link2.find(roof_type_text))
        roof_type_data.append(link2[roof_type+len(roof_type_text):roof_type+len(roof_type_text)+20])
        if len(roof_type_data[-1]) != 0:
            roof_type_data[-1] = roof_type_data[-1][0:roof_type_data[-1].find('"')]
        if roof_type_data[-1] == 'sorigin=':
            roof_type_data[-1] = 'no info'    
        #MOTYW PODOBNY JAK WYŻEJ
        
        heating_type_text = '"Heating_types":["'
        heating_type = (link2.find(heating_type_text))
        heating_type_data.append(link2[heating_type+len(heating_type_text):heating_type+len(heating_type_text)+20])
        if len(heating_type_data[-1]) != 0:
            heating_type_data[-1] = heating_type_data[-1][0:heating_type_data[-1].find('"')]
        if heating_type_data[-1] == 'gin=':
            heating_type_data[-1] = 'no info'    
        #MOTYW PODOBNY JAK WYŻEJ
                      
        extras_text = '"Extras_types":["'
        extras = (link2.find(extras_text))
        extras_data.append(link2[extras+len(extras_text):extras+len(extras_text)+60])
        if len(extras_data[-1]) != 0:
            extras_data[-1] = extras_data[-1][0:extras_data[-1].find(']')]
        if extras_data[-1][0:5] == 'igin=' or extras_data[-1] == '':
            extras_data[-1] = 'no info'
        #MOTYW PODOBNY JAK WYŻEJ
        
        #tutaj wyszukujemy niepotrzebne cudzysłowy (chyba tak się to odmienia?) i zamieniamy je na spacje, albo na puste pola
        index_to_change = [m.start() for m in re.finditer('"', extras_data[-1])]
        var = 0
        var_str = extras_data[-1]
        var_str = list(var_str)
        for j in range(len(index_to_change)):
            if var%2 == 0:
                var_str[index_to_change[j]] = ''
            elif var%2 == 1:
                var_str[index_to_change[j]] = ' '
            var += 1
        extras_data[-1] = var_str
        extras_data[-1] = ''.join(extras_data[-1])
        
        security_text = '"Security_types":["'
        security = (link2.find(security_text))
        security_data.append(link2[security+len(security_text):security+len(security_text)+100])
        if len(security_data[-1]) != 0:
            security_data[-1] = security_data[-1][0:security_data[-1].find(']')]
        if security_data[-1][0:3] == 'in=':
            security_data[-1] = 'no info'
        #MOTYW PODOBNY JAK WYŻEJ
        
        #tutaj wyszukujemy niepotrzebne cudzysłowy (chyba tak się to odmienia?) i zamieniamy je na spacje, albo na puste pola
        index_to_change = [m.start() for m in re.finditer('"', security_data[-1])]
        var = 0
        var_str = security_data[-1]
        var_str = list(var_str)
        for j in range(len(index_to_change)):
            if var%2 == 0:
                var_str[index_to_change[j]] = ''
            elif var%2 == 1:
                var_str[index_to_change[j]] = ' '
            var += 1
        security_data[-1] = var_str
        security_data[-1] = ''.join(security_data[-1])    
    
        media_text = '"media_types","values":["'
        media = (link2.find(media_text))
        media_data.append(link2[media+len(media_text):media+len(media_text)+200])
        if len(media_data[-1]) != 0:
            media_data[-1] = media_data[-1][0:media_data[-1].find(']')]
        if media_data[-1][0:3] == 'ony':
            media_data[-1] = 'no info'
        #MOTYW PODOBNY JAK WYŻEJ
        
        #tutaj wyszukujemy niepotrzebne cudzysłowy (chyba tak się to odmienia?) i zamieniamy je na spacje, albo na puste pola
        media_data[-1] = media_data[-1].replace('media_types::', '')
        index_to_change = [m.start() for m in re.finditer('"', media_data[-1])]
        var = 0
        var_str = media_data[-1]
        var_str = list(var_str)
        for j in range(len(index_to_change)):
            if var%2 == 0:
                var_str[index_to_change[j]] = ''
            elif var%2 == 1:
                var_str[index_to_change[j]] = ' '
            var += 1
        media_data[-1] = var_str
        media_data[-1] = ''.join(media_data[-1])

        if (x == number_of_samples):
            small_flag = True
            break;

    if (small_flag == True):
        break;
                
    #utworzenie linku do kolejnej strony    
    URL = URL_add + str(i+1)
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")



with open(csv_path, 'w+', newline='') as csvFile:
    writer = csv.writer(csvFile)
    for row in range(0, number_of_samples):
        if(row == 0):
            writer.writerow(["price_data","terrain_area_data","house_area_data","market_data","no_rooms_data",
                            "building_type_data","no_floors_data","construction_status_data","build_year_data","building_material_data",
                            "roof_type_data","heating_type_data","extras_data","security_data","media_data"])
        writer.writerow([price_data[row],terrain_area_data[row],house_area_data[row],market_data[row],no_rooms_data[row]
                            ,building_type_data[row],no_floors_data[row],construction_status_data[row],build_year_data[row],building_material_data[row],
                         roof_type_data[row],heating_type_data[row],extras_data[row],security_data[row],media_data[row]])

with open(csv_path_links, 'w+', newline='') as csvFile:
    writer = csv.writer(csvFile)
    for row in range(0, number_of_samples):
        if(row == 0):
            writer.writerow(["URL_full"])
        writer.writerow([URL_full[row]])