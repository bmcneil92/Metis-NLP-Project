Brandon McNeil   
Metis Project 5 - NLP

## Context

Skin care is an incredibly daunting world to begin to navigate. With so many different types of products available, it is hard to 
narrow in on what will help your particular skin's needs.

This is something even rapper Cardi B struggles with! On January 25, 2021, Cardi B took to her Twitter following of over 
18 million users in search for product recommendations for her current skincare plight.

What if a newcomer to this industry could get the same feedback - without having to have to acquire 18 million twitter followers? 
Our goal is to try to build a recommondation system using the major skincare retail store - Sephora's - user reviews. 
We'll try to cluster topics found in the comments that can then recommend certain products based on what the end user is looking for in a skincare product.

With the global skin care products market size valued at 134.8 billion - it would benefit a skincare retail store to have this type of 
recommendation system available to new customers looking to enter the world of clear skin!

## Data

Our data was webscrapped off of Sephora's website using Selenium and stored in a MongoDB database. In total, we gathered 99,697 reviews across 
189 different products.

Before modeling, we decided to not include reviews that were 2 stars or below. The reason being is we did not want to output negative star 
reviews in our recommendation system.

After stemming and removing certain words, we ran our data through a countvectorizer before loading it into our model.

## Model 

Our final model was a NMF model tuned to seperate our data into 5 topics. Our final topics we reviews relating to 1) Makeup Removing, 2) Dry Skin, 3) General Cleansing, 4) Oily Skin, 5) Acne.

The model was pickled and placed into a Streamlit app that was able to accept user input and transform it via our NMF model. 
Using a noramlized version of our model's trained features, we were able to calculate the cosine similarities of our trained features and user inputted comments. 
We then were able to return the top 5 unique products based on the similar user's review.

![image](https://user-images.githubusercontent.com/43186680/119935783-0c563100-bf56-11eb-9654-88a1a04527ce.png)


 
## Tools
Altair for visualizations   
Pandas    
Numpy  
NMF  
PorterStemmer
MongoDB
Selenium
Streamlit
