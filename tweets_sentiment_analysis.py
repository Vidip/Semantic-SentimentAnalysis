import tweepy
import requests
import xlwt
from xlwt import Workbook

#function to get tweets
def gettwittersearch():
	all_the_tweets = []
	date_since = "2019-10-01"
	author_name = ''
	for j in list_of_words:
		search_words = j
		tweets = tweepy.Cursor(api.search,q=search_words ,lang="en",since=date_since,tweet_mode="extended").items(700)
		counter = 0
		for i in tweets:
			counter +=1
			if len(i.entities['user_mentions']) >0:
				author_name = i.entities['user_mentions'][0]['name']
			final_tweet = ''.join((char if char is ' ' or char.isalnum() else ' ') for char in i.full_text)
			final_tweet = final_tweet.encode('ascii', 'ignore').decode('ascii')
			final_tweet = final_tweet.split("https",1)[0]
			new_list.append(final_tweet)
	analyse_tweets(new_list)

#function to analyse tweets, split them and store them as key in dictionary
def analyse_tweets(new_list):
	final_list = []
	new_val = 0
	for i in new_list:
		new_dict = {}
		split_list = i.split(" ")
		for j in split_list:
			count = 0
			if j != '':
				if j not in new_dict.keys() and j is not None:
					count += 1
					new_dict[j] = count
				else:
					new_val = new_dict[j] + 1
					new_dict[j] = new_val
		final_list.append(new_dict)
	compare_tweets(final_list,new_list)

#comparing positive and negative words
def compare_tweets(final_list,new_list):
	print(final_list)
	positive = 0
	negative = 0
	status = ''
	match = ''
	status_dict = dict()
	all_results = []
	#opening a workbook
	wb = Workbook()
	sheet1 = wb.add_sheet('Sheet 1')
	sheet1.write(0,0, "tweet") 
	sheet1.write(0,1, "message") 
	sheet1.write(0,2, "match") 
	sheet1.write(0,3, "polarity")
	#comparing words with files having positive and negative words
	with open('positive_words.txt') as file, open('negative_words.txt') as file2:
		contents = file.read()
		contents2 = file2.read()
		counter = 0
		for i in range(len(final_list)):
			for key,value in final_list[i].items():
				if key in contents.split('\n'):
					positive += 1
					match = key
				elif key in contents2.split('\n'):
					negative += 1
					match2 = key
			status_dict['tweet'] = i
			status_dict['message'] = new_list[i]
			if positive > negative:
				polarity = 'positive'
			elif negative > positive:
				polarity = 'negative'
				match = match2
			else:
				polarity = "neutral"
			counter += 1
			status_dict['match'] = match
			status_dict['polarity'] = polarity
			all_results.append(status_dict)
			status_dict = {}
			sheet1.write(counter,0, i) 
			sheet1.write(counter,1, new_list[i]) 
			sheet1.write(counter,2, match) 
			sheet1.write(counter,3, polarity)
			wb.save('data_tweets.xls')
			positive = 0
			negative = 0
		print(all_results)



if __name__ == "__main__":
	new_list = []
	new_dict = {}
	list_of_words = ["Canada","Halifax","Dalhousie University","Canada Education","University"]
	auth = tweepy.OAuthHandler("XPkBPaq3xkgqRmlA7qLJbB4Ys","pAeuGBrNi6TFWxthwmEaKu3myto68iVBAimkFn1hCokDANbpyN")
	auth.set_access_token("703534714817159168-DITofzt94rgeMbgycWjMirc9o1NcxvV","67kMQ7dz3t2kSdf3dQyK457pcof9mIzj573y0YhaP193j")
	api = tweepy.API(auth,wait_on_rate_limit=True)
	gettwittersearch()