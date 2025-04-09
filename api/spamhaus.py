import httpx


URL = "https://www.spamhaus.org/api/v1/sia-proxy/api/intel/v2/byobject/domain"

async def get_data(search):
    url = f"{URL}/{search}/overview"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()
        data = response.json()

        spamhaus = {
            "score" : data["score"],
            "human" : data["dimensions"]["human"],
            "identity" : data["dimensions"]["identity"],
            "infra" : data["dimensions"]["infra"],
            "malware" : data["dimensions"]["malware"],
            "smtp" : data["dimensions"]["smtp"]
        }
        return spamhaus
