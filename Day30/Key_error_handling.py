facebook_posts = [
    {'Likes': 21, 'Comments': 2},
    {'Likes': 13, 'Comments': 2, 'Share': 1},
    {'Likes': 33, 'Comments': 8, 'Share': 3},
    {'Comments': 4, 'Share': 2},
    {'Comments': 1, 'Share': 1},
    {'Likes': 19, 'Comments': 3}
]

total_likes = 0

for post in facebook_posts:
    try:
        total_likes = total_likes + post['Likes']
    except KeyError:
        print("ignore")
        # OR pass
        # OR total_likes += 0

print(total_likes)
