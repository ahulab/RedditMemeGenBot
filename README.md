#RedditMemeBot

In progress

Creates image-macros out of an image post on a subreddit and the top comment on that post

##Note:
If you clone this repo and use it, it will fail if it comes across an imgur album post. This is because I am using the imgur API to get the first image from any imgur album. Doing so requires passing a Client-ID in the header, I am loading this client-ID from an environment variable on my mac since it is specific to my registered application. I'd be happy to share the client-ID with anyone who wants to contribute, just message me as I did not want to leave it in the source. 

##Known Bugs
__Text Wrapping__ - every once in a while the text does not fit the image perfectly.


__Text Centering__ - passing alignt='center' to the PIL's ImageDraw does not produce the right results all of the time. Depending on the length of the string it may or may not center the text correctly. For now I think I will not center the text because it ends up being prettier in my opinion

##TODO
__Automomation__ - once I get my raspberry pi setup at school I'll run this daily on a cron job against one or two subreddits (or maybe a random subreddit) 


__Imgur API__ - I plan on utilizing the imgur api to automatically upload the results to a gallery on imgur. In that gallery I'd like to have each picture with a description that includes: A link to the original post, the post author's username, a creation date of the post, the top comment text, and the top comment author's username. This information is being collected already and stored in a dictionary. I'm going to have to do some reading on the Imgur API documentation. 

