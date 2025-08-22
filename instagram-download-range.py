from datetime import datetime
from itertools import dropwhile, takewhile

import instaloader

L = instaloader.Instaloader()

USER = "thayungmun"
PROFILE = USER

L.interactive_login(USER)  # (ask password on terminal)


posts = instaloader.Profile.from_username(L.context, "account").get_posts()

SINCE = datetime(2014, 6, 24)
UNTIL = datetime(2007, 3, 1)

for post in takewhile(
    lambda p: p.date > UNTIL, dropwhile(lambda p: p.date > SINCE, posts)
):
    print(post.date)
    L.download_post(post, "account")

print("Completed")
