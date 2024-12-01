import instaloader

# Initialize Instaloader with no metadata
L = instaloader.Instaloader(download_comments=False, 
                            save_metadata=False, 
                            post_metadata_txt_pattern="")

USER = "thayungmun"

# Interactive login to fetch the session (asks for password)
L.interactive_login(USER)

# Load the profile
profile = instaloader.Profile.from_username(L.context, USER)

# Get all saved posts
saved_posts = profile.get_saved_posts()

# Download only the pictures
for post in saved_posts:
    L.download_post(post, target=r"/Users/muneer78/Downloads/saved_posts")

print("Picture downloads completed")
