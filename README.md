#RedditMemeBot

Work in progress

Creates image-macros out of an image post on a subreddit and the top comment on that post

##Note:
If you clone this repo and use it, it will fail if it comes across an imgur album post. This is because I am using the imgur API to get the first image from any imgur album. Doing so requires passing a Client-ID in the header, I am loading this client-ID from an environment variable on my mac since it is specific to my registered application. I'd be happy to share the client-ID with anyone who wants to contribute, just message me as I did not want to leave it in the source. 

##Known Bugs
I'm playing with the text wrapping, every once in a while the text does not fit the image perfectly. 
