#!/usr/bin/python
# -*- coding: utf-8 -*-
import os, re, pytz
import requests
from datetime import datetime
import facepy
import s3
import fb
from clean_urls import *
import json

c = yaml.safe_load(open('config.yml'))

# date formats
IN_TIME_FORMAT = "%Y-%m-%dT%H:%M:%S+0000"
OUT_TIME_FORMAT = "%Y-%m-%d %H:%M:%S"


def clean_datetime(date_string):
    utc = pytz.timezone("UTC")
    tz = pytz.timezone(c['time_zone'])

    dt = datetime.strptime(date_string, IN_TIME_FORMAT)
    try:
        dt = dt.replace(tzinfo=utc)
    except:
        return None
    else:
      return tz.normalize(dt.astimezone(tz))

def get_fb_link(post_data, unshorten):
  if post_data.has_key('link'):
    if unshorten :
      return clean_url(unshorten_link(post_data['link']))
    else:
      return clean_url(post_data['link'])
  elif post_data.has_key('source'):
    if unshorten :
      return clean_url(unshorten_link(post_data['source']))
    else:
      return clean_url(post_data['source'])
  else:
    return None

def get_insights(api, post_id):

  graph_results = api.get(post_id + "/insights", page=False, retry=5)
  data = graph_results['data']
  insights = {}
  for d in data:
    val = d['values'][0]['value']
    if isinstance(val, dict):
      for k, v in val.iteritems():
        insights[k] = v
    else:
      insights[d['name']] = val

  return insights

def get_new_data_for_page(page_id):
  
  data = []
  api = fb.connect()
  print "> getting new data for %s" % page_id
  
  # fetch account data so we can associate the number of likes with the account AT THAT TIME
  try:
    acct_data = api.get(page_id)
  except Exception as e:
    print "!!! "
    print e
    return []
  else:
    # keep track of new post ids
    new_post_ids = []

    # get last 100 articles for this page
    page = api.get(page_id + "/posts", page=False, retry=5, limit=int(c['limit']))

    # loop through and extract data
    for post in page['data']:
      try:
        post_id = post['id'] if post.has_key('id') else None
      except Exception as e:
        print "!!! "
        print e
        continue
      else:
        if post.has_key('created_time'):
          date_time = clean_datetime(post['created_time'])
        else:
          date_time = None

        print "< %s" % post_id
        print date_time
        # extract message and potential so we can find links within the msg if not in url
        # fields
        message = post['message'].encode('utf-8') if post.has_key('message') else None
        url = get_fb_link(post, unshorten=True)
        short_url = get_fb_link(post, unshorten=False)
        if url is None or is_facebook(url):
          if message is not None:
            url = clean_url(unshorten_link(extract_url(message)))

        # safely return post data
        post = {
          'page_id': page_id,
          'post_id': post['id'] if post.has_key('id') else None,
          'page_likes': acct_data['likes'] if acct_data.has_key('likes') else None,
          'page_talking_about': acct_data['talking_about_count'] if acct_data.has_key('talking_about_count') else None,
          'url': url,
          'short_url': short_url,
          'type': post['type'] if post.has_key('type') else None,
          'status_type': post['status_type'] if post.has_key('status_type') else None,
          'message': message,
          'datetime': date_time.strftime(OUT_TIME_FORMAT) if date_time is not None else None,
          'timestamp': date_time.strftime("%s") if date_time is not None else None,
          'year': date_time.year if date_time is not None else None,
          'month': date_time.month if date_time is not None else None,
          'wkdy': date_time.weekday() if date_time is not None else None,
          'wknd': 1 if date_time.weekday() > 4 and date_time is not None else 0,
          'day': date_time.day if date_time is not None else None,
          'hour': date_time.hour if date_time is not None else None,
          'minute': date_time.minute if date_time is not None else None
        }

        insights = get_insights(api, post_id)

        # combine data
        data.append(dict(post.items() + insights.items()))

    return data

if __name__ == '__main__':
  today = datetime.now().strftime("%Y/%m/%d")
  timestamp = datetime.now().strftime("%s")
  bucket = s3.connect_to_bucket(c['s3_bucket'])
  for page_id in c['fb_page_ids']:
    data = get_new_data_for_page(page_id)
    string = "\n".join([json.dumps(d) for d in data])
    filepath = "hindsights/%s/%s/%s.json" % (page_id, today, timestamp)
    s3.upload_string(string, filepath, bucket)

