"""
Generate similar items for products added to cart by the user.

"""
from surprise.dump import load
import pandas as pd
from backend.src.config import engine


def get_similar_items(item_name, n_similar_items=5):
    """
    Get Similar Items predicted by model.

    Parameters
    ----------
        item_name: name of the selected product.
        n_similar_items: number of similar products required, default=5.

    Returns
    -------
        Similar items list.
    """
    _, algo = load("backend/models/similar_items_algo.pkl")

    inner_item_mapping = pd.read_sql_table("item_id_mapping", engine, index_col="index")
    inner_id = inner_item_mapping[inner_item_mapping["item_raw_id"] == item_name]
    inner_id = int(inner_id["item_inner_id"])
    similar_item_ids = algo.get_neighbors(inner_id, k=n_similar_items)

    similar_items = [algo.trainset.to_raw_iid(ids) for ids in similar_item_ids]
    return similar_items
