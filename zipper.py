# Importing necessary libraries
import pyshorteners
from urllib.parse import urlparse
import re
from pyfiglet import Figlet  

# Color codes for console output
Red = '\033[31m'  # red
Green = '\033[32m'  # green
Cyan = '\033[36m'  # cyan
White = '\033[0m'   # white
Yellow = '\033[33m'  # yellow

# Banner creation using pyfiglet
banner_text = "URL-ZIPPER"
fig = Figlet(font='slant')  # Choose a font style
banner = f"{Green}{fig.renderText(banner_text)}{White}\n"

# Program version
VERSION = '1.0.0'

def print_banners():
    """
    Print program banners including ASCII art.
    """
    print(f'{Red}{banner}{White}\n')
    print(f'{Green}╰➤ {Cyan}Version      : {White}{VERSION}')
    print(f'{Green}╰➤ {Cyan}Creator      : {White}CyberKnight')

################
# Display the banners
print_banners()

# Initialize the URL shorteners
short = pyshorteners.Shortener()

# Additional URL shorteners
shorteners = [
    short.tinyurl,
    short.osdb,
    short.dagd,
    short.clckru,
]

# Input validation functions

def validate_web_url(url):
    """
    Validate the format of a web URL.
    """
    url_pattern = re.compile(
        r'^(https?://)'  # starts with 'https://'
        r'([a-zA-Z0-9-]+\.)*'  # optional subdomains
        r'([a-zA-Z]{2,})'  # domain
        r'(:\d{1,5})?'  # optional port
        r'(/.*)?$'
    )

    if not url_pattern.match(url):
        raise ValueError("Invalid URL format. Please provide a valid web URL.")

def validate_custom_domain(domain):
    """
    Validate the format of a custom domain.
    """
    domain_pattern = re.compile(r'^[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')

    if not domain_pattern.match(domain):
        raise ValueError("Invalid custom domain. Please provide a valid domain name.")

def format_phish_keywords(keywords):
    """
    Format phishing keywords.
    """
    max_length = 15
    if not isinstance(keywords, str):
        raise TypeError("Input must be a string.")

    if " " in keywords:  # Fix variable name
        raise TypeError("Phishing keywords should not contain spaces. Use '-' to separate them.")

    if len(keywords) > max_length:
        raise ValueError("Input string exceeds the maximum allowed length.")

    return "-".join(keywords.split())

# Input from the user with validation
try:
    while True:
        web_url = input(f"{Green}Enter the original link {White}(ex: https://www.ngrok.com): {White}")
        try:
            validate_web_url(web_url)
            break
        except ValueError as e:
            print(e)

    while True:
        custom_domain = input(f"\n{Yellow}Enter your custom domain {White}(ex: gmail.com): {White}")
        try:
            validate_custom_domain(custom_domain)
            break
        except ValueError as e:
            print(e)

    while True:
        phish = input(f"\n{Cyan}Enter phishing keywords {White}(ex: free-stuff, login): {White}")
        try:
            phish = format_phish_keywords(phish)
            break
        except TypeError as e:
            print(e)

    # Prepare the data for the request
    data = {
        'url': web_url,
        'shorturl': '',
    }

    # Shorten the original URL with multiple URL shorteners
    short_urls = [shortener.short(web_url) for shortener in shorteners]

    # Mask the URLs with custom domain and phishing keywords
    def mask_url(domain, keyword, url):
        # Use urlparse to properly split the URL
        parsed_url = urlparse(url)

        # Reconstruct the URL with the custom domain and phishing keyword
        return f"{parsed_url.scheme}://{domain}-{keyword}@{parsed_url.netloc}{parsed_url.path}"

    # Print the results
    print(f"\n{Yellow}Original URL:{White}", web_url, "\n")
    print(f"{Green}[~] {Red}Masked URL (using multiple shorteners):{White}")
    for i, short_url in enumerate(short_urls):
        masked_url = mask_url(custom_domain, phish, short_url)
        print(f"{Green}╰➤ {Cyan}Shortener {White} {i + 1}: {masked_url}")

except Exception as e:
    print(f"{Red}An error occurred: {White}{str(e)}")
