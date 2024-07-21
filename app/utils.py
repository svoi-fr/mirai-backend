def strip_https(url):
    """
    Strips 'https://' from the URL if it exists.
    
    Parameters:
    url (str): The URL to strip 'https://' from.

    Returns:
    str: The URL without 'https://'.
    """
    if url.startswith("https://"):
        return url[8:]
    return url

def add_https(url):
    """
    Adds 'https://' to the URL if it does not already have 'https://', 
    or replaces 'http://' with 'https://'.
    
    Parameters:
    url (str): The URL to add 'https://' to.

    Returns:
    str: The URL with 'https://'.
    """
    if url.startswith("http://"):
        return "https://" + url[7:]
    elif not url.startswith("https://"):
        return "https://" + url
    return url
