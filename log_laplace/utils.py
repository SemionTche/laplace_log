import json

def json_style(d: dict) -> str:
    '''Return a pretty-printed JSON string of a dictionary for logging.'''
    try:
        return json.dumps(d, indent=4, sort_keys=True, default=str)
    except Exception as e:
        return str(d)  # fallback if object is not JSON serializable