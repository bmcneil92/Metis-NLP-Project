import streamlit as st
import pandas as pd
import altair as alt
import pickle
from sklearn.feature_extraction.text import CountVectorizer
import string
import re
from sklearn.metrics.pairwise import cosine_similarity
from nltk.tokenize import word_tokenize
from sklearn.decomposition import NMF
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
import numpy as np
import collections


review_df = pickle.load(open('review_dataframe.pkl', 'rb'))
product_df = pickle.load(open('product_dataframe.pkl', 'rb'))
df_nmf_feautres = pickle.load(open('df_nmf_features.pkl', 'rb'))
cv1 = pickle.load(open('countvector.pkl', 'rb'))
topic_model = pickle.load(open('finalized_nmf_model.pkl','rb'))
stopwords = stopwords.words('english')
ps = PorterStemmer()
blocker_words = ['skin', 'would', 'cleanser', 'around', 'say', 'month', 'day', 'product', 'time', 'week',
                'use', 'ive', 'get', 'first', 'start', 'night', 'year', 'sinc', 'everi', 'balm', 'receiv', 'free',
                'size', 'test', 'think', 'still', 'like', 'yet', 'cleanser', 'price', 'everyth', 'influenst', 
                 'sampl', 'thing', 'stuff', 'littl', 'almost', 'thought', 'long', 'amount', 'one', 'cloth', 
                'sephora', 'morn', 'afterward', 'im', 'go', 'also', 'stuff', 'second', 'took', 'cloth', 
                 'cotton', 'way', 'face', 'feel', 'love', 'realli', 'tri', 'smell', 'great', 'make', 'well'
                , 'good', 'take', 'definit', 'amaz', 'super', 'best', 'got', 'never', 'buy', 'bit', 'lot', 'job'
                'want', 'goe', 'review', 'last', 'enough', 'actual', 'sure', 'though', 'usual', 'back', 'seem', 
                'far', 'anyth', 'howev', 'bought', 'routin', 'perfect', 'see', 'someth', 'come', 'away', 
                'give', 'dont', 'much', 'even', 'find', 'rins', 'star', 'small', 'know', '2', 'skincar', 'noth'
                'right', 'cant', 'two', 'part', 'done', 'came', 'brush', 'wasnt', 'twice', 'pump', 'squeaki',  
                'honestli', 'old', 'top', 'prior', 'write', 'wipe', 'nervou', 'eye', 'eyes', 'green', 'blue',
                'hazel', 'brown', 'hair', 'not', 'list', 'listed', 'brunett', 'blond', 'chin', 'real', 'bottl', 
                 'doesnt', 'open', 'auburn', 'aubur', 'gray', 'grey', 'black', 'red', 'other', 'forward', 'nice'
                ,'ok']


def clean_text(txt):
    txt = "".join([c.lower() for c in txt if c not in string.punctuation])
    tokens = re.split('\W+', txt)
    txt = " ".join([ps.stem(word) for word in tokens if word not in stopwords and ps.stem(word) not in blocker_words])
    return txt

def user_input_modeling(user_input):
	list_input = [str(user_input)]
	cleaned_user_input = clean_text(list_input)
	cv_input = cv1.transform([cleaned_user_input])
	input_model = topic_model.transform(cv_input)
	df_user_input = pd.DataFrame(input_model)
	user_matrix = df_user_input.loc[0, :]
	return user_matrix

st.set_page_config(page_title = 'Sephora Face Cleanser Recommendation', layout='wide')

st.image('https://i.pinimg.com/originals/ab/53/70/ab5370ea658a44052f1a7f264e43bbdb.jpg', width=150)
st.title('Sephora Face Cleanser Recommendation')


def main():

	user_input = st.text_input("Enter Skin Concerns")

	if st.button("Search"):

		user_topic = user_input_modeling(user_input)

		similarities = df_nmf_feautres.dot(user_topic)

		sim_dict = similarities.nlargest(50).to_dict()

		
		# Loop Through dictionary of 50 similiar products 
		# to create another dictionary of product IDs.

		top_matches_dict = collections.defaultdict(list)
		for k in sim_dict.keys():
			if int(review_df.iloc[k]['review_rating_cleaned']) > 3:
				top_matches_dict[k] = review_df.iloc[k]['product']
			else:
				continue


		# Get unique product ids from the top_matches_dict


		top_matches_list = set( val for dic in top_matches_dict for val in top_matches_dict.values())

		
		product_display_dict = collections.defaultdict(list)
		for i, k in enumerate(top_matches_list):
			if len(product_display_dict) != 5:
				product_display_dict[i].append(product_df[product_df['_id'] == k]['product_url'].item())
				product_display_dict[i].append(product_df[product_df['_id'] == k]['brand_name'].item())
				product_display_dict[i].append(product_df[product_df['_id'] == k]['product_name'].item())
				product_display_dict[i].append(product_df[product_df['_id'] == k]['price'].item())
				product_display_dict[i].append(product_df[product_df['_id'] == k]['product_img_url'].item())
				product_display_dict[i].append(product_df[product_df['_id'] == k]['review_rating_cleaned'].item())
			else:
				break

		

		if len(product_display_dict) >= 1:
			col1_1, col1_2, col1_3 = st.beta_columns([1, 3, 2])
			
			with col1_2:
				st.markdown(f'**_{product_display_dict[0][1]}_** - [{product_display_dict[0][2]}] ({product_display_dict[0][0]})', unsafe_allow_html=True)
				st.text(f'Price: ${product_display_dict[0][3]}0')
				st.text(f'Rating: {product_display_dict[0][5]}')
			
			with col1_3:
				st.image(f"https://www.sephora.com{product_display_dict[0][4]}", width=150)


		if len(product_display_dict)>=2:
			col2_1, col2_2, col2_3 = st.beta_columns([1 ,3, 2])
			
			with col2_2:
				st.markdown(f'**_{product_display_dict[1][1]}_** - [{product_display_dict[1][2]}] ({product_display_dict[1][0]})', unsafe_allow_html=True)
				st.text(f'Price: ${product_display_dict[1][3]}0')
				st.text(f'Rating: {product_display_dict[1][5]}')
			
			with col2_3:
				st.image(f"https://www.sephora.com{product_display_dict[1][4]}", width=150)
		
		if len(product_display_dict) >= 3:
			col3_1, col3_2, col3_3 = st.beta_columns([1, 3, 2])
			
			with col3_2:
				st.markdown(f'**_{product_display_dict[2][1]}_** - [{product_display_dict[2][2]}] ({product_display_dict[2][0]})', unsafe_allow_html=True)
				st.text(f'Price: ${product_display_dict[2][3]}0')
				st.text(f'Rating: {product_display_dict[2][5]}')
			
			with col3_3:
				st.image(f"https://www.sephora.com{product_display_dict[2][4]}", width=150)
		
		if len(product_display_dict) >= 4:
			col4_1, col4_2, col4_3 = st.beta_columns([1, 3, 2])
			
			with col4_2:
				st.markdown(f'**_{product_display_dict[3][1]}_** - [{product_display_dict[3][2]}] ({product_display_dict[3][0]})', unsafe_allow_html=True)
				st.text(f'Price: ${product_display_dict[3][3]}0')
				st.text(f'Rating: {product_display_dict[3][5]}')
			
			with col4_3:
				st.image(f"https://www.sephora.com{product_display_dict[3][4]}", width=150)
		
		if len(product_display_dict) >= 5:
			col5_1, col5_2 , col5_3= st.beta_columns([1, 3, 2])
			
			with col5_2:
				st.markdown(f'**_{product_display_dict[4][1]}_** - [{product_display_dict[4][2]}] ({product_display_dict[4][0]})', unsafe_allow_html=True)
				st.text(f'Price: ${product_display_dict[4][3]}0')
				st.text(f'Rating: {product_display_dict[4][5]}')
			
			with col5_3:
				st.image(f"https://www.sephora.com{product_display_dict[4][4]}", width=150)



if __name__=='__main__':
    main()


