import requests

#function to fetch news api data, same function used in assignment 2
def getnewsapi():
	list_of_words = ["Canada","Halifax","Dalhousie University","Canada Education","University"]
	file_counter = 0
	for jk in list_of_words:
		print(jk)
		url = ('https://newsapi.org/v2/everything?'
		       'q='+jk+'&'
		       'pageSize=100&'
		       'apiKey=e1b82350fddc453b8b4fda0facd370f2')
		response = requests.get(url)
		aa = response.json()
		cc = 0
		print(len(aa['articles']))
		for i,j in enumerate(aa['articles']):
			cc += 1
			file_counter += 1
			file = open('new_files2/news_collection'+str(file_counter)+'.txt','a+')
			if j['description'] is not None:
				final_text = ''.join((char if char is ' ' or char.isalnum() else ' ') for char in j['description'])
				final_text = final_text.encode('ascii', 'ignore').decode('ascii')
				final_tweet = final_text.split("https",1)[0]
				file.write("Description:"+final_text+"\n")
			if j['title'] is not None:
				file.write("Title:"+j['title']+"\n")
			if j['content'] is not None:
				file.write("Content"+j['content']+"\n")
			file.close()
getnewsapi()