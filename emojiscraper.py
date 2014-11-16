from bs4 import BeautifulSoup

filepath = 'php-emoji-master/table.htm'

f = open(filepath, 'r')
text = f.read()
f.close()

soup = BeautifulSoup(text)

trs = soup.find_all('tr')

emojiList = []
unicodeList = []

for tr in trs[1:]:
	tds = tr.find_all('td')
	i = 0
	for td in tds:
		if i == 1:
			emojiList.append(td.string)
		elif i == 2:
			unicodeList.append(td.string)
		i+=1


emojiDict = dict(zip(emojiList, unicodeList))

# print emojiDict