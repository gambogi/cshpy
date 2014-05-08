import requests
import json

class Webnews:
	def __init__(self, api_key, api_agent='A script using webnews.py'):
		self.payload = {'api_key'   : api_key
		          , 'api_agent' : api_agent
		          }
		self.headers = {'Accept' : 'application/json'}
		self.prefix = 'https://webnews.csh.rit.edu/'
	
	def get(self, target, params={}):
		url = self.prefix + target
		payload = dict(self.payload.items() + params.items())
		return requests.get(url, params = payload, headers=self.headers, verify=False)

	def post(self, target, params={}):
		url = self.prefix + target
		payload = dict(self.payload.items() + params.items())
		return requests.post(url, params = payload, headers=self.headers, verify=False)

	def put(self, target, params={}):
		url = self.prefix + target
		payload = dict(self.payload.items() + params.items())
		return requests.put(url, params = payload, headers=self.headers, verify=False)

	def delete(self, target, params={}):
		url = self.prefix + target
		payload = dict(self.payload.items() + params.items())
		return requests.delete(url, params = payload, headers=self.headers, verify=False)
	
	def newsgroups(self):
		url = self.prefix + 'newsgroups'
		r = requests.get(url,params = payload, headers=self.headers, verify=False)
		deserialized = json.loads(r.text)
		return self.get('newsgroups')

	def newsgroup_names(self):
		names = []
		groupDicts = self.newsgroups()[u'newsgroups']
		for groupDict in groupDicts:
			name = groupDict[u'name']
			names.append(name)
		return names

	def search(self, more=True, **kwargs):
		while more:
			r = json.loads(self.get('search', params=kwargs).content)
			posts = r['posts_older']
			more = r['more_older']
			if more:
				kwargs['from_older'] = posts[-1]['post']['date']
			yield posts

	def user(self):
		return json.loads(self.get('user').content)['user']

	def newspost(self, newsgroup, num):
		r = self.get(newsgroup+'/'+str(num), {'html_body':True})
		return json.loads(r.content)['post']
	def get_unread_counts(self):
		return json.loads(self.get('unread_counts').content)['unread_counts']

	def get_newsgroup_index(self, newsgroup):
		return json.loads(self.get(newsgroup+'/index', {'newsgroup':newsgroup}).content)

	def get_last_date(self, posts):
		return posts[-1][u'post'][u'date']

	def compose(self, newsgroup, subject, **kwargs):
		kwargs['newsgroup'] = newsgroup
		kwargs['subject'] = subject
		self.post('compose', params = kwargs)

	def mark_read(self, **kwargs):
		self.put('mark_read', kwargs)

	def stick(self, newsgroup, number, time):
		self.put(newsgroup+'/'+number+'/sticky', {'sticky_until':time})

	def unstick(self, newsgroup, number):
		self.put(newsgroup+'/'+number+'/sticky', {'unstick':True})
	
	def star(self, newsgroup, number):
		self.put(newsgroup+'/'+number+'/star')
	
	def delete_post(self, newsgroup, number, reason='I do what I want'):
		params = { 'reason' : reason 
				 , 'confirm_cancel' : True
				 , 'posting_host' : 'wannamaker'
				 }
		self.delete(newsgroup+'/'+str(number), params)

	def activity(self):
		a = self.get('activity')
		return json.loads(a.content)['activity']

