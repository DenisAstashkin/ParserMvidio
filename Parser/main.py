import requests
from requests import Request
import json
import os
from conf.config import *

PATH = os.path.dirname(os.path.abspath(__file__))
PATH = PATH.replace(PATH[0], PATH[0].upper())