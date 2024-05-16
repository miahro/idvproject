import ssl
import socket


def check_ssl_certificate(url):
    """
    Check the SSL certificate of a URL.
    """
    hostname = url.split("://")[-1].split("/")[0]
    ctx = ssl.create_default_context()
    with ctx.wrap_socket(socket.socket(), server_hostname=hostname) as s:
        s.connect((hostname, 443))
        certificate = s.getpeercert()
    return certificate


def main():

    # url = "https://budjetti.vm.fi/indox/opendata/2024/tae/eduskunnanKirjelma/2024-tae-eduskunnanKirjelma.html"
    url = "https://www.helsinki.fi/"
    # url = "https://budjetti.vm.fi/indox/opendata/2024/tae/eduskunnanKirjelma/2024-tae-eduskunnanKirjelma-21.csv"
    certificate = check_ssl_certificate(url)
    print(certificate)


if __name__ == "__main__":
    main()
