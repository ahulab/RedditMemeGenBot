from PostCollection import Post
import praw
from os import listdir, mkdir, curdir, environ
from shutil import move
from time import gmtime, strftime
import urllib2 as urllib
from json import loads


def load_json():
	"""loads past data so that we don't meme-ify the same posts over and over"""
	pass


def save_json():
	"""saves dictionary created during runtime"""
	pass


def file_work(sub_name):
	#moves all pictures from runtime to folder
	#get time for folder name
	time = strftime("%a, %d %b %Y at %H:%M", gmtime())
	folder_name = "{}: {}".format(sub_name, time)
	#create folder with time as name
	mkdir("./{}".format(folder_name))
	#folder path
	folder_path = "./{}".format(folder_name)

	#list of all files in current directory
	names = listdir(curdir)
	for i in names:
		#all memed images will start with memedPost and have the postId appended by the Post class
		if i.startswith('memedPost'):
			#use shutil.move to move images to folder for safe keeping :)
			move(i, folder_path)


def load_draw_save(submission, filetype, commentIndex, album=False, album_id=None):
	targetPost = Post(submission, filetype, commentIndex=commentIndex)
	
	if album:
		#must load from environment variable or change this line manually
		#this app is registered with imgurs API
		imgur_client_id = environ['imgur_client_id']

		request = urllib.Request('https://api.imgur.com/3/album/%s' % album_id, headers={'Authorization': 'Client-ID %s' % imgur_client_id})
		content = urllib.urlopen(request).read()
		content = loads(content)

		#need error handling
		url = content['data']['images'][0]['link']
		targetPost.load_image(url)

	else:
		url = submission.url + '.jpg'
		targetPost.load_image(url)

	if targetPost.image:
		#checking to see if the image loaded correctly, if it didn't then we just skip and move on
		targetPost.add_text()

		# dictionary stuff for record keeping
		if submission.id not in post_dict['items']:
			post_dict['items'][targetPost.dict['postId']] = targetPost.dict


#via redditlist.com/all
#top_subreddits = ['wtf', 'aww', 'space', 'creepy', 'spaceporn', 'pics', 'whatsthisplant', 'whatsthisbug', 'animalID', 'whatsthisbird',
#'Whatisthisthing', 'mildlyinteresting', 'whatsthisrock', 'FossilID',  'nsfw', 'gonewild']
top_subreddits = ['pics']


######################################
########### main stuff ###############
######################################

#load from json file here instead in the future maybe
post_dict = {
	'items':{}
}

user_agent = "Meme generator bot v1.0 by /u/cDoubt"
r = praw.Reddit(user_agent=user_agent)

for subreddit in top_subreddits:
	sub_name = subreddit
	pics_subreddit = r.get_subreddit(sub_name)
	hot_posts = pics_subreddit.get_hot(limit=60)
	#other options include
	#get_top_from_all
	#get_top
	#get_hot
	#get_top_from_month
	#get_top_from_week


	#submission = r.get_submission(submission_id='3hrv35')
	#for x in range(0,1):
	for submission in hot_posts:

		#make sure there is at least 1 comment in the submission
		if submission.comments > 0:
			#boolean to run the main 
			doable = False
			#try 3 times to find a suitable comment
			for attempt in range(0,3):
				try:
					#for instance, if someone comments with a link to an imgur album, it could error out, so we try again
					if len(submission.comments[attempt].body) > 0:
						comment = attempt
						doable = True
						#break once we find a comment, this commend gets passed to the init function of the post class
						break
				except:
					pass

		#if it's not doable it's because the above if statement could not find a suitable comment, or any comment at all
		if doable:
			#to handle imgur albums we just get the first image from the album
			if submission.domain == 'imgur.com' and '/a/' in submission.url:
				album_id = submission.url.split('/a/')[-1]

				print "\nURL is {}. It is an imgur album. Post id is {}".format(submission.url, submission.id)
				load_draw_save(submission, 'jpg', attempt, album=True, album_id=album_id)

			#otherwise we find the filetype of the picture
			elif '.jpg' in submission.url or '.png' in submission.url or '.JPEG' in submission.url:
				
				#so that we can pass the filetype to the Post instance and name the file accordingly when we save it
				filetype = submission.url.split('.')[-1]
				if 'jpg' in filetype.lower():
					filetype = 'jpg'
				elif 'png' in filetype.lower():
					filetype = 'png'
				elif 'jpeg' in filetype.lower():
					filetype = 'jpeg'

				print "\nURL is {}. Post id is {}".format(submission.url, submission.id)

				#do it all yo
				load_draw_save(submission, filetype, attempt)

			elif submission.domain == 'imgur.com':
				#this is gross
				#so if the image does not have .jpg or .png or .JPEG in it's url, BUT it's domain is imgur.com
				#then this means that it is still an image, but the link goes to the viewing page on imgur, not the
				#actual image. So we will just add .jpg to the end of the url and carry on

				print "\nURL is {}. Post id is {}".format(submission.url, submission.id)

				try:
					filetype = 'jpg'
					#do it all yo
					load_draw_save(submission, filetype, attempt)
				except:
					print 'Error loading file for post {}, skipping'.format(submission.id)

				
			else:
				print "Ignoring post {}, not a picture, url is {}".format(submission.id, submission.url)

	file_work(sub_name)

