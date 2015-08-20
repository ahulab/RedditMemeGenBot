import re, io
import urllib2 as urllib
from urllib2 import Request
from PIL import Image, ImageDraw, ImageFont
from StringIO import StringIO

#from MemeIt import *
path_to_font='/Library/Font/Trebuchet MS Bold.ttf'

class Post:

	def __init__(self, submission, filetype, commentIndex=0):
		self.dict ={
			'postId': submission.id,
			'postName': submission.title,
			'postComment': submission.comments[commentIndex].body,
			'postAuthor': submission.author,
			'postUrl': submission.permalink,
			'picUrl': submission.url,
			'postDate': submission.created,
			'commentAuthor': submission.comments[commentIndex].author
		}
		self.filetype = filetype
		self.draw_failed = None
		#initialized as None, but is loaded in the next step in main after it's initialized
		self.image = None


	def load_image(self, picUrl):
		try:
			picture = urllib.urlopen(picUrl)
			image_file = io.BytesIO(picture.read())
			img = Image.open(image_file).convert('RGB')
			self.image = img

		except urllib.HTTPError, e:
			self.image = None	

		except IOError:
			self.image = None	


	def add_text(self):
		
		#open current image
		draw = ImageDraw.Draw(self.image)

		##sanitize and encode text
		self.dict['postComment'] = re.sub(r'[\n\r]', '', self.dict['postComment']).encode('utf-8')


		#get both halfs of the string
		string_halves = self.halve_string()
		
		print "First half string length: {}. Second half length: {}".format(len(string_halves[0]), len(string_halves[1]))

		#counting number of words total so we can guess how many lines we will need to have		
		word_count = 0
		for i in string_halves[0]:
			if i == " ":
				word_count += 1
		for i in string_halves[1]:
			if i == " ":
				word_count += 1

		self.font_setup(string_halves, self.image.width, 10)

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
		

		new_size = self.font.size * lines
		self.font = ImageFont.truetype(path_to_font, size=new_size)


		#find the height of the string so that we know where to start of the y axis
		string_height = draw.textsize(string_halves[0])[1]
		#same drawing operation as was done with the first half of text
		self.split_to_fit(string_halves[1], draw, position='bottom')
		#draw the first half on the image
		self.split_to_fit(string_halves[0], draw, position='top')

		

		if self.draw_failed:
			#don't save the image
			pass
		else:
			self.image.save('memedPost{}.{}'.format(self.dict['postId'], self.filetype))


	def split_to_fit(self, string, draw, position):
		#string is first half of the message
		
		#split the string into multiple strings that we can write to the picture 
		#starting point for each slice
		begin_slice = 0
		end_slice = 0
		#string with newline chars. cannot modify string, need to create a new one to make changes
		new_string = ''
		#index of each space in the string
		spaces = []
		spaces_location = [(0,1)]
		#spaces_location [(character index in string, line number)]
		#number of newline chars inserted into the string, needed to calculate offset of text from bottom of image
		slice_count = 1

		#if draw.textsize(string)[0] > width:
		if self.font.getsize(string)[0] > self.image.width - 2:
			#if the string will not fit onto the image in one line then we will need to make some changes to it
			#otherwise it will stay the same
			num_spaces = 0
			for x, char in enumerate(string):
				if char == " ":
					spaces_location.append((x, slice_count))
				#if the character is a space then check to see if the chunk of text we're looking at 
				#will fit on the image, if it does not fit, then we need to stick a newline character in the string
				if self.font.getsize(string[begin_slice:x])[0] > self.image.width - 2:
					

					#get the second to last item in the list 'spaces'. This will be the space that was found last time
					#this portion of the loop was executed. We are going to stick a newline char in that spot
					#This is because otherwise we could potentially have a word that trails off of the end of the image
					
					#new_string += string[begin_slice:x - 1] + '\n'
					if spaces_location[-1][1] == slice_count or slice_count == 1:
						new_string += string[begin_slice:spaces_location[-1][0]] + '\n'
						begin_slice = spaces_location[-1][0] + 1
						
					else: 
						
						#last space is on a line above, insert new line at current location
						new_string += string[begin_slice:x - 2] + '\n'
						begin_slice = x - 2

					slice_count += 1
					end_slice = begin_slice
					
				else:
					#the current slice of text will fit in between the bounds of the image
					pass

			#print "1. height from bottom is {}".format(height - font.getsize(new_string)[1] * slice_count)


			new_string += string[end_slice:]


		#elif draw.textsize(string)[0] >= width:
		elif self.font.getsize(string)[0] <= self.image.width:
			#do nothing because the string will fit
			new_string = string

		#return [new_string, slice_count]

		
		self.draw_meme_string(new_string, slice_count, draw, string, position=position)



	def draw_meme_string(self, new_string, slice_count, draw, string, position):
		no_text_zone = ((self.image.height/9*4), (self.image.height/9*5))

		#see if bottom text goes over the no text zone in the middle of the photo
		#we only need to check the bottom because bottom text is written first, so if there is an issue with text size
		#it will be fixed by the time this function is called with the the top text
		if position == 'bottom' and (self.font.getsize(new_string)[1] * slice_count) < self.image.height * .15:
		\
			font_size = int(self.font.size * 1.2)
			self.font = ImageFont.truetype(path_to_font, size=font_size)
			self.split_to_fit(string, draw, position)

		else:

			if position == 'bottom' and self.font.getsize(new_string)[1] * slice_count < self.image.height - no_text_zone[1] or position == 'top':
				
					#depending on arg, text will be written on top or bottom
				if position == 'top':
					xy = (0,0)
				elif position == 'bottom':
					slice_count = 1
					for i in new_string:
						if i == '\n':
							slice_count += 1

					#find height of text using selected font, multiply that by the number of slices to know how high up we must start
					xy = (0,(self.image.height - self.font.getsize(new_string)[1] * slice_count))
				
				#print 'drawing {} at {}'.format(new_string, xy)
				try:
					draw.multiline_text(xy,new_string,fill='black', font=self.font)
					ab = (xy[0] + 2, xy[1] + 2)
					draw.multiline_text(ab,new_string,fill='white', font=self.font)
					self.draw_failed = False
				except:
					self.draw_failed = True
					print "Drawing failed, not modifying picture"
				

			else:
				#the text is too large and goes over our no text zone
				font_size = int(self.font.size / 1.5)
				self.font = ImageFont.truetype(path_to_font, size=font_size)
				self.split_to_fit(string, draw, position)

		


	def find_center(width):
		try:
			center = round((width / 2))
			return center
		except (TypeError):
			print 'find_center takes an int as an arg. The arg "{}" is of type: {}'.format(width, type(width))
			print "Exiting..."
			exit()


	def font_setup(self, string_halves, width, size, last_size=None):
		font = ImageFont.truetype(path_to_font, size=size)

		if font.getsize(string_halves[0])[0] > width or font.getsize(string_halves[1])[0] > width:
			#the line goes over, this is fine
			print "Choosing font size of {}".format(last_size)
			if last_size:
				#print 'last_size is not null'
				font = ImageFont.truetype(path_to_font, size=last_size)
				self.font = font
				return font
				

			else:
				#this will only execute if this is the first time this function has been called (ie. last_size is None) and size 10 is too
				#large of a text size for the image. I'm just going to leave it at 10 for now
				font = ImageFont.truetype(path_to_font, size=10)
				self.font = font
				return font

		elif font.getsize(string_halves[0])[0] < width or font.getsize(string_halves[1])[0] < width:
			last_size = size
			size += 4
			font = self.font_setup(string_halves, width, size, last_size=last_size)

		self.font = font
		return font


	def halve_string(self):
		first_half = ''
		second_half = ''
		string = []

		#split on spaces
		for i in self.dict['postComment'].split(' '):
			#do not add blank whitespaces to array
			if len(i) <> 0:
				string.append(i)

		#divide length by two to find middle of list, change type to int
		half = int(round(len(string)/2))

		#now we have a list of the first and second half of the string to print
		#the first half will go on the top of the image, the second on the bottom
		for x, i in enumerate(string[0:half]):
			if string.index(i) == half - 1:
				first_half += i
			else:
				first_half += i + " "

		for i in string[half:]:
			if string.index(i) == len(string) - 1:
				second_half += i
			else:
				second_half += i + " "

		#returns 2 strings
		return first_half, second_half


