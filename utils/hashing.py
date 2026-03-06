import hashlib


def generate_lead_hash(post_url, profile_url, comment_text):

    unique_string = f"{post_url}-{profile_url}-{comment_text}"

    return hashlib.sha256(unique_string.encode()).hexdigest()

'''
duplicate leads prevent karo

Isliye hum generate karenge:

hash(post_url + profile_url + comment_text)

Example output:

b41c9d89e3d3...

Agar hash already exist karta hai → lead skip.
'''