#library_of_congress_scraper.py
from __future__ import print_function
from gcputils.gcpclient import GCSClient
from bs4 import BeautifulSoup
import requests
# import lxml.etree as etree
# import xml.etree.ElementTree as ET
import json
# import pandas as pd
import os
import time
# import random
# import math
from pprint import pprint
#import load_vars as lv
import html
# import yaml
# from yaml import Loader, Dumper
# import glob
# import datetimeResult
import os.path
# from googleapiclient.discovery import build
# from google_auth_oauthlib.flow import InstalledAppFlow
# from google.auth.transport.requests import Request
# from google.oauth2.credentials import Credentials
# from google.oauth2 import service_account
# from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload
from flatten_json import flatten
# import networkx as nx
# import matplotlib
# from networkx.readwrite import json_graph
# import matplotlib.pyplot as plt
# import tracemalloc
# import os
#from ratelimiter import RateLimiter

# Imports the Cloud Logging client library
import google.cloud.logging
import logging


class cd:
    """Context manager for changing the current working directory"""
    def __init__(self, newPath):
        self.newPath = os.path.expanduser(newPath)

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)

class search_results_page():

    def __init__(self,base_url = "https://www.loc.gov/collections",collection = "united-states-reports",json_parameter = "fo=json",results_per_page = "c=79",query_param = "?",page_param ="sp=",page_num = 1):
        #pprint(num_columns)
        print("initializing Search Result Generator")
        self.search_url = self.create_search_url(base_url,collection,json_parameter,results_per_page,query_param,page_param,page_num)
        self.response = self.request_data()
        self.response_json = self.response_to_json()
        #self.soup_html = self.html_parse()
        self.next_url = self.get_next_url()
        self.page_num = page_num

    def to_json(self, file_name = 'result_',file_num = 0, extension =".json"):
        output_name = file_name + str(file_num)
        output_name = output_name + extension
        print(json.dumps(self.response_json))
        with open(output_name, 'w') as outfile:
            json.dump(self.response_json, outfile)

    def to_pandas(self):
        df = nx.to_pandas_edgelist(self.graph)
        return(df)

    def to_csv(self,file_name = 'result_',file_num = 0, extension =".csv"):
        output_name = file_name + str(file_num)
        output_name = output_name + extension
        df = self.to_pandas()
        df.to_csv(output_name)


    def write_graphml(self,file_name = 'result_', file_num=0, extension = ".graphml"):
        output_name = file_name + str(file_num)
        output_name = output_name + extension
        nx.write_graphml(self.graph, output_name)

    def write_to_file(self,data = None, file_name = 'result_',file_num = 0, extension = ".json"):
        output_name = file_name + str(file_num)
        output_name = output_name + extension
        with open(output_name, 'w') as outfile:
            json.dump(data, outfile)


    def node_gen_2(self, data, root ='result', node_list = [], edge_list = [], previous_k = None, previous_edge = None, graph = None):
        #root = root 
        if type(data) is dict:
            for k, v in data.items():
                if k is not None and k not in node_list:
                    graph.add_node(k, type = k)
                    #node_list.append((k, {'type' : k}))
                    #(1, 2, color='red', weight=0.84, size=300)\
                    graph.add_edge(root,k, relationship = "of", type = "root")
                    #edge_list.append((root , k, {"relationship" : "of"}, {"type" : 'root'}))
                #pprint('passing_value')
                #save k
                previous_k = k
                previous_edge = (root , k)
                self.node_gen_2(v,root = root, node_list = node_list,edge_list = edge_list, previous_k = k, previous_edge = previous_edge, graph = graph)

        elif type(data) is list:
            for item in data:
                #pprint('passing_data')

                self.node_gen_2(item,root = root, node_list = node_list,edge_list = edge_list,previous_k = previous_k, previous_edge= previous_edge, graph = graph)
                #create_edge to k

        else:
            #this item is no longer a dictionary or list
            pprint('appending_data')
            #create edge to k
            if data is not None:
                graph.add_node(data,type = data)
                #node_list.append((data, {"type" : data}))
                graph.add_edge(previous_k, data, relationship = "is", type = previous_k)
                #edge_list.append((previous_k ,data,{'relationship': "is"}, {'type' : data}))
                #edge_list.append((root,data))

    #flatten(hierarchak)_dict)
        return graph 

    
    def node_runner(self,data,graph):
        
        node_list = []
        edge_list = []
        for item in data:
            #root = item['title']
            graph = self.node_gen_2(data = item, node_list = node_list, graph = graph)
        #pprint(edge_list)
        return graph

    def node_generator(self, data, root ='title_testing', node_list = [], edge_list = [], previous_k = None, previous_edge = None):
        #pprint(data)
        if type(data) is dict:
            for k, v in data.items():
                if k is not None and k not in node_list:
                    node_list.append(k)
                    edge_list.append((root , k))
                #pprint('passing_value')
                #save k
                previous_k = k
                previous_edge = (root , k)
                self.node_generator(v,root = root, node_list = node_list,edge_list = edge_list, previous_k = k, previous_edge = previous_edge)

        elif type(data) is list:
            for item in data:
                #pprint('passing_data')

                self.node_generator(item,root = root, node_list = node_list,edge_list = edge_list,previous_k = previous_k, previous_edge= previous_edge)
                #create_edge to k

        else:
            #this item is no longer a dictionary or list
            pprint('appending_data')
            #create edge to k
            if data is not None:
                node_list.append(data)
                edge_list.append((previous_k ,data))
                edge_list.append((root,data))

    #flatten(hierarchak)_dict)
        return node_list, edge_list 
        #self.json_graph = self.create_json_graph()


    def create_json_graph(self):
        #graph = nx.Graph(self.response_json)
        graph = nx.from_dict_of_dicts(self.response_json)
        #graph = json_graph.node_link_graph(self.response_json)
        nx.draw(graph)
        return graph
        
        #self.node_list = self.node_generator`



    def create_search_result_node(self):
     
        for item in self.response_json_flat:
            for k,v in item.items():
                if k not in self.column_lookup_table:
                    column_string = self.colnum_string()

                    self.column_lookup_table[k] = self.colnum_string(self.num_columns)
                    self.num_columns += 1
                else:
                    continue

    def append_to_data_list(self,rnge,d):#rename to _data_list
        request_body = {
            'range': rnge,
            "majorDimension": "COLUMNS",
            "values": [d]
        }
        return request_body
        #data_list.append(request_body_tmp)

    def map_column_to_range(self,column_key):
        
        rnge = "'Sheet1'" + "!" + column_key + str(1)
        return rnge
                

    def colnum_string(self,num_columns):
        string = ""
        #pprint("conlum_string")
        #pprint(num_columns)
        while num_columns > 0:
            num_columns, remainder = divmod(num_columns - 1, 26)
            string = chr(65 + remainder) + string
            #pprint(string)
        return string

    def map_columns_to_lookup_table(self):

        #print('first_map_columns_print')
        #num_columns_tmp = self.num_columns
        #pprint(num_columns_tmp)
        for item in self.response_json_flat:
            for k in item.keys():
                num_columns_tmp = self.num_columns
                if k not in self.column_lookup_table:
                    #print('second_map_Columns_print')
                    #pprint(num_columns_tmp)
                    self.column_lookup_table[k] = self.colnum_string(num_columns = num_columns_tmp)
                    self.num_columns = self.num_columns + 1
       
                    #append range to request... 
                    #append collumn to batch lookup
                

                else:
                    continue
    
    def column_request_list_generator(self):
        request_list = []
        for k,v in self.column_lookup_table.items():
            rnge = self.map_column_to_range(k)
            request_body = self.append_to_data_list(rnge,v)
            #pprint(request_body)
            request_list.append(request_body)
        return request_list





        #return column_lookup_table

    def get_next_url(self):
        return (self.response_json['pagination']['next'])

    def create_search_url(self,base_url,collection,json_parameter,results_per_page,query_param,page_param,page_num):
        url_sep ="/"
        page_param = page_param +(str(page_num))
        query = "&".join([json_parameter,results_per_page,page_param])
        query = query_param + query
        search_url = url_sep.join([base_url,collection,query])
        #pprint(search_url)
        
        return search_url

    def say_hello(self):
        pprint(self.base_url)

    def request_data(self):
        headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.11 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9',
                    'Accept-Encoding': 'identity'
                }
        return requests.get(self.search_url,headers=headers)

    def response_to_json(self):
        return self.response.json()

    def html_parse(self):
        soup=BeautifulSoup(self.response.content,'lxml')
        #pprint(soup)
        return soup

    def flatten_result(self):
        flat_result_list = []
        for item in self.response_json['results']:
            flat_json = flatten(item)
            flat_result_list.append(flat_json)
        return flat_result_list



class search_result():
    
    def __init__(self,dict_item,num_columns,colnum_string):
        self.key = dict_item.key()
        self.value = dict_item.value()
        self.column_string = colnum_string
        self.index = num_columns
        self.range = self.create_column_range_string()
        self.request_body = self.create_column_request()

    def create_column_request(self):
        request_body = {
            'range': self.range,
            "majorDimension": "COLUMNS",
            "values": [self.value]
        }
        return request_body

    
    def create_column_range_string(self):

        rnge = "'Sheet1'" + "!" + self.column_string + str(1)
        return rnge
    def colnum_string(self, num_columns):
        string = ""
        while num_columns > 0:
            num_columns, remainder = divmod(num_columns - 1, 26)
            string = chr(65 + remainder) + string
        return string

class google_drive:
    def __init__(self,creds):
        self.service = self.get_drive_service(creds)

    def test(self):
        pprint("hello I exist")

    def get_drive_service(self, creds):
        """Shows basic usage of the Drive v3 API.
        Prints the names and ids of the first 10 files the user has access to.
        """
        SCOPES = []
        #creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.

        service = build('drive', 'v3', credentials=creds)

        # Call the Drive v3 API
        results = service.files().list(
            pageSize=10, fields="nextPageToken, files(id, name)").execute()
        items = results.get('files', [])

        if not items:
            print('No files found.')
        else:
            print('Files:')
            for item in items:
                print(u'{0} ({1})'.format(item['name'], item['id']))

        return service
    
    

    def create_folder(self,title):
        drive_service = self.service
        file_metadata = {
            'name': '{}'.format(title),
            'mimeType': 'application/vnd.google-apps.folder'
        }
        file = drive_service.files().create(body=file_metadata,
                                            fields='id').execute()
        print('Folder ID: %s' % file.get('id'))



    def add_spreadsheet_to_folder(self ,folder_id,title):
        drive_service = self.service
    
        file_metadata = {
        'name': '{}'.format(title),
        'parents': [folder_id],
        'mimeType': 'application/vnd.google-apps.spreadsheet',
        }

        res = drive_service.files().create(body=file_metadata).execute()
        #print(res)

        return res

class google_sheet():

    def __init__(self,creds):
        self.service =self.get_sheet_service(creds)


    def get_sheet_service(self,creds):
        service = build('sheets', 'v4', credentials=creds)
        return service.spreadsheets()

class google_creds():

    def __init__(self,creds_path):

        self.creds = self.get_creds(creds_path)
   
    def get_creds(self,creds_path):

        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
                print("no creds")
            else:
                creds = service_account.Credentials.from_service_account_file(creds_path)
                #creds = ServiceAccountCredentials.from_json_keyfile_name('add_json_file_here.json', SCOPES)
                #flow = InstalledAppFlow.from_client_secrets_file(
                #    'credentials.json', SCOPES)
                #creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            #with open('token.json', 'w') as token:
            #    token.write(creds.to_json())
        return creds

class config():

    def __init__(self,file_path):
        #self.yaml_stream = file("config.yaml", 'r')
        self.data = self.load_config(file_path)


    def load_config(self,file_path):
        #print("test")
        stream = open(file_path, 'r')
        data = yaml.load(stream,Loader = Loader)
        #pprint(data)
        return data

def create_google_credentials_object(creds_path = 'credentials.json'):
    google_credentials_object = google_creds(creds_path)
    return google_credentials_object
    
def create_config_object(file_path = 'config.yaml'):
    config_object = config(file_path)
    return config_object


def search_result_generator(condition = True, page_num=1):
    #column_lookup_table = {}
    #pprint(num_columns)
    # page_num = 1
    column_lookup_table = {}
    while condition ==True:
        #pprint(num_columns)
        time.sleep(61)
        search_results_page_object = create_search_results_page_object(page_num = page_num)
        if search_results_page_object.next_url != None:
            condition = True
            page_num = page_num + 1            
            yield (search_results_page_object)
        else:
            condition = False
            yield (search_results_page_object)
        
def create_search_results_page_object(base_url = "https://www.loc.gov/collections",collection = "united-states-reports",json_parameter = "fo=json",results_per_page = "c=70",query_param = "?",page_param ="sp=",page_num = 1):
    #search = search_results(base_url,collection,json_parameter,results_per_page,query_param,page_param,page_num)
    #pprint(search.search_url)
    #pprint(num_columns)
    return search_results_page(base_url,collection,json_parameter,results_per_page,query_param,page_param,page_num)

def create_google_drive_object(google_creds):
    drive_service_object = google_drive(google_creds)
    return drive_service_object

def create_google_sheet_object(google_creds):
    sheet_service_object = google_sheet(google_creds)
    return sheet_service_object

def create_new_google_sheet(google_drive_object,folder_id,title):
    sheet_meta_data = google_drive_object.add_spreadsheet_to_folder(folder_id, title)
    return sheet_meta_data

def flatten_result(result_json):
    flat_json = flatten(result_json)
    return flat_json

def write_last_page_num(page_num):
    with open('last_page_num.txt', 'w') as f:
        f.write(str(page_num))

def read_last_page_num(f = 'last_page_num.txt'):
        count = 0
        base_case = 1
        print("\nUsing readline()")
        
        with open(f, 'r') as fp:
            while True:
                count += 1
                line = fp.readline()
        
                if not line:
                    break
                
                if int(line) > base_case:
                    base_case = int(line)
                print("Line{}: {}".format(count, line.strip()))
        
        return base_case
        

def main():
    #hardcoding this.. idk if it is better to add it to the config or not. 
    # i have thoughts on both. 
    # just hardcoding to limit th enumber of htings to be aware of when working with this script
    project_id = 'smart-axis-421517'
    last_page_num = read_last_page_num() + 1
    # print(f"Starting at {last_page_num}")

    gcs = GCSClient(project_id, credentials_path=None)
    
    # Instantiates a cloud loggingclient
    client = google.cloud.logging.Client()

    # Retrieves a Cloud Logging handler based on the environment
    # you're running in and integrates the handler with the
    # Python logging module. By default this captures all logs
    # at INFO level and higher
    client.setup_logging()

    # List buckets to test client authorization
    buckets = gcs.list_buckets()
    print("Buckets:", buckets)
    logging.info(f"Buckets: {buckets}")

    # creating a new bucket if it doesn't exist
    bucket_name = "loc-scraper"

    bucket = gcs.create_bucket(bucket_name=bucket_name)
    logging.info(bucket)
    print(bucket)

    # this will create a last_page blob if it does not already exist. The intent of this is pull locally and drop whatever the last local run says into the blob 
    # Overwrite is not true therefore we will not overwrite if there is a blob already instantiated. This is a bit of a base case.
    # it does depend on a last_page.txt document locally but that really doesn't matter too much and can be updated in the next build to not be scripted into the code

    last_page_blob_name = 'last_page.txt'
    last_page_blob_data = str(last_page_num)

    #this will attempt to create. if it already exists it will return the blob that was previously generated

    last_blob = gcs.put_blob_from_string(bucket_name, last_page_blob_data, last_page_blob_name, overwrite = False)
    if last_blob:
        print("Blob contents:")
        last_blob_data = int(last_blob.download_as_string().decode("utf-8")) + 1
        print(last_blob_data)
        print(type(last_blob_data))

    print('Starting Run')
    logging.info("Starting Run")
    # tracemalloc.start()
    #rate_limiter = RateLimiter(max_calls=1, period=60)
    #cd to output
    #result = create_search_results_page_object()
    #with cd("output"):d
    #    result.write_to_file(data = result.dict_of_dicts, file_num = 1)

    for obj in search_result_generator(page_num = last_blob_data):   
        page_num = str(obj.page_num)
        # print("testing")
        logging.info(f"Starting page:{page_num}")
        destination_blob_name = "-".join(["result",page_num,]) + ".json"
        # with cd("output_2"):
            #print('hahaha')
        file_string = json.dumps(obj.response_json)
        blob = gcs.put_blob_from_string(bucket_name, file_string, destination_blob_name)
        # print(blob)
        # obj.to_json(file_num = page_num)
            #obj.write_graphml(file_num= page_num)
            #obj.to_pandas()
            #obj.write_to_file(data = obj.dict_of_dicts, file_num = page_num)
            #obj.to_csv()
        #the following commenti sa vestigal of a previous run. This can likely be dropped in next official push
        # actually i am keeping it to keep the base case on local runs up to date
        write_last_page_num(page_num)
        last_blob = gcs.put_blob_from_string(bucket_name, str(page_num), last_page_blob_name, overwrite = True)
        if last_blob:
            # print("Blob contents:")
            last_blob_data = int(last_blob.download_as_string().decode("utf-8"))
            # print(last_blob_data)
            logging.info(f"blob:contents:{last_blob_data}")
            # print(type(int(last_blob_data)))
            # print("{} Search Results Crawled".format(page_num))
            logging.info("{} Search Results Crawled".format(page_num))


    
    # snapshot = tracemalloc.take_snapshot()
    # top_stats = snapshot.statistics('lineno')
    # print("[ Top 10 ]")
    # for stat in top_stats[:10]:
        # print(stat)


if __name__ == "__main__":
    main()

        
        

    
