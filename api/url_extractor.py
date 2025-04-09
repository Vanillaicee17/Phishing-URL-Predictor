import ssl
import socket
from datetime import datetime, timezone
from urllib.parse import urlparse
from dateutil.relativedelta import relativedelta
from ssl_checker import check_ssl_issuer
from web_traffic import check_traffic
from subdomain import analyze_subdomain
from URL_of_anchor import extract_url_of_anchor
from request_urls import classify_url
from spamhaus import get_data
import asyncio



def extractor(url):
    features = {
        'Prefix_Suffix': 1,
        'having_Sub_Domain': 1,
        'SSLfinal_State': 1,
        'Request_URL': 1,
        'web_traffic': 1,
        "score" : 0,
        "human" : 0,
        "identity" : 0,
        "infra" : 0,
        "malware" : 0,
        "smtp" : 0
    }

    try:
        # Parse URL components
        parsed = urlparse(url if '://' in url else f'https://{url}')
        domain = parsed.netloc.split(':')[0]

        # 1. Prefix/Suffix check
        features['Prefix_Suffix'] = 1 if '-' in domain else -1

        # 2. Subdomain count
        
        features['having_Sub_Domain'] = analyze_subdomain(url)
             # exclude main domain and TLD

        # SSL/TLS analysis
        context = ssl.create_default_context()
        with socket.create_connection((domain, 443)) as sock:
            with context.wrap_socket(sock, server_hostname=domain) as ssock:
                cert = ssock.getpeercert()
                now = datetime.now(timezone.utc)

                # 3. SSL final state (HTTPS + valid cert + Trusted Issuer)
                if cert:
                    features['SSLfinal_State'] = -1 if check_ssl_issuer(url) else 0
                else:
                    features['SSLfinal_State'] = 1


                # 4. Certificate validity period
                not_before = datetime.strptime(
                    cert['notBefore'], "%b %d %H:%M:%S %Y GMT")
                not_after = datetime.strptime(
                    cert['notAfter'], "%b %d %H:%M:%S %Y GMT")
                features['Domain_registeration_length'] = (
                    not_after - not_before).days


        features['Request_URL'] = classify_url(url)

        features['URL_of_Anchor'] = extract_url_of_anchor(url)

        # 7. Web traffic estimation (pseudo-code - needs actual API implementation)
        visits = int(check_traffic(domain))
        if visits>100000:
            features['web_traffic'] = -1
        elif visits<100000 and visits>50000:
            features['web_traffic'] = 0
        else:
            features['web_traffic'] = 1

        spamhaus_data = asyncio.run(get_data(domain))

        features['score'] = spamhaus_data["score"]
        features['human'] = spamhaus_data["human"]
        features['identity'] = spamhaus_data["identity"]
        features['infra'] = spamhaus_data["infra"]
        features['malware'] = spamhaus_data["malware"]
        features['smtp'] = spamhaus_data["smtp"]
        

        return features

    except Exception as e:
        print(f"Error analyzing {url}: {str(e)}")
        return features


url = "google.com"
print(extractor(url))
