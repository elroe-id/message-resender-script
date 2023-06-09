#!/bin/python3

import sys
import traceback
import argparse
import csv
import time
import requests


def resend_messages(rids):
    url = "https://api-internal.fayda.et/registrationprocessor/v1/sender-stage/resend"
    failed = open("failed.txt","a")
    for rid in rids:
        data = "{\"rid\":\""+rid+"\", \"regType\":\"NEW\", \"process\":\"NEW\", \"source\":\"REGISTRARTION_CLIENT\"}"
        print(data)
        r = requests.post(url, data=data)
        print(r)
        if r.status_code != 200:
            failed.write(rid+"\tSTATUS CODE: "+str(r.status_code)+"\n")


def read_rids(filename):
    '''
    Read rids from a file with a list of rids one on each line
    '''
    rids = open(filename, 'rt', encoding='utf-16').readlines()
    rids = [r.strip() for r in rids]  # Strip newline char
    rids = [r for r in rids if len(r) != 0]  # Filter empty lines
    rids = [r.replace("\"","") for r in rids] # Remove quotes
    return rids

# def fetch_rids_from_db(query):
#     db = DB(conf.db_user, conf.db_pwd, conf.db_host, conf.db_port, 'mosip_regprc') 
#     rids = db.get_rids(query)
#     rids = [r[0] for r in rids] 
#     return rids
   
def args_parse(): 
   parser = argparse.ArgumentParser()
   group = parser.add_mutually_exclusive_group(required=True)
   group.add_argument('--rid', type=str,  help='RID to be processed')
   group.add_argument('--file', type=str,  help='File containing newline seperated list of RIDs')
   group.add_argument('--db', action='store_true',  help='Query db and get RIDs')
   parser.add_argument('--server', type=str, help='Full url to point to the server.  Setting this overrides server specified in config.py')
   parser.add_argument('--disable_ssl_verify', help='Disable ssl cert verification while connecting to server', action='store_true')
   args = parser.parse_args()
   return args, parser

def main():
    args, parser =  args_parse() 
    #if args.server:
    #     conf.server = args.server   # Overide

    # if args.disable_ssl_verify:
    #     conf.ssl_verify = False

    # init_logger('full', 'a', './out.log', level=logging.INFO)  # Append mode
    # init_logger('last', 'w', './last.log', level=logging.INFO, stdout=False)  # Just record log of last run
   
    if args.rid:
       rids = [args.rid]
    elif args.file:
      rids = read_rids(args.file)
    # elif args.db:
    #   rids = fetch_rids_from_db(conf.query)
    else:    
       parser.print_usage()
       
    try:
       resend_messages(rids) 
    except:
        formatted_lines = traceback.format_exc()
        print(formatted_lines)
        sys.exit(1)

    sys.exit(0)

if __name__=="__main__":
    main()