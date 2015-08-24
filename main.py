
import praw
import base64
import re
import urllib2 as urllib

from os import listdir, mkdir, curdir, environ, chdir, getcwd
from shutil import move
from time import gmtime, strftime
from json import loads, dump, load


from PostCollection import Post
import ImgurAPI


global post_dict



def load_json(directory=None):
    """
    loads json data generated when the program ran against a given subreddit
    """
    
    if directory:
        chdir(directory)
        with open('memedPost_json_data.txt') as json_data:
            data = load(json_data)
            return data
    else:
        chdir(curdir)
        with open('memedPost_json_data.txt') as json_data:
            data = load(json_data)
            return data


def file_work(sub_name, outputFoldersPath):
    # moves all pictures from runtime to folder
    # get time for folder name
    time = strftime("%a, %d %b %Y at %H_%M", gmtime())
    folder_name = "{} {}".format(sub_name, time)
    # create folder with time as name
    mkdir("{}/{}".format(outputFoldersPath, folder_name))
    # folder path
    folder_path = "{}/{}".format(outputFoldersPath, folder_name)

    # list of all files in current directory
    names = listdir(curdir)
    for i in names:
        # all memed images will start with memedPost and have the postId 
        # appended by the Post class
        if i.startswith('memedPost'):
            # use shutil.move to move images to folder for safe keeping :)
            move(i, folder_path)

    return folder_path


def load_draw_save(dictionary, submission, filetype, commentIndex, 
    album=False, album_id=None):

    targetPost = Post(submission, filetype, commentIndex=commentIndex)
    
    if album:
        # must load from environment variable or change this line manually
        # this app is registered with imgurs API
        imgur_client_id = environ['imgur_client_id']

        request = urllib.Request('https://api.imgur.com/3/album/%s' % album_id
            , headers={'Authorization': 'Client-ID %s' % imgur_client_id})
        content = urllib.urlopen(request).read()
        content = loads(content)

        # need error handling
        url = content['data']['images'][0]['link']
        targetPost.load_image(url)

    else:
        url = submission.url + filetype
        targetPost.load_image(url)

    if targetPost.image:
        # checking to see if the image loaded correctly, if it didn't then
        # we just skip and move on
        targetPost.add_text()

        #  dictionary stuff for record keeping
        if submission.id not in post_dict['items']:
            post_dict['items'][targetPost.dict['postId']] = targetPost.dict


# via redditlist.com/all
# top_subreddits = ['wtf', 'aww', 'space', 'creepy', 'spaceporn', 'pics',
# 'whatsthisplant', 'whatsthisbug', 'animalID', 'whatsthisbird',
# 'Whatisthisthing', 'mildlyinteresting', 'whatsthisrock', 'FossilID',
#   'nsfw', 'gonewild']
top_subreddits = ['pics', 'all']


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # #  main stuff # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


user_agent = "Meme generator bot v1.0 by /u/cDoubt"
r = praw.Reddit(user_agent=user_agent)
folder_paths = []

workingDirectory = getcwd()

# Creates folder in working directory named 'OutputFolders' to store all of the images
# If the folder already exists then we make it our output destination and move on
try:
    mkdir('{}/OutputFolders'.format(getcwd()))
    outputFoldersPath = '{}/OutputFolders'.format(getcwd())
except OSError as error:
    outputFoldersPath = '{}/OutputFolders'.format(getcwd())


for subreddit in top_subreddits:
    print '\nWorking on /r/{}'.format(subreddit)
    sub_name = subreddit
    pics_subreddit = r.get_subreddit(sub_name)
    hot_posts = pics_subreddit.get_hot(limit=25)

    post_dict = {
    'subreddit': subreddit,
    'time':  strftime("%a, %d %b %Y at %H_%M", gmtime()), 
    'items': {}
    }
    # other options include
    # get_top_from_all, get_top, get_top_from_month, get_top_from_week

    ## this block is for testing
    #submission = r.get_submission(submission_id='3i0bab')
    #for x in range(0,1):

    for submission in hot_posts:

        # make sure there is at least 1 comment in the submission
        if submission.comments > 0:
            # boolean to run the main
            doable = False
            # try 3 times to find a suitable comment
            for attempt in range(0, 3):
                try:
                    # for instance, if someone comments with a link to an
                    # imgur album, it could error out, so we try again
                    if len(submission.comments[attempt].body) > 0:
                        comment = attempt
                        doable = True
                        # break once we find a comment, this commend gets
                        # passed to the init function of the post class
                        break
                except:
                    pass

        # if it's not doable it's because the above if statement
        # could not find a suitable comment, or any comment at all
        if doable:
            # to handle imgur albums we just get the first image from the album
            if submission.domain == 'imgur.com' and '/a/' in submission.url:
                album_id = submission.url.split('/a/')[-1]

                print "\nURL is {}. It is an imgur album. Post id is {}".format(submission.url, submission.id)
                load_draw_save(post_dict, submission, 'jpg', attempt, album=True, album_id=album_id)

            # otherwise we find the filetype of the picture
            elif '.jpg' in submission.url or '.png' in submission.url or '.JPEG' in submission.url:
                # so that we can pass the filetype to the Post instance and name the file accordingly when we save it

                filetype = submission.url.split('.')[-1]
                if 'jpg' in filetype.lower():
                    filetype = 'jpg'
                elif 'png' in filetype.lower():
                    filetype = 'png'
                elif 'jpeg' in filetype.lower():
                    filetype = 'jpeg'

                print "\nURL is {}. Post id is {}".format(submission.url, submission.id)

                # do it all yo
                load_draw_save(post_dict, submission, filetype, attempt)

            elif submission.domain == 'imgur.com':
                # this is gross
                # so if the image does not have .jpg or .png or .JPEG in it's url, BUT it's domain is imgur.com
                # then this means that it is still an image, but the link goes to the viewing page on imgur, not the
                # actual image. So we will just add .jpg to the end of the url and carry on

                print "\nURL is {}. Post id is {}".format(submission.url, submission.id)

                try:
                    filetype = '.jpg'
                    # do it all yo
                    load_draw_save(post_dict, submission, filetype, attempt)
                except:
                    print 'Error loading file for post {}, skipping'.format(submission.id)


            else:
                print "\nIgnoring post {}, not a picture, url is {}".format(submission.id, submission.url)

        elif not doable:
            print '\nCould not find a suitable comment on this post'

    # move all images from this subreddit into a folder, add that folder path to 
    # list so that we can run thru them after and upload each image to an imgur album
    folder_paths.append(file_work(sub_name, outputFoldersPath))

    # write dictionary data from this subreddit to a file so that we can name pictures and 
    # write descriptions about each etc. 
    with open('{}/memedPost_json_data.txt'.format(folder_paths[-1]), 'w') as outfile:
        dump(post_dict, outfile)


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # #  Imgur API  # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# set the following variables that are needed for API calls
imgur_client_id, imgur_client_secret, imgur_refresh_token = ImgurAPI.load_imgur_creds()

# refresh access token, this will write the new access_token as an env variable
ImgurAPI.refresh_access(imgur_client_id, imgur_client_secret, imgur_refresh_token)

# pull value from environement variable
access_token = environ['imgur_access_token']

# folder_paths is a list of the path for each folder that we've saved images
# to when the program last ran. Of format /Users/usr/Env/etc....
for path in folder_paths:
    print '\n Uploading images to imgur album for files in {}'.format(path)
    # change directory to the folder path
    chdir(path)
    album_json = load_json()

    # if there is more than just the output json file in the folder (aka, if there are pictures in the folder)
    if listdir(curdir) > 1:
        album_title = '/r/{}'.format(album_json['subreddit'])

        album_description = """
        Imgur album created by the RedditMemeGen bot. The pictures in this album
        were generated from the 'hot' content in the {} subreddit at {}
        """.format(album_json['subreddit'], album_json['time'])

        # creates the imgur album for the images to be uploaded to. Returns the id of 
        # the album which needs to be passed with each image upload
        album_id = ImgurAPI.album_creation(album_title, album_description, access_token)

        # current directory is the folder_path
        num_images = len(listdir(curdir))
        image_uploaded_number = 0
        print 'Uplading Images \n'

        for targetFile in listdir(curdir):
            """
            Looks for images in the current directory, gets the postID from the image and then uses that
            to lookup it's dictionary entry. From there we use that data to create an image description
            to be used when each image is uploaded to imgur
            """
            if targetFile.startswith('memedPostPic'):
                image_uploaded_number += 1
            
                # gets the picture id from the image filename, uses this as the lookup value in the output dictionary
                picId = re.sub('memedPostPic', '', str(targetFile)).split('.')[0]
                picTitle = album_json['items'][picId]['postName'] + ' by /u/{}'.format(album_json['items'][picId]['postAuthor'])
                picName = picId 

                picDescription = ''

                picDescription += "Post URL: {}\n\n".format(album_json['items'][picId]['postUrl'])
                picDescription += "Top Comment: {}\n\n".format(album_json['items'][picId]['postComment'])
                picDescription += "Comment Author: /u/{}\n\n".format(album_json['items'][picId]['commentAuthor'])
                picDescription += "Picture URL: {}".format(album_json['items'][picId]['picUrl'])

                with open(targetFile, 'rb') as image_file:
                    encoded64_string = base64.b64encode(image_file.read())
                    ImgurAPI.upload_image(encoded64_string, album_id, picName, picTitle, picDescription, access_token














