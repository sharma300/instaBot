import requests, urllib
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer

APP_ACCESS_TOKEN = '1773713678.5a4c43f.4577640077dd49549abf9a94363db447'


BASE_URL = 'https://api.instagram.com/v1/'

'''
Function declaration to get your own info
'''


def self_info():
    request_url = (BASE_URL + 'users/self/?access_token=%s') % (APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_info = requests.get(request_url).json()

    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
            print 'Username: %s' % (user_info['data']['username'])
            print 'No. of followers: %s' % (user_info['data']['counts']['followed_by'])
            print 'No. of people you are following: %s' % (user_info['data']['counts']['follows'])
            print 'No. of posts: %s' % (user_info['data']['counts']['media'])
        else:
            print 'User does not exist!'
    else:
        print 'Status code other than 200 received!'


'''
Function declaration to get the ID of a user by username
'''


def get_user_id(insta_username):
    request_url = (BASE_URL + 'users/search?q=%s&access_token=%s') % (insta_username, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_info = requests.get(request_url).json()

    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
            return user_info['data'][0]['id']
        else:
            return None
    else:
        print 'Status code other than 200 received!'
        exit()


'''
Function declaration to get the info of a user by username
'''


def get_user_info(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'User does not exist!'
        exit()
    request_url = (BASE_URL + 'users/%s?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_info = requests.get(request_url).json()

    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
            print 'Username: %s' % (user_info['data']['username'])
            print 'No. of followers: %s' % (user_info['data']['counts']['followed_by'])
            print 'No. of people you are following: %s' % (user_info['data']['counts']['follows'])
            print 'No. of posts: %s' % (user_info['data']['counts']['media'])
        else:
            print 'There is no data for this user!'
    else:
        print 'Status code other than 200 received!'


'''
Function declaration to get your recent post
'''


def get_own_post():
    request_url = (BASE_URL + 'users/self/media/recent/?access_token=%s') % (APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    own_media = requests.get(request_url).json()

    if own_media['meta']['code'] == 200:
        if len(own_media['data']):
            image_name = own_media['data'][0]['id'] + '.jpeg'
            image_url = own_media['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(image_url, image_name)
            print 'Your image has been downloaded!'
        else:
            print 'Post does not exist!'
    else:
        print 'Status code other than 200 received!'

'''
Function declaration to get the recent post of a user by username
'''
def get_post_liked_by_user():
    request_url = (BASE_URL + 'users/self/media/liked?access_token=%s') % (APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    media_list = requests.get(request_url).json()
    if media_list['meta']['code'] == 200:
        if len(media_list['data']):
            print 'Username of post whose post user liked \n '
            for i in range(0,len(media_list['data'])):
                print media_list['data'][i]['user']['username']
        else:
            print 'User did not like any post.\n'
    else:
        print 'Not able to fetch post liked by user. Try agai.'


'''
Function declaration to get the recent post of a user by username
'''


def get_user_post(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'User does not exist!'
        exit()
    request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_media = requests.get(request_url).json()

    if user_media['meta']['code'] == 200:
        if len(user_media['data']):
            image_name = user_media['data'][0]['id'] + '.jpeg'
            image_url = user_media['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(image_url, image_name)
            print 'Your image has been downloaded!'
        else:
            print 'Post does not exist!'
    else:
        print 'Status code other than 200 received!'



'''
 function declaration for the recent post liked by other user
'''

def get_post_like_by_friend(username):

    user_id = get_user_id(username)

    if user_id is None:
        print ' No such user'
        exit()
    request_url = BASE_URL + '/users/%s/media/recent/?access_token=%s' % (user_id, APP_ACCESS_TOKEN)

    print 'GET request url : %s' % request_url
    recent_media = requests.get(request_url).json()

    if recent_media['meta']['code'] == 200:
        if len(recent_media['data']):
            print 'Post id he/she liked recently' + recent_media['data'][0]['id']
        else:
            return None


'''
Function declaration to get the ID of the recent post of a user by username
'''


def get_post_id(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'User does not exist!'
        exit()
    request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_media = requests.get(request_url).json()

    if user_media['meta']['code'] == 200:
        if len(user_media['data']):
            return user_media['data'][0]['id']
        else:
            print 'There is no recent post of the user!'
            exit()
    else:
        print 'Status code other than 200 received!'
        exit()


'''
Function declaration to like the recent post of a user
'''


def like_a_post(insta_username):
    media_id = get_post_id(insta_username)
    request_url = (BASE_URL + 'media/%s/likes') % (media_id)
    payload = {"access_token": APP_ACCESS_TOKEN}
    print 'POST request url : %s' % (request_url)
    post_a_like = requests.post(request_url, payload).json()
    if post_a_like['meta']['code'] == 200:
        print 'Like was successful!'
    else:
        print 'Your like was unsuccessful. Try again!'


'''
Function declaration to make a comment on the recent post of the user
'''


def post_a_comment(insta_username):
    media_id = get_post_id(insta_username)
    comment_text = raw_input("Your comment: ")
    payload = {"access_token": APP_ACCESS_TOKEN, "text": comment_text}
    request_url = (BASE_URL + 'media/%s/comments') % (media_id)
    print 'POST request url : %s' % (request_url)

    make_comment = requests.post(request_url, payload).json()

    if make_comment['meta']['code'] == 200:
        print "Successfully added a new comment!"
    else:
        print "Unable to add comment. Try again!"


'''
Function declaration to get comment list of the user
'''


def get_comment_list(insta_username):
    media_id = get_post_id(insta_username)
    request_url = (BASE_URL + 'media/%s/comments?access_token=%s')%(media_id,APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    comment_list = requests.get(request_url).json()
    print "\nComments on post are : "
    for i in range(0,len(comment_list['data'])):
        print comment_list['data'][i]['from']['username']+" : "+comment_list['data'][i]['text']


    if comment_list['meta']['code'] == 200:
        print "\nThis were comments in the list!"
    else:
        print "Unable to show comment list. Try again!"


'''
Function declaration to get like list of the user
'''


def get_like_list(insta_username):
    media_id = get_post_id(insta_username)
    request_url = (BASE_URL + 'media/%s/likes?access_token=%s')%(media_id,APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    comment_list = requests.get(request_url).json()
    print "\nPeople who liked are : "
    for i in range(0,len(comment_list['data'])):
        print comment_list['data'][i]['username']


    if comment_list['meta']['code'] == 200:
        print "\nThese people liked the post!"
    else:
        print "Unable to show like list. Try again!"



'''
Function declaration to make delete negative comments from the recent post
'''


def delete_negative_comment(insta_username):
    media_id = get_post_id(insta_username)
    request_url = (BASE_URL + 'media/%s/comments/?access_token=%s') % (media_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    comment_info = requests.get(request_url).json()

    if comment_info['meta']['code'] == 200:
        if len(comment_info['data']):
            # Here's a naive implementation of how to delete the negative comments :)
            for x in range(0, len(comment_info['data'])):
                comment_id = comment_info['data'][x]['id']
                comment_text = comment_info['data'][x]['text']
                blob = TextBlob(comment_text, analyzer=NaiveBayesAnalyzer())
                if (blob.sentiment.p_neg > blob.sentiment.p_pos):
                    print 'Negative comment : %s' % (comment_text)
                    delete_url = (BASE_URL + 'media/%s/comments/%s/?access_token=%s') % (
                    media_id, comment_id, APP_ACCESS_TOKEN)
                    print 'DELETE request url : %s' % (delete_url)
                    delete_info = requests.delete(delete_url).json()

                    if delete_info['meta']['code'] == 200:
                        print 'Comment successfully deleted!\n'
                    else:
                        print 'Unable to delete comment!'
                else:
                    print 'Positive comment : %s\n' % (comment_text)
        else:
            print 'There are no existing comments on the post!'
    else:
        print 'Status code other than 200 received!'


'''
Function declaration to comment on targeted tagname
'''


def comment_on_caption(tag_name):

    comment_text = raw_input("Your comment: ")

    request_url = (BASE_URL + 'tags/%s/media/recent?&access_token=%s') % (tag_name, APP_ACCESS_TOKEN)
    tag_info = requests.get(request_url).json()
    payload = {"access_token": APP_ACCESS_TOKEN, "text": comment_text}

    if tag_info['meta']['code'] == 200:

        if len(tag_info['data']):
            for i in range(0,len(tag_info['data'])):
                request_url = (BASE_URL + 'media/%s/comments') % (tag_info['data'][i]['id'])
                print 'POST request url : %s' % (request_url)
                make_comment = requests.post(request_url, payload).json()
                if make_comment['meta']['code'] == 200:
                    print "Successfully added comment to all posts!"

                else:
                    print "Unable to add comment. Try again!"

        else:
            print 'sumthing went wrong'
            exit()

def start_bot():
    while True:
        print '\n'
        print '\n'
        print 'Hey! Welcome to instaBot!'
        print 'Here are your menu options:'
        print "a.Get your own details\n"
        print "b.Get details of a user by username\n"
        print "c.Get your own recent post\n"
        print "d.Get the recent post of a user by username\n"
        print "e.Get recent post liked by a user\n"
        print "f.Get recent post liked by other user by username\n"
        print "g.Get a list of people who have liked the recent post of user\n"
        print "h.Like the recent post of a user\n"
        print "i.Get a list of comments on the recent post of a user\n"
        print "j.Make a comment on the recent post of a user\n"
        print "k.Delete negative comments from the recent post of a user\n"
        print "l.Comment on all post of a target caption\n"
        print "m.Exit"

        choice = raw_input("Enter you choice: ")
        if choice == "a":
            self_info()
        elif choice == "b":
            insta_username = raw_input("Enter the username of the user: ")
            get_user_info(insta_username)
        elif choice == "c":
            get_own_post()
        elif choice == "d":
            insta_username = raw_input("Enter the username of the user: ")
            get_user_post(insta_username)
        elif choice == "e":
            get_post_liked_by_user()
        elif choice == "f":
            username = raw_input('Enter your friends name')
            get_post_like_by_friend(username)
        elif choice == "g":
            insta_username = raw_input("Enter the username of the user: ")
            get_like_list(insta_username)
        elif choice == "h":
            insta_username = raw_input("Enter the username of the user: ")
            like_a_post(insta_username)
        elif choice == "i":
            insta_username = raw_input("Enter the username of the user: ")
            get_comment_list(insta_username)
        elif choice == "j":
            insta_username = raw_input("Enter the username of the user: ")
            post_a_comment(insta_username)
        elif choice == "k":
            insta_username = raw_input("Enter the username of the user: ")
            delete_negative_comment(insta_username)
        elif choice == "l":
            tag_name = raw_input("Enter the tag name for targeted commenting : ")
            comment_on_caption(tag_name)
        elif choice == "m":
            exit()
        else:
            print "Please rnter valid choice "
            start_bot()


start_bot()


