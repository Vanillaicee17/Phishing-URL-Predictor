import ssl
import socket
from datetime import datetime
from urllib.parse import urlparse
# import whois
# import dns.resolver
# import requests
from dateutil.relativedelta import relativedelta
# import time
# import requests
from ssl_checker import check_ssl_issuer
from web_traffic import check_traffic
from subdomain import analyze_subdomain
from URL_of_anchor import extract_url_of_anchor
from request_urls import classify_url




def extractor(url):
    features = {
        'Prefix_Suffix': 1,
        'having_Sub_Domain': 1,
        'SSLfinal_State': 1,
        # 'Domain_registeration_length': -1,
        'Request_URL': 1,
        # 'URL_of_Anchor': -1,
        # 'Links_in_tags': -1,
        # 'SFH': -1,
        # 'age_of_domain': -1,
        # 'DNSRecord': -1,
        'web_traffic': 1,
        # 'Page_Rank': -1,
        # 'Google_Index': -1,
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
                now = datetime.utcnow()

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

        # 5. Domain age using WHOIS
        # domain_info = whois.whois(domain)
        # if domain_info.creation_date:
        #     if isinstance(domain_info.creation_date, list):
        #         creation_date = domain_info.creation_date[0]
        #     else:
        #         creation_date = domain_info.creation_date
        #     age = relativedelta(now, creation_date)
        #     features['age_of_domain'] = age.years * 12 + age.months

        # # 6. DNS records check
        # try:
        #     dns.resolver.resolve(domain, 'MX')
        #     features['DNSRecord'] = 1
        # except dns.resolver.NoAnswer:
        #     features['DNSRecord'] = -1

        features['Request_URL'] = classify_url(url)

        features['URL_of_Anchor'] = extract_url_of_anchor(url)

        # 7. Web traffic estimation (pseudo-code - needs actual API implementation)
        visits = int(check_traffic(domain))
        print("this is the traffic >",visits)
        if visits>100000:
            features['web_traffic'] = -1
        elif visits<100000 and visits>50000:
            features['web_traffic'] = 0
        else:
            features['web_traffic'] = 1
            

        # 8. PageRank check (example implementation)
        # features['Page_Rank'] = get_page_rank(domain)

        # 9. Google Index check
        # try:
        #     response = requests.get(
        #         f"https://www.google.com/search?q=site:{domain}", timeout=5)
        #     features['Google_Index'] = 1 if domain in response.text else -1
        # except:
        #     features['Google_Index'] = -1

        return features

    except Exception as e:
        print(f"Error analyzing {url}: {str(e)}")
        return features


