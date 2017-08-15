#!/usr/bin/evn python
# -*- coding: UTF-8 -*-
from datetime import datetime
from datetime import timedelta
from elasticsearch import Elasticsearch
import pytz
import pandas as pd
import DateGenerator



def search_es(es):
	body = {
  		"query": {
    		"filtered": {
      			"query": {
       				 "query_string": {
         				 "query": "*",
         				 "operator": "and"
       				 }
     			 },
				"filter": {
        			"bool": {
          				"must": [
           		 			{
             		 			"query": {
               						"query_string": {
                 						 "query": "iphone",
                 						 "operator": "and"
                					}
              					}
            				},
           		 			{
           						 "query": {
                					"query_string": {
                 			 			"operator": "and",
                 						"query": "*"
                					}
             					}
        					 }
       					 ],
        				"must_not": []
       	 			}
      			}
   			}
 		 },
 		"size": 10,
 		 "aggs": {
    			"2": {
     				 "terms": {
       					 "field": "versionName",
       					 "size": 1000,
        				"order": {
         					 "_count": "desc"
       					}
     				 }
    			}
  		}
	}

	result = es.search(index='statistics-user*', body=body,size = 10)
	return result


def analyse(buckets):
    '''
    构建data frame
    '''
    data = []
    for item in buckets:
        data.append(item['doc_count'])
    return data


def get_count_of_last_week():
   # start_date, end_date = DateGenerator.generate_date()
    es = Elasticsearch(['http://app.publish.youni.im:9200/'])
    result = search_es(es)
    #buckets = result['aggregations'][DATE_AGG]['buckets']
    #result = analyse(buckets)
    return result

get_count_of_last_week()