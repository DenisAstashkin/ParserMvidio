import requests
from requests import Request
import json
import os
from conf.config import *
from sys import argv
import sys
import math

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


def GetPath(names: list, path: str) -> str:
    res = []
    for name in names:
        res.append(f"{path}{name}")
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


def Get_Data():   
    items = {}    
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
                "pathToImage": GetPath(nameImage, f"{PATH}/image/".replace('/', '\\'))
            }      
        
        params = {
        'productIds': ','.join(products_id),
        'addBonusRubles': 'true',
        'isPromoApplied': 'true',
        }

        response = GetRespJson("GET", "https://www.mvideo.ru/bff/products/prices", params=params)
        
        
        materialPrices = response.get("body").get("materialPrices")
        for item in materialPrices:        
            items[item.get("price").get("productId")] = {
                "name": links[item.get("price").get("productId")]['name'],
                "basePrice": item.get("price").get("basePrice"),
                "salePrice": item.get("price").get("salePrice"),
                "bonusRubles": item.get("bonusRubles").get("total"),
                "linkToproduct": links[item.get("price").get("productId")]['linkToproduct'],
                "pathToImage": links[item.get("price").get("productId")]['pathToImage']
            }
        print(f"[INFO] Page {i + 1}/9")
    with open(f"{PATH}products_id4.json", "a+") as file:
        json.dump(items, file, indent=5, ensure_ascii=False)


def main():
    Get_Data()


if __name__ == '__main__':
    if os.path.isdir(f'{PATH}image') == False:     
        os.mkdir(f'{PATH}image')
    main()    
    with open(f"{PATH}Log.txt", "w") as file:
        file.write("[INFO] The parsing was completed successfully.")