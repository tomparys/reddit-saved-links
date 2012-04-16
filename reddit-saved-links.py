# -*- coding: utf-8 -*-
import re
import time
import reddit

def _getSubreddit(submission):
	"""Returns subreddit of said submission, or "Saved comments" if it's not link to a submission but a comment."""
	try:
		return re.findall("www.reddit.com/r/([^/]*)/", submission.permalink)[0]
	except IndexError:
		#raise Error("Cannot parse submission subreddit for: " + submission.permalink)
		return "Saved comments"

def getSavedLinksBySubreddit(username, password):
	r = reddit.Reddit(user_agent='A very timid bot of u/GNeps')
	r.login(username, password)
	submissions = r.get_saved_links(limit=None)

	saved = dict()
	for x in submissions:
		saved.setdefault(_getSubreddit(x), []).append(x)
		
	return sorted(saved.items(), key=lambda (a, b): -len(b))

def printSavedLinksBySubreddit():
	saved = getSavedLinksBySubreddit('gneps','enigma')
	for subreddit, submissions in saved:
		print subreddit
		for submission in submissions:
			print "\t", str(submission)

def htmlSavedLinksBySubreddit():
	saved = getSavedLinksBySubreddit('gneps','enigma')
	
	with open("saved-links.html", "w") as html:
		html.write("<html>\n<body>\n\n");
		html.write("<h1>Saved links from Reddit sorted by subreddits</h1>\n")
		html.write("I found a total of %s saved links in %s subreddits.\n\n\n" % (
				sum(len(b) for (a, b) in saved), len(saved)))
		
		for subreddit, submissions in saved:
			html.write("<h2>" + subreddit + "</h2>\n<ul>\n")
			
			for submission in submissions:
				try:
					html.write("<li><a href='%s'>%s</a>\n" % (submission.permalink, str(submission)))
				except UnicodeEncodeError:
					#print "UnicodeError for:", submission.permalink
					html.write("<li><a href='%s'>%s</a>\n" % (submission.permalink, "Name unknown"))
			html.write("</ul>\n\n\n")
		
		html.write("</body>\n</html>\n");

	
if __name__ == "__main__":
	htmlSavedLinksBySubreddit()