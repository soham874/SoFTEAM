import json

def jsonify_df_object(df_object):
    return json.loads(df_object.to_json(orient='records', date_format='iso').replace('\\"', '"'))