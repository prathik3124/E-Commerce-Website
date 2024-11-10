Using the customer orders and rating data from Olist E-Commerce Public Dataset, which has information about 100k orders made at multiple marketplaces in Brazil from 2016 to 2018, I trained 3 models that generate product recommendations.

*NOTE* 

*- The granularity of orders in the dataset is at product category level, thus recommendations are product categories in the true sense.*

*- The application is deployed on a free server that goes into sleep mode, expect a ~10 seconds delay in loading, If it takes more than 10 seconds, try refreshing! :)*

## Architecture

The website is divided into 3 sections.
### 1. Top Trending
**Demographic Filtering** - Recommends highest rated products in the dataset.

**Method** - Uses [IMDB weighted average formula](https://help.imdb.com/article/imdb/track-movies-tv/ratings-faq/G67Y87TFYYP6TWAV#calculatetop) and recommends highest rated products.

### 2. Similar Products
**Item based collaborative filtering** - Takes user input of one product and recommends 5 similar products.
      
**Method** - Computes cosine similarity between selected product and others based on historical ratings given by customers using KNN Basic algorithm.

### 3. Products you might like
**User based collaborative filtering** - Takes user input & rating of one product and recommends 3 products based on the rating given for the selected product.
      
**Method** -   Approximates the user's taste by running two algorithms in the backend, first computes the most similar user who has sufficient historical data, and second, makes recommendations based on their taste.


## Setup Instructions

This repo is currently in a development state, I'm working on setting up an easy method to run this application on local machines, will update this section soon. 