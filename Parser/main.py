import requests
from requests import Request
import json
import os
from conf.config import *

PATH = os.path.dirname(os.path.abspath(__file__))
PATH = PATH.replace(PATH[0], PATH[0].upper())

def GetRespJson(TypeReq: str, URL: str, json = None, params=None):     
    
    session = requests.Session()
    
    response = Request()
    
    match TypeReq.split():
        case['GET']:
            response = session.get(
            URL,
            params=PARAMS,
            cookies=COOKIES,
            headers=HEADERS,
            json=json,
            allow_redirects=False
            )
        
            redirect_url = f'https://www.mvideo.ru{response.headers["Location"]}'
            if params != None:                
                response = session.get(
                redirect_url,   
                params=params,        
                headers=HEADERS,
                cookies=COOKIES,
                json=json,
                allow_redirects=True
                )
            else:
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
            
    session.close()
    
    return response.json()


def SaveImage(URL: str, Path: str, names: list) -> list:    
    images = []
    for name in names:              
        if (name.find('s') != -1) or (name.removeprefix('Pdb/').removesuffix(".jpg").isdigit() == True):
            continue
        if (os.path.exists(f"{PATH}\\{Path}\\{name.removeprefix('Pdb/')}")) == False:
            with open(f"{Path}/{name.removeprefix('Pdb/')}", "wb") as file:
                file.write(requests.get(f"{URL}{name}").content)  
        if  (f"{PATH}\\{Path}\\{name.removeprefix('Pdb/')}" in images) == False:
            images.append(f"{name}")
            
            
    return images



def GetPath(names: list, path: str) -> str:
    res = []
    for name in names:
        res.append(f"{path}{name}")
    return res