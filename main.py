from PostCollection import Post
import praw
from os import listdir, mkdir, curdir
from shutil import move
from time import gmtime, strftime


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


def load_draw_save(submission, filetype, commentIndex):
	targetPost = Post(submission, filetype, commentIndex=commentIndex)
	url = submission.url + '.jpg'
	targetPost.load_image(url)

	if targetPost.image:
		targetPost.add_text()

		# dictionary stuff for record keeping
		if submission.id not in post_dict['items']:
			post_dict['items'][targetPost.dict['postId']] = targetPost.dict

#via redditlist.com/all
# top_subreddits = ['pics', 'todayilearned', 'aww', 'wtf',
#  'gaming', 'leagueoflegends', 'gonewild', 'me_irl', 'news', 'mildlyinteresting', 
#  'worldnews', 'politics', 'DotA2', 'pcmasterrace', 'TrollXChromosomes',
#  'SandersForPresident', 'GlobalOffensive', 'soccer', 'trees', 'interestingasfuck', 
#  'technology', 'nsfw', 'RealGirls', 'gentlemenboners', 'atheism', 'science', 'woahdude', 'food']

#above was for testing, idk too lazy to change it all back or whatver
top_subreddits = ['whatisthisthing']


######################################
########### main stuff ###############
######################################

#load from json file here instead
post_dict = {
	'items':{}
}

user_agent = "Meme generator bot 0.1 by /u/cDoubt"
r = praw.Reddit(user_agent=user_agent)

for subreddit in top_subreddits:
	sub_name = subreddit
	pics_subreddit = r.get_subreddit(sub_name)
	hot_posts = pics_subreddit.get_top_from_all(limit=50)
	#other options include
	#get_top
	#get_hot
	#get_top_from_month
	#get_top_from_week

	#gets 25 'hot' submissions in the subreddit

	for submission in hot_posts:
		#print submission.title
		
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

		if doable:
			if '/a/' not in submission.url and '.jpg' in submission.url or '.png' in submission.url or '.JPEG' in submission.url:
				
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
					print 'error'

				
			else:
				print "Ignoring post {}, not a picture, url is {}".format(submission.id, submission.url)


	file_work(sub_name)

