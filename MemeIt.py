from PIL import Image, ImageDraw, ImageFont

path_to_font='/Library/Font/Phosphate.ttc'

def draw_meme_text(string, width, height, font, draw, position):
	#string is first half of the message
	string_list = string.split(' ')

	#split the string into multiple strings that we can write to the picture 
	#starting point for each slice
	begin_slice = 0
	end_slice = 0
	#string with newline chars. cannot modify string, need to create a new one to make changes
	new_string = ''
	#index of each space in the string
	spaces = []
	#number of newline chars inserted into the string, needed to calculate offset of text from bottom of image
	slice_count = 1

	#if draw.textsize(string)[0] > width:
	if font.getsize(string)[0] > width:
		#if the string will not fit onto the image in one line then we will need to make some changes to it
		#otherwise it will stay the same
		for x, char in enumerate(string):
			if char == " ":
				spaces.append(x)
				#if the character is a space then check to see if the chunk of text we're looking at 
				#will fit on the image, if it does not fit, then we need to stick a newline character in the string
				#if draw.textsize(string[begin_slice:x])[0] > width:
				if font.getsize(string[begin_slice:x])[0] > width:
					slice_count += 1

					#get the second to last item in the list 'spaces'. This will be the space that was found last time
					#this portion of the loop was executed. We are going to stick a newline char in that spot
					#This is because otherwise we could potentially have a word that trails off of the end of the image
					new_string += string[begin_slice:spaces[(len(spaces)-2)]] + '\n'
					
					#start on a new slice of text to add. start one word earlier than the current word
					begin_slice = spaces[(len(spaces)-2)] + 1

					#the end of this slice is one character after the space, so the start of the next word..
					end_slice = x + 1
				else:
					#the current slice of text will fit in between the bounds of the image
					pass


		new_string += string[end_slice:]

	#elif draw.textsize(string)[0] >= width:
	elif font.getsize(string)[0] <= width:
		#do nothing because the string will fit
		new_string = string

	#depending on arg, text will be written on top or bottom
	if position == 'top':
		xy = (0,0)
	elif position == 'bottom':
		#find height of text using selected font, multiply that by the number of slices to know how high up we must start
		xy = (0,(height - font.getsize(new_string)[1] * slice_count))
	
	#print 'drawing {} at {}'.format(new_string, xy)
	draw.multiline_text(xy,new_string,(255,255,255), font=font)


def find_center(width):
	try:
		center = round((width / 2))
		return center
	except (TypeError):
		print 'find_center takes an int as an arg. The arg "{}" is of type: {}'.format(width, type(width))
		print "Exiting..."
		exit()


def font_setup(string_halves, width, size, last_size=None):
	font = ImageFont.truetype(path_to_font, size=size)

	if font.getsize(string_halves[0])[0] > width or font.getsize(string_halves[1])[0] > width:
		#the line goes over, this is fine
		print "Choosing size of {}".format(last_size)
		if last_size:
			#print 'last_size is not null'
			font = ImageFont.truetype(path_to_font, size=last_size)
			return font

		else:
			#this will only execute if this is the first time this function has been called (ie. last_size is None) and size 10 is too
			#large of a text size for the image. I'm just going to leave it at 10 for now
			font = ImageFont.truetype(path_to_font, size=10)

	elif font.getsize(string_halves[0])[0] < width or font.getsize(string_halves[1])[0] < width:
		last_size = size
		size += 4
		font = font_setup(string_halves, width, size, last_size=last_size)

	return font



def halve_string(meme_string):
	first_half = ''
	second_half = ''
	string = []

	#split on spaces
	for i in meme_string.split(' '):
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






