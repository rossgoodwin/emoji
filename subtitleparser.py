import nltk
from nltk.corpus import wordnet as wn
from sys import argv
import string

from emojiscraper import emojiDict

script, subfilepath = argv

# PICK APART EMOJIDICT...

emojiSyn = []
emojiName = []

for name, unicodeNum in emojiDict.iteritems():

	nameTokens = nltk.word_tokenize(name)

	for word in nameTokens:

		synonyms = []
		ss = wn.synsets(word.lower())
		for s in ss:
			synonyms+=s.lemma_names

		for i in range(len(synonyms)):
			synonyms[i] = string.replace(synonyms[i], '_', ' ')

		synonyms = set(synonyms)

		if bool(synonyms):
			emojiName.append(name)
			emojiSyn.append(synonyms)




# SUBTITLE FILE...

subfile = open(subfilepath, 'r')
# subtext = subfile.read()
# subfile.close()

textLines = []
for line in subfile:
	textLines.append(line)

# print textLines

lineCount = 1
trueTextLines = []
for i in range(len(textLines)):
	if textLines[i] == str(lineCount)+'\n':
		trueTextLines.append(textLines[i+2])
		lineCount+=1

# print trueTextLines

lineTokens = [nltk.word_tokenize(l) for l in trueTextLines]
lineEmoji = [[] for _ in trueTextLines]

lineCount = 0
for l in lineTokens:
	for word in l:

		synonyms = []
		ss = wn.synsets(word.lower())
		for s in ss:
			synonyms+=s.lemma_names

		for i in range(len(synonyms)):
			synonyms[i] = string.replace(synonyms[i], '_', ' ')

		synonyms = set(synonyms)

		for i in range(len(emojiName)):
			if bool(synonyms & emojiSyn[i]):
				lineEmoji[lineCount].append(emojiDict[emojiName[i]])

	lineCount+=1


trueLineEmoji = [[] for _ in lineEmoji]
lineCount = 0
for l in lineEmoji:

	for u in l:
		numba = u.split('+')[-1]
		try:
			emoji = unichr(int(numba, 16))
			trueLineEmoji[lineCount].append(emoji)
		except:
			pass

	lineCount+=1


# for l in trueLineEmoji:
# 	for w in l:
# 		print w
# 	print '\n'

_subfilepath = subfilepath.split('.srt')[0]

newsubfile = open(_subfilepath+'_emoji.srt', 'w')

print len(trueTextLines)
print len(trueLineEmoji)

lineCount = 0
for i in range(len(textLines)):
	if textLines[i][0] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
		newsubfile.write(textLines[i])
	elif lineCount < len(trueTextLines) and textLines[i] == trueTextLines[lineCount]:
		newsubfile.write(''.join(trueLineEmoji[lineCount]).encode('utf8')+'\n')
		newsubfile.write('\n')
		lineCount+=1

subfile.close()
newsubfile.close()






