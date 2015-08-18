import praw, requests, re
from PIL import Image, ImageDraw, ImageFont
from StringIO import StringIO

from MemeIt import *

def add_text(image, post_id, comment):
	#open current image
	#im = Image.open(path_to_image)

	im = image
	draw = ImageDraw.Draw(im)


	##if i need to try sanitizing text
	# meme_string = meme_string.rstrip('\r\n')
	comment = re.sub(r'[\n\r]', '', comment)

	#get both halfs of the string
	string_halves = halve_string(comment)
	#print string_halves
	print len(string_halves)
	#choosing font size

	fnt = font_setup(string_halves, im.width, 10)
	#dirty, gives us x lines of text so that text isn't super small on image

	lines = 1
	new_size = fnt.size * lines
	fnt = ImageFont.truetype(path_to_font, size=new_size)
	print fnt.size

	#draw the first half on the image
	draw_meme_text(string_halves[0], im.width, im.height, fnt, draw, position='top')

	#find the height of the string so that we know where to start of the y axis
	string_height = draw.textsize(string_halves[0])[1]
	#same drawing operation as was done with the first half of text
	draw_meme_text(string_halves[1], im.width, im.height, fnt, draw, position='bottom')


	im.save('{}.jpg'.format(post_id))
	#im.show()

user_agent = "Meme generator bot 0.1 by /u/cDoubt"
r = praw.Reddit(user_agent=user_agent)

#submission = r.get_submission(submission_id='3he9zi')
#forest_comments = submission.comments
pics_subreddit = r.get_subreddit('pics')
hot_posts = pics_subreddit.get_hot()

#gets 25 'hot' submissions in the subreddit
pics_posts = []
for x, i in enumerate(hot_posts):
	#print i.title
	if i.comments > 0:
		pics_posts.append((i.title, i.comments[0].body))

		if '/a/' not in i.url and '.jpg' in i.url:
			print i.url, i.id
			#this is an image link ending in .jpg, will be okay for now
			picture = requests.get(i.url)
			img = Image.open(StringIO(picture.content))
			add_text(img, i.id, i.comments[0].body)

			#img.show()


