import requests

def check_traffic(domain):
    url = "https://similar-web.p.rapidapi.com/get-analysis"
    querystring = {"domain": domain}


    headers = {
    "x-rapidapi-key": "2d19db5775msh5e1d78bd4ead909p14a14bjsn35fb153292ce",
    "x-rapidapi-host": "similar-web.p.rapidapi.com"
    }

    response = requests.get(url, headers = headers, params = querystring)
    data = response.json()

    monthly_visits = data["Engagments"]["Visits"]
    
    return monthly_visits
