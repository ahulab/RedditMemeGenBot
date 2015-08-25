import urllib2
import urllib
import json
import base64

from time import gmtime, strftime
from os import environ, curdir, listdir
from json import load


"""
Basic response model looks like:

{
    data : Is null, boolean, or integer value. If it's a post then
    this will contain an object with the all generated values, such as an ID.

    success : boolean

    status : HTTP status code integer
}
"""

def load_imgur_creds():
    """
    For portability between machines the program will pull these values from the
    corresponding environment variables. You will have to set those environment variables
    youself. Otherwise input them manually in this file in each except block below. 
    """
    try:
        imgur_client_id = environ['imgur_client_id']
    except KeyError as e:
        print 'error importing {}, using user defined value.'.format(e)
        imgur_client_id = ''

    try:
        imgur_client_secret = environ['imgur_client_secret']
    except KeyError as e:
        print 'error importing {}, using user defined value.'.format(e)
        imgur_client_secret = ''

    try:
        imgur_refresh_token = environ['imgur_refresh_token']
    except KeyError as e:
        print 'error importing {}, using user defined value.'.format(e)
        imgur_refresh_token = ''

    return imgur_client_id, imgur_client_secret, imgur_refresh_token


def get_access_code(imgur_client_id, client_secret):
    """
    Gets access code for new account authorization. I shouldn't have to use this again
    anytime soon, but just in case I need to authorize a new account...
    Read thru console output to get access code
    """

    values = {'client_id' : imgur_client_id,
              'client_secret' : imgur_client_secret,
              'grant_type' : 'authorization_code',
              'code' : '' } # pull from http redirect in browser

    data = urllib.urlencode(values)
    request = urllib2.Request('https://api.imgur.com/oauth2/token')
    content = urllib2.urlopen(request, data)

    #print vars(content)
    content = json.loads(content.read())

    print content


def refresh_access(imgur_client_id, imgur_client_secret, imgur_refresh_token):
    """
    POST
    Basic response model
    Gets a new access token using the refresh token and writes the new refresh token
    to the environment variable 'access_token'
    """

    url = 'https://api.imgur.com/oauth2/token'
    request = urllib2.Request(url)

    values = {
    'refresh_token' : imgur_refresh_token,
    'client_id': imgur_client_id,
    'client_secret' : imgur_client_secret,
    'grant_type' : 'refresh_token' # value documentation says to use
    } 

    data = urllib.urlencode(values)
    content = urllib2.urlopen(request, data)
    # turn to dict
    content_json = content.read()

    try:
        content_json = json.loads(content_json)
    except ValueError as e:
        print e
        print content_json.read()

    environ['imgur_access_token'] = content_json['access_token']


def album_creation(title, description, access_token, privacy='public', layout='verticle'):
    """
    POST. Needs auth header. Basic response model. 
    Creates a blank album and returns the album id for use when uploading images
    """

    time = strftime("%d %b %Y", gmtime())

    url = 'https://api.imgur.com/3/album'
    request = urllib2.Request(url, headers={'Authorization' : 'Bearer {}'.format(access_token)})

    title = "{} {}".format(title, time)
    values = {
    'title' : title.encode('utf-8'),
    'description' : description.encode('utf-8'),
    'privacy' : privacy,
    'layout' : layout,
    }

    data = urllib.urlencode(values)
    content = urllib2.urlopen(request, data)
    content_json = content.read()
    content_json = json.loads(content_json)

    if content_json['success']:
        print 'Album ID is {}'.format(content_json['data']['id'])
        return content_json['data']['id']
    else:
        print 'Album creation failed'
        print 'Success: {}. Status: {}'.format(content_json['success'], content_json['status'])


def upload_image(picBase64, album, name, title, description, access_token):
    """ 
    POST. Needs auth token. Basic Response. 
    Uploads all images in given directory to specific album ID
    """
    
    url = 'https://api.imgur.com/3/image'
    request = urllib2.Request(url, headers={'Authorization' : 'Bearer {}'.format(access_token)})

    values = {
    'image' : picBase64,
    'album' : album.encode('utf-8'),
    'type' : 'base64',
    'name' : name.encode('utf-8'),
    'title' : title.encode('utf-8'),
    'description' : description
    }

    data = urllib.urlencode(values)
    content = urllib2.urlopen(request, data)
    content_json = content.read()
    content_json = json.loads(content_json)







