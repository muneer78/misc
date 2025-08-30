from trafilatura import fetch_url, extract

url = "https://kk.org/thetechnium/103-bits-of-advice-i-wish-i-had-known/"
downloaded = fetch_url(url)
result = extract(downloaded)
print(downloaded)
