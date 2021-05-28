# NLP Project

### Sephora Skincare Recommendations

For this project, we will set out to explore user reviews on the Sephora website for face cleansers.

### Question/need:

Skin care is an incredibly daunting world to begin to navigate. With so many different types of products available, it is hard to narrow in on what will help your 
particular skin's needs.

This is something even rapper Cardi B struggles with! On January 25, 2021, Cardi B took to her Twitter following of over 18 million users in search for 
product recommendations for her current skincare plight.


<img src="https://user-images.githubusercontent.com/43186680/118877333-54bd8100-b8bc-11eb-9978-962d1f1d6aee.png" width="500">


What if a newcomer to this industry could get the same feedback - without having to have to acquire 18 million twitter followers? Our goal is to try to build a recommondation 
system using the major skincare retail store - Sephora's - user reviews. We'll try to cluster topics found in the comments that can then recommend certain products based on 
what the end user is looking for in a skincare product.

With the global skin care products market size valued at 134.8 billion - it would benefit a skincare retail store to have this type of recommendation 
system available to new customers looking to enter the world of clear skin!


### Data Description:

Our data will be webscrapped from the Sephora website and placed into a proprietary database. 

Each row of data will contain the text from the comment and their ranking of the product.

### Tools:

SQL Lite/MongoDB - for data storage  
Python - for data processing/modeling  
Flask - for potential Web Application to display model  


### MVP:

An MVP for this project will consist of a simple topic model that can provide insight into the types of clusters gathered from the comments we webscrapped.
