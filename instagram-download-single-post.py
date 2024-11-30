import instaloader

# Initialize Instaloader with no metadata
L = instaloader.Instaloader(download_comments=False, 
                            save_metadata=False, 
                            post_metadata_txt_pattern="")

USER = "thayungmun"
SHORTCODE = "DCXi7iHzS0t"

# Interactive login to fetch the session (asks for password)
L.interactive_login(USER)

# Get the post by shortcode
post = instaloader.Post.from_shortcode(L.context, SHORTCODE)

# Download only the picture
L.download_post(post, target="picture_only")

print("Picture download completed")
