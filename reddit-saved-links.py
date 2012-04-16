# -*- coding: utf-8 -*-
import os
import re
import time
import shelve
from contextlib import closing
import getpass
import reddit
import argparse
import webbrowser

HTML_OUTPUT_FILE = 'saved-links.html'

def _getSubreddit(submission):
	"""Returns subreddit of said submission, or "Saved comments" if it's not link to a submission but a comment."""
	try:
		return re.findall("www.reddit.com/r/([^/]*)/", submission.permalink)[0]
	except IndexError:
		#raise Error("Cannot parse submission subreddit for: " + submission.permalink)
		return "Saved comments"

def getSavedLinksBySubreddit(username, password):
	r = reddit.Reddit(user_agent='A very timid bot of u/GNeps')
	try:
		r.login(username, password)
		submissions = r.get_saved_links(limit=None)

		saved = dict()
		for x in submissions:
			saved.setdefault(_getSubreddit(x), []).append(x)
			
		return sorted(saved.items(), key=lambda (a, b): -len(b))
	except reddit.errors.InvalidUserPass:
		print "Invalid username or password."

def printSavedLinksBySubreddit(savedLinks):
	for subreddit, submissions in savedLinks:
		print subreddit
		for submission in submissions:
			print "\t", str(submission)

def htmlSavedLinksBySubreddit(savedLinks):
	with open(HTML_OUTPUT_FILE, "w") as html:
		html.write("<html>\n<body>\n\n");
		html.write("<h1>Saved links from Reddit sorted by subreddits</h1>\n")
		html.write("I found a total of %s saved links in %s subreddits.\n\n\n" % (
				sum(len(b) for (a, b) in savedLinks), len(savedLinks)))
		
		for subreddit, submissions in savedLinks:
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
	# Let's find out what the user wants.
	argparser = argparse.ArgumentParser(description='Reddit saved links by subreddit.')
	argparser.add_argument('-c','--credentials', action='store_true')
	argparser.add_argument('-r','--reload', action='store_true')
	cmdargs = argparser.parse_args()
	
	# Let's do our magic.
	if not os.path.exists(HTML_OUTPUT_FILE) or cmdargs.reload or cmdargs.credentials:
		with closing(shelve.open("settings.dat", writeback=True)) as settings:
			if not settings.has_key('username') or not settings.has_key('password') or cmdargs.credentials:
				settings['username'] = raw_input('Reddit username: ')
				settings['password'] = getpass.getpass()

			savedLinks = getSavedLinksBySubreddit(settings['username'], settings['password'])
			if savedLinks:
				htmlSavedLinksBySubreddit(savedLinks)
	
	webbrowser.open(HTML_OUTPUT_FILE)



		
		
		