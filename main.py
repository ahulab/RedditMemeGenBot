from PostCollection import Post
import praw

######################################
########### main stuff ###############
######################################

#load from json file here instead
post_dict = {
	'items':{}
}


user_agent = "Meme generator bot 0.1 by /u/cDoubt"
r = praw.Reddit(user_agent=user_agent)

pics_subreddit = r.get_subreddit('pics')
hot_posts = pics_subreddit.get_top_from_year(limit=50)

#gets 25 'hot' submissions in the subreddit

for x, submission in enumerate(hot_posts):
	#print submission.title
	if submission.comments > 0:

		if '/a/' not in submission.url and '.jpg' in submission.url:
			print "\nURL is {}. Post id is {}".format(submission.url, submission.id)
			#this is an image link ending in .jpg, will be okay for now

			targetPost = Post(submission)
			targetPost.add_text()

			
			#Post.add_text(img, submission.id, submission.comments[0].body)

			#dictionary stuff for record keeping
			if submission.id not in post_dict['items']:
				post_dict['items'][targetPost.dict['postId']] = targetPost.dict
			print post_dict