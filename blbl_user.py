#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import json
import os
import requests
import datetime

HOME = os.path.expandvars('$HOME')+"/"  #user home directory
pic_dir = HOME+"pictures/Bing"  #default dir
isDelete = True
delete_time = 7

def load_config():  # the load config function
    global HOME
    global pic_dir
    config_dir = HOME+"./config/Bing"
    json_file = config_dir+"/"+"config.json"
    init_config = {'Bing':{'dir':pic_dir,'delete':'True','time'=7,'version':'1.0'}}
    if not os.path.exists(config_dir)
