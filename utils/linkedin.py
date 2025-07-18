# utils/linkedin.py

import urllib.parse

def infer_linkedin_url(full_name: str, company: str = "") -> str:
    """
    Simulates a LinkedIn search URL based on name and company.

    Args:
        full_name (str): Full name of the lead
        company (str): Company or brand for disambiguation

    Returns:
        str: A LinkedIn search URL for manual review
    """
    if not full_name:
        return ""
    
    query = full_name
    if company:
        query += f" {company}"
    
    encoded = urllib.parse.quote(query)
    return f"https://www.linkedin.com/search/results/people/?keywords={encoded}"
# LinkedIn profile handling and scraping (manual or API)
