import ssl
import socket
import OpenSSL

def check_ssl_issuer(domain):
    # List of trusted CAs (you can expand this list)
    trusted_cas = [
        "DigiCert Inc",
        "Let's Encrypt",
        "Sectigo Limited",
        "GlobalSign",
        "Amazon",
        "GoDaddy.com, Inc.",
        "Actalis",
        "Entrust",
        "Add Trust",
        "Certum",
        "Verisign",
        "GeoTrust",
        "Comodo",
        "DigiCert",
        "GoDaddy",
        "SecureTrust",
        "RapidSSL",
        "Thawte",
        "Google Trust Services",
    ]

    try:
        # Remove "https://" if present in domain input
        domain = domain.replace("https://", "").replace("http://", "").strip("/")

        # Create an SSL context
        context = ssl.create_default_context()
        
        # Establish an SSL connection
        with socket.create_connection((domain, 443), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=domain) as secure_sock:
                # Get the certificate
                cert = secure_sock.getpeercert(binary_form=True)
                x509 = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_ASN1, cert)

                # Extract issuer information
                issuer = dict(x509.get_issuer().get_components())
                issuer_cn = issuer.get(b'O', b'Unknown').decode()

                # Print the issuer name
                print(f"Issuer: {issuer_cn}")

                # Check if the issuer is trusted
                is_trusted = issuer_cn in trusted_cas

                return is_trusted

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return False
