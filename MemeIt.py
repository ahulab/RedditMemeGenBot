from PIL import Image, ImageDraw, ImageFont


#stringy = """Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse ac lorem orci. Suspendisse libero felis, fringilla nec quam quis, dictum finibus odio. Morbi at facilisis arcu, a porta elit. Morbi odio enim, molestie ac lobortis et, vestibulum sed elit. Integer faucibus felis at dui pulvinar ornare. Mauris scelerisque ultricies mauris, in vehicula tortor cursus sed. Pellentesque ultrices porttitor urna, in cursus neque elementum id. Suspendisse iaculis tincidunt nulla in feugiat. Phasellus et risus vel nisi feugiat maximus. Quisque eget dictum urna. Integer auctor, ipsum vel fringilla egestas, mauris magna ullamcorper arcu, pharetra porttitor magna elit quis quam. Mauris semper finibus elit ut bibendum. Praesent nec placerat purus, sit amet convallis nibh. Donec ut ornare nisl. Nunc hendrerit felis eget turpis dignissim laoreet. Donec commodo eget neque sed sodales. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Nullam ultricies congue ullamcorper. Phasellus mollis erat consectetur orci efficitur, sed tincidunt mauris congue. Donec vel viverra sem. Praesent lorem purus, eleifend eget ex id, tincidunt commodo purus. Nam id velit lorem. Interdum et malesuada fames ac ante ipsum primis in faucibus. In hac habitasse platea dictumst. Donec pharetra at massa eget dapibus. Vestibulum mauris augue, auctor a dolor nec, ultrices molestie massa. Nunc sit amet gravida felis. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Fusce sed aliquam purus. Nam ullamcorper lacus eget aliquam luctus. Sed vitae tortor sit amet nisl gravida porttitor nec sed risus. Suspendisse placerat, libero eu tristique pharetra, augue magna congue augue, ultrices egestas ligula lacus mollis tortor. In tristique bibendum tellus non malesuada. Donec varius arcu eu eleifend tincidunt. Quisque molestie sit amet ex vel ultrices.
#"""
globalFont = int
path_to_font = "/Library/Fonts/Silom.ttf"
path_to_image = "test.jpg"

stringy = "Lorem ipsum dolor sit amet, this is a test so deal with it"

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

	if font.getsize(string_halves[0])[0] > width:
		#the line goes over, this is fine
		print "text goes over"
		if last_size:
			print 'last_size is not null'
			font = ImageFont.truetype(path_to_font, size=last_size)
			return font
			globalFont = last_size


		else:
			#this will only execute if this is the first time this function has been called (ie. last_size is None) and size 10 is too
			#large of a text size for the image. I'm just going to leave it at 10 for now
			print 'last_size is null'
			font = ImageFont.truetype(path_to_font, size=10)
			globalFont = 10

	elif font.getsize(string_halves[0])[0] < width:
		#the line does not go over, we want it to be longer then
		last_size = size
		size += 5
		##print "increasing size by 10"
		##print font.size
		#recursive bit
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

	return first_half, second_half


def draw_meme_text(string, width, height, font, position):
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



#open current image
im = Image.open(path_to_image)
draw = ImageDraw.Draw(im)


##if i need to try sanitizing text
# meme_string = meme_string.rstrip('\r\n')
# stringy = stringy.rstrip('\r\n')

#get both halfs of the string
string_halves = halve_string(stringy)
#print string_halves

#choosing font size

fnt = font_setup(string_halves, im.width, 10)
#dirty, gives us x lines of text so that text isn't super small on image
lines = 1
new_size = fnt.size * lines
fnt = ImageFont.truetype(path_to_font, size=new_size)
print fnt.size

#draw the first half on the image
draw_meme_text(string_halves[0], im.width, im.height, fnt, position='top')

#find the height of the string so that we know where to start of the y axis
string_height = draw.textsize(string_halves[0])[1]
#same drawing operation as was done with the first half of text
draw_meme_text(string_halves[1], im.width, im.height, fnt, position='bottom')


im.save('edited.jpg')
im.show()




