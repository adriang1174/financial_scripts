import requests
requests.post('https://api.mynotifier.app', {
    "apiKey": os.environ['MYNOTIFIER_API_KEY'],
    "message": "Our first notification!",
    "description": "This is cool",
    "type": "info", # info, error, warning or success
})