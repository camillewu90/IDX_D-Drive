# get all the captain coaster api data for rollercoasters
import json 
import requests
import re
import numpy as np 
import pandas as pd
from collections import OrderedDict

# scrape coaster data from captain coaster
# my captain coaster api key
my_key= '12be1092-8f11-4b5d-99be-9e2192dd8c07'
# create a list of all coaster id,captain coaster id is from 1 to 3294
coaster_ids=list(range(1,3295))
# create the list of urls for api requests
urls=[]
for coaster_id in coaster_ids:
    coaster_id=str(coaster_id)
    urls.append('https://captaincoaster.com/api/coasters?id='+coaster_id)

# get info chunck from the api
def get_infochunk(url):
    res=requests.get(url,headers={'X-Auth-Token': my_key})
    #load json data
    json_data=res.json()
    # grab the info list from json file
    for key,value in json_data.items():
        if key=="hydra:member":
            infochunk=value
    return infochunk
        
# unpack the info list to just one dict element
def get_info_dict(infochunk):
    for element in infochunk:
        info_dict=element
    return info_dict

# select only info I want from the info_dict
def get_clean_dict(info_dict):
    clean_dict={k:info_dict[k] for k in ('height','id','inversionsNumber','length','mainImage','manufacturer',
                                         'materialType','name','park','rank','score','seatingType','speed','status',
                                         'totalRatings','validDuels')}
    return clean_dict

#create the final data dict
def create_dict(clean_dict):
    final_dict=dict()
    for key,value in clean_dict.items():
        if key=='mainImage':
            final_dict[key]=value['path']
        elif key in ['manufacturer','materialType','seatingType','status']:
            final_dict[key]=value['name']
        elif key=='park':
            final_dict['park_id']=int(value['@id'].replace("/api/parks/",''))
            final_dict['park_name']=value['name']
        else:
            final_dict[key]=value
    return final_dict   

dict_list=[]
for url in urls:
    infochunk=get_infochunk(url)
    info_dict=get_info_dict(infochunk)
    clean_dict=get_clean_dict(info_dict)
    final_dict=create_dict(clean_dict)
    dict_list.append(final_dict)
df_coasters=pd.DataFrame(dict_list)
df_coasters.to_csv('captain_coaster_data.csv',index=False)
