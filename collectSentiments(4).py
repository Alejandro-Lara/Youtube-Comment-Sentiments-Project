from textblob import TextBlob
import re

commentsFile=open('commentsAndTime.txt','r')
sentimentsFile=open('sentimentsAndTime.txt', 'w')
fileLines=commentsFile.readlines()
timeFormat = re.compile('\d\d:\d\d:\d\d')
print(len(fileLines))
discardCount=0

for line in fileLines:
    twoParts = line.split('--')
    #print(twoParts)
    if len(twoParts) == 2 and timeFormat.match(twoParts[1]):       
        blob=TextBlob(twoParts[0])
        sentimentsFile.write(str(blob.sentiment.polarity)+" "+twoParts[1])
    else:
        discardCount+=1

print(discardCount)
commentsFile.close()
sentimentsFile.close()
