# RedditMemeBot

Created 25 August 2015

Creates image-macros out of an image post on a subreddit and the top comment on that post

## Note!!!!!
If you clone this repo and use it, it will fail if it comes across an imgur album post. This is because I am using the imgur API to get the first image from any imgur album. Doing so requires passing a Client-ID in the header, I am loading this client-ID from an environment variable since it is specific to my registered application. I'd be happy to share the client-ID with anyone who wants to contribute, just message me as I did not want to leave it in the source. 


Additionally, the most recent changes to this program utilize the imgur API even further to upload images and create albums for my RedditMemeGenBot user account. The ImgurAPI module handles all of that code and the 'Imgur API' block of code in the main runs it. You will have to comment out that entire section or otherwise register an API account on Imgur and use your own credentials. I'd be happy to help anyone understand that further if asked :)

## Known Bugs
__Text Wrapping__ - every once in a while the text does not fit the image perfectly.


__Text Centering__ - passing alignt='center' to the PIL's ImageDraw does not produce the right results all of the time. Depending on the length of the string it may or may not center the text correctly. For now I think I will not center the text because it ends up being prettier in my opinion

## TODO
__Automation__ - once I get my raspberry pi setup at school I'll run this daily on a cron job against one or two subreddits (or maybe a random subreddit) 


__Imgur API__ - I'll be looking for a way to streamline the imgur API portion of the main. Currently the program is refreshing the access token each time it is run, regardless of whether or not the access token has expired or not. I'm going to try and find a way to check if the token has expired and then either refresh it or not. 

