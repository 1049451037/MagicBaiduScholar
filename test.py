from MagicBaiduScholar import MagicBaiduScholar
import pprint

mbs = MagicBaiduScholar()

for i in mbs.search(query='机器学习'):
	try:
		pprint.pprint(i)
	except:
		pass
		