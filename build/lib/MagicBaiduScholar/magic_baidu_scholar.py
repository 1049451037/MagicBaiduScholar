import os
import random
import time

import cchardet
import requests

from bs4 import BeautifulSoup
from MagicBaiduScholar.config import USER_AGENT


class MagicBaiduScholar():
	"""
	Magic Baidu Scholar search.
	"""

	def __init__(self):
		pass

	def search(self, query, start=0, pause=2):
		"""
		Get the results you want,such as title,description,url
		:param query:
		:param start:
		:return: Generator
		"""
		start = start // 10 * 10
		content = self.search_page(query, start, pause)
		soup = BeautifulSoup(content, "html.parser")
		for item in soup.find_all(name='div', attrs={"class": "result sc_default_result xpath-log"}):
			'''
			Adapted from https://github.com/renfanzi/Crawling_Baidu_Academic
			'''
			sub_article = item

			# -----<学术标题>----- #
			academic_title = "".join(
				list(sub_article.find(name='a', attrs={"data-click": "{'button_tp':'title'}"}).stripped_strings))

			# -----<学术主要内容>----- #
			academic_contents = sub_article.find(name='div', attrs={"class": "c_abstract"}).stripped_strings
			academic_content = ''.join(list(academic_contents))
			academic_content = academic_content[:academic_content.rfind('...')+3]

			# -----<学术链接>----- #
			academic_href = sub_article.find(name='a', attrs={"data-click": "{'button_tp':'title'}"}).get("href")


			# -----<论文来源： 知网啊， 等>----- #
			source_articles = sub_article.find(name="div", attrs={"class": "sc_allversion"})
			source_articles_li = []
			if source_articles:

				source_articles_span = source_articles.findAll(name="span", attrs={"class": "v_item_span"})
				# print(s1)
				for i in range(len(source_articles_span)):
					# 如果不是【】， 证明这个是免费的
					sub_source_articles_dict = {}
					source_articles_i = source_articles_span[i].findAll(name="i",
																		attrs={"class": "c-icon c-icon-free v_freeicon"})
					if source_articles_i:
						# 证明是免费的
						sub_source_articles_dict["free"] = 1
					else:
						sub_source_articles_dict["free"] = 0

					source_articles_a = source_articles_span[i].find(name="a", attrs={"class": "v_source"})
					sub_source_articles_dict["name"] = source_articles_a.get("title")
					sub_source_articles_dict["url"] = source_articles_a.get("href").strip()

					source_articles_li.append(sub_source_articles_dict)

			# -----<作者>----- #
			academic_author = [i.string for i in
							   sub_article.findAll(name='a', attrs={"data-click": "{'button_tp':'author'}"})]

			# -----<作者连接>----- #
			academic_author_href = [i.get("href").strip() for i in
									sub_article.findAll(name='a', attrs={"data-click": "{'button_tp':'author'}"})]

			if sub_article.find(name='a', attrs={"data-click": "{'button_tp':'sc_cited'}"}):
				# -----<被引量>----- #
				academic_count = sub_article.find(name='a', attrs={"data-click": "{'button_tp':'sc_cited'}"}).string.strip()

				# -----<被引用文章链接>----- #
				academic_count_href = sub_article.find(name='a', attrs={"data-click": "{'button_tp':'sc_cited'}"}).get(
					"href").strip()
			else:
				academic_count = 0
				academic_count_href = ''

			# -----<标签>----- #
			academic_label = [i.string for i in
							  sub_article.findAll(name='a', attrs={"data-click": "{'button_tp':'sc_search'}"})]

			sub_data = {}
			sub_data["title"] = academic_title
			sub_data["content"] = academic_content
			sub_data["href"] = academic_href
			sub_data["author"] = academic_author
			sub_data["author_href"] = academic_author_href
			sub_data["count"] = academic_count
			sub_data["count_href"] = academic_count_href
			sub_data["label"] = academic_label
			sub_data["article_source"] = source_articles_li
			yield sub_data

	def search_page(self, query, start=0, pause=2):
		"""
		Baidu search
		:param query: Keyword
		:param language: Language
		:return: result
		"""
		start = start // 10 * 10
		time.sleep(pause)
		param = { 'wd' : query , 'pn': str(start)}
		url = 'http://xueshu.baidu.com/s'
		# Add headers
		headers = { 'User-Agent': self.get_random_user_agent(), 
					'Host': 'xueshu.baidu.com',
					'Referer': 'http://xueshu.baidu.com'
					}
		try:
			requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)
			r = requests.get(url=url,
							 params=param,
							 headers=headers,
							 allow_redirects=False,
							 verify=False,
							 timeout=10)
			content = r.content
			charset = cchardet.detect(content)
			text = content.decode(charset['encoding'])
			return text
		except:
			return None

	def pq_html(self, content):
		"""
		Parsing HTML by pyquery
		:param content: HTML content
		:return:
		"""
		return pq(content)

	def get_random_user_agent(self):
		"""
		Get a random user agent string.
		:return: Random user agent string.
		"""
		return random.choice(self.get_data('user_agents.txt', USER_AGENT))

	def get_data(self, filename, default=''):
		"""
		Get data from a file
		:param filename: filename
		:param default: default value
		:return: data
		"""
		root_folder = os.path.dirname(__file__)
		user_agents_file = os.path.join(
			os.path.join(root_folder, 'data'), filename)
		try:
			with open(user_agents_file) as fp:
				data = [_.strip() for _ in fp.readlines()]
		except:
			data = [default]
		return data
		