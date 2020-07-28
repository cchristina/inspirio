# BITSPIRATION


This project started out with a simple prompt– make a spoof of an instagram inspiration quote, and I found myself faced with a problem: I'm not that funny on the fly. So, I decided to see if I could generate some funny text that was a plausible quote, and found myself a little bit carried away. This started as a simple jupyter notebook working a quote dataset I found on kaggle [source](https://www.kaggle.com/akmittal/quotes-dataset), to ultimately figuring out how to automate the image generation, too.


It works by starting out by checking off categories you want the quote to draw from. To save the tedium of checking everything off, leaving everything unchecked will automatically check everything. The categories are sent as a POST request to the `/make` endpoint  to work their magic. 

![app screenshot: image with several themes with a checkbox, with "Science", "Wisdom", and "Success" selected.](https://i.imgur.com/dDsc5mzm.png) ![flask debug screenshot: Post Variables for "Science", "Wisdom", and "Success"](https://i.imgur.com/Lj6vZNW.png)

The categories are the inputted into the markov chain to narrow down the set of quotes to pull from in order to make a new one and an author. 

![example output: "Success is stumbling from failure to seize opportunity."
– Jeanette Stein" over an image of fallen leaves on wood planking](https://i.imgur.com/L6Rqylo.png)

(this one appears to build off two quotes)
![jupyter notebook screenshot showing the rows with matching quotes](https://i.imgur.com/VNYwmUJ.png)
