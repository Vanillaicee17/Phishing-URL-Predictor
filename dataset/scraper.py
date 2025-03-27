import requests
from bs4 import BeautifulSoup
url = "https://phishtank.org/phish_detail.php?phish_id=8980612"

response = requests.get(url)



soup = BeautifulSoup(response.text, "html.parser")

print(soup)

h2_tag = soup.find("h2")


if h2_tag:
    h2_text = h2_tag.get_text(strip=True)
    print("Extracted Text:", h2_text)
else:
    print("H2 tag not found")