import reddit
r = reddit.Reddit(user_agent='my_cool_application')
submissions = r.get_subreddit('opensource').get_hot(limit=5)
[str(x) for x in submissions]

"""
import reddit

r = reddit.Reddit(user_agent='A very timid bot of u/GNeps')
r.login('gneps','enigma')

print r.get_subreddit('android').get_top(limit=10)
"""