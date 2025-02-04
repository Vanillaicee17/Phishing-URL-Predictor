# def extractor(url):
#     features ={
#         'having_IP_Address': '-1', #can be checked
#         'URL_Length': '1', #can be extracted
#         'Shortining_Service': '1', #have to figure out common shortening services
#         'having_At_Symbol': '1', #can be checked
#         'double_slash_redirecting': '-1', #can be checked
#         'Prefix_Suffix': '-1', #can be extracted
#         'having_Sub_Domain': '-1', #can be extracted
#         'SSLfinal_State': '-1',#https://github.com/narbehaj/ssl-checker or SSL library or https://apify.com/sorrek/url-parser
#         'Domain_registeration_length': '-1', #DNS Look up
#         'Favicon': '1', #HTML Parsing is required
#         'port': '1',
#         'HTTPS_token': '-1', #https://apify.com/sorrek/url-parser
#         'Request_URL': '1',
#         'URL_of_Anchor': '-1',
#         'Links_in_tags': '1',
#         'SFH': '-1',
#         'Submitting_to_email': '-1',
#         'Abnormal_URL': '-1',
#         'Redirect': '0',
#         'on_mouseover': '1',
#         'RightClick': '1',
#         'popUpWidnow': '1',
#         'Iframe': '1',
#         'age_of_domain': '-1', #DNS look up
#         'DNSRecord': '-1', #DNS look up
#         'web_traffic': '-1',
#         'Page_Rank': '-1',
#         'Google_Index': '1',
#         'Links_pointing_to_page': '1',
#         'Statistical_report': '-1',
#     }

# import ssl
# import socket

# domain = 'jaipur.manipal.edu'

# context = ssl.create_default_context()
# with socket.create_connection((domain, 443)) as sock:
#     with context.wrap_socket(sock, server_hostname=domain) as ssock:
#         cert = ssock.getpeercert()
#         if cert:  # Check if the certificate exists
#             print("Valid certificate retrieved!")
#         else:
#             print("No certificate found!")

from urllib.parse import urlparse

url = "http://www.google.com/"
parsed_url = urlparse(url)

# Get port number
port = parsed_url.port

if port:
    print(f"Port number: {port}")
else:
    port = parsed_url.port or (443 if parsed_url.scheme == "https" else 80)
    print(f"Port: {port}")
