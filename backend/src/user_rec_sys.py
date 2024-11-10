"""
Online Learning ML module for computing recommendation based on user rating given.
"""
import pandas as pd
import numpy as np
import random
from surprise import KNNWithMeans
from surprise import Dataset, Reader
from surprise import dump

# Local Imports.
from backend.src.config import engine


# Step 1: Add New User to dataset.
def _add_new_user(user_rec_sys_data, product_category, review_score):
    """
    Adds new user rating to the user_rec_sys_data.

    Parameters
    ----------
        user_rec_sys_data: Reviews data for adding new user.
        product_category: Product Selected on the website.
        review_score: Rating given for the item.

    Yields
    ------
        Updates user_rec_sys_data.csv

    Returns
    -------
        updated_data, new_user_id.
    """

    # Computing new_user_id.
    new_user_raw_id = user_rec_sys_data["customer_id"].max() + 1
    new_data = {"customer_id": new_user_raw_id,
                "product_category": product_category,
                "review_score": review_score}

    updated_data = user_rec_sys_data.append(new_data, ignore_index=True)
    return updated_data, new_user_raw_id


# Step 2: Online Similar User Model.
def _online_similar_user_model(product_category, review_score):
    """
    Trains KNNBasic algorithm to find similar users.

    Parameters
    ----------
        product_category: str.
        review_score: int.

    Returns
    -------
        trainset, new_user_raw_id, new_user_neighbor_raw_id
    """

    user_rec_sys_data = pd.read_sql_table("user_rec_sys", engine, index_col="index")

    updated_data, new_user_raw_id = _add_new_user(user_rec_sys_data, product_category, review_score)
    review_score_values = list(updated_data["review_score"].value_counts().index)

    # Defining Data Object.
    reader = Reader(rating_scale=(min(review_score_values), max(review_score_values)))
    data = Dataset.load_from_df(updated_data, reader)
    trainset = data.build_full_trainset()

    # Training.
    random.seed(0)
    np.random.seed(0)

    sim_options = {
        "name": "msd",
        "user_based": True
    }

    algo = KNNWithMeans(sim_options=sim_options, verbose=False)
    algo.fit(trainset)

    # Find Similar User.
    new_user_inner_id = trainset.to_inner_uid(new_user_raw_id)
    new_user_neighbor_inner_id = algo.get_neighbors(new_user_inner_id, k=1)
    new_user_neighbor_raw_id = new_user_neighbor_inner_id[0]
    return trainset, new_user_raw_id, new_user_neighbor_raw_id


# Step 3: Compute Recommendations.
def _compute_recommendations(trainset, new_user_neighbor_raw_id, n_recommendations=3):
    """
    Compute Top 5 Product Recommendations.

    Parameters
    ----------
        trainset: data object.
        new_user_neighbor_raw_id: str, Inner Id for the nearest neighbor.
        n_recommendations: int, Number of recommendations.

    Returns
    -------
        top 5 recommendations.
    """
    _, algo = dump.load("backend/models/user_predictions_algo.pkl")
    item_id_mapping = pd.read_sql_table("item_id_mapping", engine, index_col="index")

    predictions = {}
    for items in list(item_id_mapping["item_raw_id"]):
        x = algo.predict(items, new_user_neighbor_raw_id)
        predictions[x[0]] = x[3]

    predictions = pd.DataFrame(predictions.values(), predictions.keys())
    top_five_recommends = list(predictions.sort_values(0, ascending=False).head(n_recommendations).index)
    return top_five_recommends


def get_top_n_recommendations(product_category, review_score, n_recommendations=3):
    """
    Generate Top Recommendation for user inputs.

    Parameters
    ----------
        product_category: str.
        review_score: int, Rating given.
        n_recommendations: int, Number of recommendations.

    Returns
    -------
        Top n-recommendations list.
    """
    # Find similar user.
    trainset, new_user_raw_id, new_user_neighbor_raw_id = _online_similar_user_model(product_category, review_score)

    # Generate prediction for nearest neighbor.
    top_recommendations = _compute_recommendations(trainset, new_user_neighbor_raw_id, n_recommendations)

    return top_recommendations
