"""
Process Top Trending .json file.

"""


def get_top_ten_trending():
    """
    Process top ten trending.

    Returns
    -------
        .json file.
    """

    top_ten = {
        "0": ["health_beauty", 9038, 3.70],
        "1": ["sports_leisure", 7872, 3.60],
        "2": ["bed_bath_table", 10223, 3.58],
        "3": ["computers_accessories", 6913, 3.42],
        "4": ["furniture_decor", 6812, 3.39],
        "5": ["housewares", 6025, 3.38],
        "6": ["watches_gifts", 5805, 3.31],
        "7": ["toys", 3982, 3.02],
        "8": ["telephony", 4287, 3.00],
        "9": ["auto", 3997, 2.97]
    }
    return top_ten
