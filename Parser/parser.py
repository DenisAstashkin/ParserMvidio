import requests
from requests import Request
from datetime import datetime
import os
from conf.config import *
from sys import argv
import sys
import math
sys.path.insert(1, os.path.join('D:\\C++\\ParserExampleMvidio\\DBManager'))
from manager import Manager
sys.path.insert(1, os.path.join('D:\\C++\\ParserExampleMvidio\\DBManager\\Model'))
from model import Item, Image


def CreatePath() -> str:    
    if len(argv) > 1:       
        Path = argv[1]
        if Path[len(Path) - 1] != '\\':            
            Path += '\\'
    else:
        Path = argv[0]
        Path = Path.replace(os.path.basename(__file__), '')
    return Path


PATH = CreatePath()
PATH = PATH.replace(PATH[0], PATH[0].upper())


def GetRespJson(TypeReq: str, URL: str, json = None, params=None):     
    
    session = requests.Session()
    
    response = Request()
    try:
        match TypeReq.split():
            case['GET']:
                response = session.get(
                    URL,   
                    params=params,        
                    headers=HEADERS,
                    cookies=COOKIES,
                    json=json,
                    allow_redirects=False
                )
                redirect_url = f'https://www.mvideo.ru{response.headers["Location"]}'
                    
                response = session.get(
                redirect_url,                        
                headers=HEADERS,
                cookies=COOKIES,
                json=json,
                allow_redirects=True
                )
                
            case['POST']:
                response = session.post(
                URL,            
                cookies=COOKIES,
                headers=HEADERS,
                json=json,
                allow_redirects=False
                )
    except Exception:
        with open("Log.txt", "w") as file:
            file.write("[ERROR] The request could not be sent. Check your internet connection.")
        sys.exit()
    finally:
        session.close()    
    
    return response.json()


def SaveImage(URL: str, Path: str, names: list) -> list:    
    images = []
    for name in names:              
        if (name.find('s') != -1) or (name.removeprefix('Pdb/').removesuffix(".jpg").isdigit() == True):
            continue
        if (os.path.exists(f"{PATH}\\{Path}\\{name.removeprefix('Pdb/')}")) == False:
            with open(f"{PATH}{Path}/{name.removeprefix('Pdb/')}", "wb") as file:
                file.write(requests.get(f"{URL}{name}").content)  
        if  (f"{PATH}\\{Path}\\{name.removeprefix('Pdb/')}" in images) == False:
            images.append(f"{name}")
            
            
    return images


def Logger(info: str, error: str, path: str, res: bool):
    with open(f"{path}Log.txt", "a") as file:
            if res:
                file.write(f"{info}\n")
            else:
                file.write(f"{error}\n")


def GetPath(names: list, path: str) -> str:
    res = []
    for name in names:
        res.append(f"{path}{name.replace('Pdb/', '')}")
    return res


def GetPage() -> int:
    response = GetRespJson("GET", "https://www.mvideo.ru/bff/products/listing", params={
                                                                                    'categoryId': '118',
                                                                                    'offset': '0',
                                                                                    'limit': '24',
                                                                                    'filterParams': [
                                                                                        'WyJza2lka2EiLCIiLCJkYSJd',
                                                                                        'WyJ0b2xrby12LW5hbGljaGlpIiwiIiwiZGEiXQ==',
                                                                                    ],
                                                                                    'doTranslit': 'true'
                                                                                })
    return math.ceil(response.get("body").get("total") / 24)


def SearchSaveData():   
    items = []
    images = []
    for i in range(0, GetPage()):
        response = GetRespJson("GET", "https://www.mvideo.ru/bff/products/listing", params={
                                                                                'categoryId': '118',
                                                                                'offset': i * 24,
                                                                                'limit': '24',
                                                                                'filterParams': [
                                                                                    'WyJza2lka2EiLCIiLCJkYSJd',
                                                                                    'WyJ0b2xrby12LW5hbGljaGlpIiwiIiwiZGEiXQ==',
                                                                                ],
                                                                                'doTranslit': 'true'
                                                                            })
        products_id = response.get("body").get("products")
        
        json_data = {
        'productIds': products_id,
        'mediaTypes': [
            'images',
        ],
        'category': True,
        'status': True,
        'brand': True,
        'propertyTypes': [
            'KEY',
        ],
        'propertiesConfig': {
            'propertiesPortionSize': 5,
        },
        'multioffer': False,
        }

        response = GetRespJson("POST", "https://www.mvideo.ru/bff/product-details/list", json_data)    
        links = {}
        for item in response.get("body").get("products"):
            nameImage = SaveImage("https://img.mvideo.ru/", "image", item.get("images"))         
            links[item.get("productId")] =  {
                "name": item.get("name"),
                "linkToproduct": f"https://www.mvideo.ru/products/{item.get('nameTranslit')}-{item.get('productId')}",
                "pathToImage": GetPath(nameImage, f"{PATH}image/".replace('/', '\\'))
            }      
        
        params = {
        'productIds': ','.join(products_id),
        'addBonusRubles': 'true',
        'isPromoApplied': 'true',
        }

        response = GetRespJson("GET", "https://www.mvideo.ru/bff/products/prices", params=params)
        
        
        materialPrices = response.get("body").get("materialPrices")
        
        for item in materialPrices:        
            items.append(Item(productId=int(item.get("price").get("productId")),
                        name=links[item.get("price").get("productId")]['name'],
                        basePrice=int(item.get("price").get("basePrice")),
                        salePrice=int(item.get("price").get("salePrice")),
                        bonusRubles=int(item.get("bonusRubles").get("total")),
                        linkToproduct=links[item.get("price").get("productId")]['linkToproduct']
                        ))
            for link in links[item.get("price").get("productId")]['pathToImage']:
                images.append(Image(productId=int(item.get("price").get("productId")),
                                    pathImage=link))
            
    
    DB_Saver = Manager(PATH_TO_BD, Item)
    
    Logger(info="[INFO] DB connection",
            error="[ERROR] DB no connection",
            res=DB_Saver.Connection(),
            path=PATH)
    
    Logger(info="[INFO] All items save",
            error="[ERROR] Something items save",
            res=DB_Saver.AddItems(items),
            path=PATH)
    
    DB_Saver = Manager(PATH_TO_BD, Image)
    Logger(info="[INFO] DB connection",
            error="[ERROR] DB no connection",
            res=DB_Saver.Connection(),
            path=PATH)
    
    Logger(info="[INFO] All items save",
            error="[ERROR] Something items save",
            res=DB_Saver.AddItems(images),
            path=PATH)






if __name__ == '__main__':
    if os.path.isdir(f'{PATH}image') == False:     
        os.mkdir(f'{PATH}image')
    Logger(info=f"{datetime.now().date()}     |      {datetime.now().hour}:{datetime.now().minute}:{datetime.now().second}", 
            error=None, 
            res=lambda: True, 
            path=PATH)
        
    SearchSaveData()
    with open(f"{PATH}Log.txt", "a") as file:
        file.write("[INFO] The parsing was completed successfully.\n")