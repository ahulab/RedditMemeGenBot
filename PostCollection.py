import praw, requests, re
from PIL import Image, ImageDraw, ImageFont
from StringIO import StringIO

from MemeIt import *

def add_text(image, post_id, comment):
	#open current image
	#image = Image.open(path_to_image)

	draw = ImageDraw.Draw(image)

	##if i need to try sanitizing text
	# meme_string = meme_string.rstrip('\r\n')
	comment = re.sub(r'[\n\r]', '', comment).encode('utf-8')


	#get both halfs of the string
	string_halves = halve_string(comment)
	#print string_halves
	print "First half string length: {}. Second half length: {}".format(len(string_halves[0]), len(string_halves[1]))
	#choosing font size

	word_count = 0
	for i in string_halves[0]:
		if i == " ":
			word_count += 1
	for i in string_halves[1]:
		if i == " ":
			word_count += 1

	print word_count
	fnt = font_setup(string_halves, image.width, 10)

	#some guesswork. depending on the number of words we are going to make the image have x lines of text
	#this is so that images with long comments do not just have one long line of unlegible text across the top and bottom
	if word_count < 20:
		lines = 1
	elif word_count > 20 and word_count < 60:
		lines = 3
	elif word_count > 60 < 150:
		lines = 5
	else:
		lines = 6

	new_size = fnt.size * lines
	fnt = ImageFont.truetype(path_to_font, size=new_size)

	#draw the first half on the image
	draw_meme_text(string_halves[0], image.width, image.height, fnt, draw, position='top')

	#find the height of the string so that we know where to start of the y axis
	string_height = draw.textsize(string_halves[0])[1]
	#same drawing operation as was done with the first half of text
	draw_meme_text(string_halves[1], image.width, image.height, fnt, draw, position='bottom')


	image.save('{}.jpg'.format(post_id))
	#image.show()


######################################
########### main stuff ###############
######################################

user_agent = "Meme generator bot 0.1 by /u/cDoubt"
r = praw.Reddit(user_agent=user_agent)

pics_subreddit = r.get_subreddit('pics')
hot_posts = pics_subreddit.get_top_from_year(limit=50)

#gets 25 'hot' submissions in the subreddit
pics_posts = []
for x, i in enumerate(hot_posts):
	#print i.title
	if i.comments > 0:
		pics_posts.append((i.title, i.comments[0].body))

		if '/a/' not in i.url and '.jpg' in i.url:
			print "\nURL is {}. Post id is {}".format(i.url, i.id)
			#this is an image link ending in .jpg, will be okay for now
			picture = requests.get(i.url)
			img = Image.open(StringIO(picture.content))
			add_text(img, i.id, i.comments[0].body)