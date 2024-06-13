import ncaadb


def read_save():
    with open("data/USR-DATA", "rb") as f:
        data = ncaadb.read_db(f)
    return data
