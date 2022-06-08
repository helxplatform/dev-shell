#!/usr/bin/env python

import os
import argparse
import json
import yaml
import boto3
import boto3.session
from boto3.s3.transfer import TransferConfig



def get_session(values):
   session = boto3.session.Session(aws_access_key_id=values['access_key'],aws_secret_access_key=values['secret_key'])
   resource = session.resource(service_name='s3',endpoint_url=values['host'])
   bucket = resource.Bucket(values['bucket'])
   return resource,bucket


def main(args):
   s3_access_key = None
   s3_bucket = None
   s3_host_url = None
   s3_private_key = None
   values = None
   values_file = None
   values_file_arg = None

   if os.environ.get('S3_ACCESS_KEY') != None: s3_access_key = os.environ.get('S3_ACCESS_KEY')
   if os.environ.get('S3_BUCKET') != None: s3_bucket = os.environ.get('S3_BUCKET')
   if os.environ.get('S3_HOST_URL') != None: s3_host_url = os.environ.get('S3_HOST_URL')
   if os.environ.get('S3_PRIVATE_KEY') != None: s3_private_key = os.environ.get('S3_PRIVATE_KEY')
   if os.environ.get('VALUES_FILE') != None: values_file = os.environ.get('VALUES_FILE')
   if args.access_key != None: s3_access_key = args.access_key
   if args.bucket != None: s3_bucket = args.bucket
   if args.host != None: s3_host_url = args.host
   if args.private_key != None: s3_private_key = args.private_key
   if args.values != None: values_file = args.values

   if values_file == None: values_file_arg = "values.yaml"
   else: values_file_arg = values_file

   try:
      with open(values_file_arg,'r') as stream: values = yaml.safe_load(stream)
      if s3_access_key != None: values['access_key'] = s3_access_key
      if s3_bucket != None: values['bucket'] = s3_bucket
      if s3_host_url != None: values['host'] = s3_host_url
      if s3_private_key != None: values['private_key'] = s3_private_key
   except Exception as e:
      if values_file != None: print("Could not open values file ({0})".format(e))
      elif s3_access_key == None or s3_bucket == None or s3_host_url == None or s3_private_key == None:
         print("Could not open values file ({0}) and s3 access not defined otherwise".format(e))
         print("s3_access_key = {s3_access_key}".format(s3_access_key=s3_access_key))
         print("s3_bucket = {s3_bucket}".format(s3_bucket=s3_bucket))
         print("s3_host_url = {s3_host_url}".format(s3_host_url=s3_host_url))
         print("s3_private_key = {s3_private_key}".format(s3_private_key=s3_private_key))
      else:
         values = { 'access_key':s3_access_key, 'bucket':s3_bucket, 'host':s3_host_url, 'secret_key':s3_private_key }
   if values != None:
      try:
         resource,bucket = get_session(values)
         MB = 1024 ** 2
         config = TransferConfig(multipart_threshold=300*MB)
         if args.command == 'ls':
            for obj in bucket.objects.all(): print(obj.key)
         elif args.command == 'get':
            filename = args.object.split('/')[-1]
            obj = resource.Object(bucket.name,args.object)
            print("getting: {bucket_name}:{filename}".format(bucket_name=bucket.name,filename=filename))
            obj.download_file(filename,Config=config)
         elif args.command == 'put':
            filename = args.src.split('/')[-1]
            prefix = args.dst
            if prefix == None: prefix = ''
            obj = resource.Object(bucket.name,prefix+filename)
            with open(args.src,"rb") as input_file: obj.put(Body=input_file,ServerSideEncryption='AES256')
         elif args.command == 'del':
            obj = resource.Object(bucket.name,args.object)
            obj.delete()
      except Exception as e:
         print("Could not perform operation ({0})".format(e))

parser = argparse.ArgumentParser()
parser.add_argument('--access_key', help="s3 access_key")
parser.add_argument('--bucket', help="s3 bucket")
parser.add_argument('--host', help="s3 host url")
parser.add_argument('--private_key', help="s3 private_key")
parser.add_argument('--values', help="values file")
subparsers = parser.add_subparsers(title='command',dest="command",help='s3 action')
parser_ls = subparsers.add_parser('ls', help='list contents in bucket')
parser_get = subparsers.add_parser('get', help='get an object')
parser_get.add_argument('object',help='object name')
parser_put = subparsers.add_parser('put', help='put an object')
parser_put.add_argument('src',help='file to put')
parser_put.add_argument('dst',nargs='?',help='prefix as if a directory in the bucket')
parser_del = subparsers.add_parser('del', help='get an object')
parser_del.add_argument('object',help='object name')

args = parser.parse_args()
main(args)

