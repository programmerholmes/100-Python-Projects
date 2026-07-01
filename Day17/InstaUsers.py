class Users:

    def __init__(self, user_id, username):
        self.user_id = user_id
        self.username = username
        self.followers = 0
        self.following = 0

    def follow(self, user):
        user.followers += 1
        self.following += 1


User_1 = Users("001", "Jack")
User_2 = Users("002", "Sparrow")
User_1.follow(User_2)


print(User_1.username)
print(User_1.followers)
print(User_1.followers)
print(User_1.following)
print(User_2.followers)
print(User_2.following)
