# -*- coding: utf-8 -*-
import sys
import os
import google.oauth2.credentials

import google_auth_oauthlib.flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow
commentTotal=0
# The CLIENT_SECRETS_FILE variable specifies the name of a file that contains
# the OAuth 2.0 information for this application, including its client_id and
# client_secret.
CLIENT_SECRETS_FILE = "client_secret.json"

# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user's account and requires requests to use an SSL connection.
SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'


def get_authenticated_service():
  flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
  credentials = flow.run_console()
  return build(API_SERVICE_NAME, API_VERSION, credentials = credentials)

def write_response(response): #this function was from an official api sample, but we repurposed it for writing to a file.
  
    commentsFile = open("commentsAndTime.txt","a") #this will only work correctly if the file is empty. For each video, the file will be opened
                                                   #and new comments will be appended. The file should have been cleared before gettint any comments
    
    for i in range(len(response['items'])):
        text=cleanUpComment(response['items'][i]['snippet']['topLevelComment']['snippet']['textOriginal'])
        time=response['items'][i]['snippet']['topLevelComment']['snippet']['publishedAt'][11:-5]
        commentsFile.write(text+'--'+time+'\n')
        #print(text)
        #print(time)
          
    commentsFile.close()
    

# Build a resource based on a list of properties given as key-value pairs.
# Leave properties with empty values out of the inserted resource.
def build_resource(properties):
  resource = {}
  for p in properties:
    # Given a key like "snippet.title", split into "snippet" and "title", where
    # "snippet" will be an object and "title" will be a property in that object.
    prop_array = p.split('.')
    ref = resource
    for pa in range(0, len(prop_array)):
      is_array = False
      key = prop_array[pa]

      # For properties that have array values, convert a name like
      # "snippet.tags[]" to snippet.tags, and set a flag to handle
      # the value as an array.
      if key[-2:] == '[]':
        key = key[0:len(key)-2:]
        is_array = True

      if pa == (len(prop_array) - 1):
        # Leave properties without values out of inserted resource.
        if properties[p]:
          if is_array:
            ref[key] = properties[p].split(',')
          else:
            ref[key] = properties[p]
      elif key not in ref:
        # For example, the property is "snippet.title", but the resource does
        # not yet have a "snippet" object. Create the snippet object here.
        # Setting "ref = ref[key]" means that in the next time through the
        # "for pa in range ..." loop, we will be setting a property in the
        # resource's "snippet" object.
        ref[key] = {}
        ref = ref[key]
      else:
        # For example, the property is "snippet.description", and the resource
        # already has a "snippet" object.
        ref = ref[key]
  return resource

# Remove keyword arguments that are not set
def remove_empty_kwargs(**kwargs):
  good_kwargs = {}
  if kwargs is not None:
    for key, value in kwargs.items():
      if value:
        good_kwargs[key] = value
  return good_kwargs

def comment_threads_list_by_video_id(client, **kwargs):
  # See full sample for function
  kwargs = remove_empty_kwargs(**kwargs)

  response = client.commentThreads().list(
    **kwargs
  ).execute()

  return write_response(response)

def cleanUpComment(commentText):
  newText=commentText.encode('ascii',errors='ignore')
  newText=newText.decode("ascii")
  newText=newText.replace('\n',' ',100)
    
  return newText

if __name__ == '__main__':
  # When running locally, disable OAuthlib's HTTPs verification. When
  # running in production *do not* leave this option enabled.
  os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
  client = get_authenticated_service()

  open('commentsAndTime.txt', 'w').close() #the purpose of this line it to clear the file of comments, if it already exists
   
  readFile = open("finalIds.txt","r")     #using every video-id which we have gathered.
  IdList = readFile.readlines()           #gather 100 comments(the max) from each
  for singleId in IdList:
      print(singleId)
      comment_threads_list_by_video_id(client,
      part='snippet',
      videoId=singleId.rstrip('\n'),
      maxResults=100,
      textFormat="plainText")

  readFile.close()
                                
                                   
  
