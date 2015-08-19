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

#via redditlist.com/all
# top_subreddits = ['pics', 'todayilearned', 'aww', 'wtf',
#  'gaming', 'leagueoflegends', 'gonewild', 'me_irl', 'news', 'mildlyinteresting', 
#  'worldnews', 'politics', 'DotA2', 'pcmasterrace', 'TrollXChromosomes',
#  'SandersForPresident', 'GlobalOffensive', 'soccer', 'trees', 'interestingasfuck', 
#  'technology', 'nsfw', 'RealGirls', 'gentlemenboners', 'atheism', 'science', 'woahdude', 'food']

#above was for testing, idk too lazy to change it all back or whatver
top_subreddits = ['pics']


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

	for x, submission in enumerate(hot_posts):
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
				print "\nURL is {}. Post id is {}".format(submission.url, submission.id)
				#this is an image link ending in .jpg, will be okay for now

				targetPost = Post(submission, commentIndex=attempt)
				targetPost.add_text()

				#dictionary stuff for record keeping
				if submission.id not in post_dict['items']:
					post_dict['items'][targetPost.dict['postId']] = targetPost.dict
				#print post_dict
			else:
				print "Ignoring post {}, not a picture".format(submission.id)


	file_work(sub_name)

