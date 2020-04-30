from bson import ObjectId
import pandas as pd

# Utility functions

def get_df(loc):
    # Extract and clean up data to not have leading or trailing spaces
    df  = pd.read_csv(loc, encoding="ISO-8859-1",dtype='object')
    df.columns = df.columns.str.strip()
    df_cols = df.columns

    # ensure all strings have no trailing space
    #for i, v in enumerate(df.dtypes):
    #    if v == object:
    #        df[df_cols[i]] = df[df_cols[i]].apply(lambda x: x.strip() if isinstance(x, str) else x)
    return df


def query_db(db, entity_type, entity_id):
    if (ObjectId.is_valid(entity_id)):
        return db[entity_type].find_one({'_id': ObjectId(entity_id)})
    else:
        return db[entity_type].find_one({'name': entity_id})


def update_db(db, entity_type, entity_id, updated_vals):
    if (ObjectId.is_valid(entity_id)):
        db[entity_type].update_one({'_id': ObjectId(entity_id)}, {'$set': updated_vals})
    else:
        db[entity_type].update_one({'name': entity_id}, {'$set': updated_vals})