# Response Analysis on Instagram

## Brief Description

Upload the json file of your chat/messages of you and your friend, and there will be an output of your the average reply time of you and your friend, as well as the average word count for each reply.

## Why do something crazy like this?

I decided to do something that isn't commonly seen. After browsing through Reddit forums on portfolio discussions it seems that everyone is tired of IMDB, Twitter, and COVID-19 related Data projects. 

I have drawn interests from data visualization such as [Tinder Insights](https://tinderinsights.com/) and [Instagram Insights](https://help.instagram.com/1533933820244654). Additionally, this is an entry project on text analytics for me as I would like to explore (or replicate) [Instagram's text analytics for product suggestion](https://www.forbes.com/sites/zakdoffman/2020/08/16/why-you-should-not-use-facebooks-new-instagram-messenger-whatsapp-iphone-android-security-warning/).

**I would like to emphasis the fact that this is of personal use and you are ethically and morally responsible for the use of this code. I have only tested this code with one of my friends after recieving their consent.**

## Output

There will be a box series plot based on what you choose. I have only created the average response time option as of now (will create the average word count later). 

Boxplot will look like (Click image to zoom in):

<img src="Report.png"  width = "4000">

## Important Note

Amongst the code you will see this

```
try:
    newlist = [i / milli_2_min for i in temp_list]
    if (statistics.mean(newlist) >= 400): #can be changed to adjust the plotted image so that outliers dont mess things up
        newlist = "remove"
        # pass
except TypeError:
    newlist = [0]
```

```
if (statistics.mean(newlist) >= 400):
```

this is added so that any outliers wouldn't mess the whole boxplot by making the y-axis range too large. You may remove this to see any differences and adjust according to your preferences.
