#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import boto
import boto.s3
from boto.s3.key import Key
import sys
import yaml

c = yaml.safe_load(open('config.yml'))

def find_s3_bucket(s3_conn, string):
    for i in s3_conn.get_all_buckets():
        if string in i.name:
            return i

def connect_to_bucket(bucket_name=c['s3_bucket']):
	conn = boto.connect_s3(c['aws_access_key_id'], c['aws_secret_access_key'])
	return find_s3_bucket(conn, bucket_name)

def upload_string(string, filepath, bucket):
	k = Key(bucket)
	k.key = filepath
	print "/\ %s" % (filepath)
	k.set_contents_from_string(string)

def download_string(filepath, do_print=True):
	k = Key(bucket)
	k.key = filepath
	print "\/ %s" % (filepath)
	return k.get_contents_as_string()


