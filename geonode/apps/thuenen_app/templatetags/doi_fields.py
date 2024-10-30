from django import template
from datetime import datetime
import requests
import logging
import re

register = template.Library()

logger = logging.getLogger(__name__)

@register.filter
def get_doi_title_and_date(doi_value):
    """
    Fetches the doi title and date from provided DOI
    """
    try:
        doi = extract_doi(doi_value)
        if not doi:
            raise Exception('Unable to extract doi')
        url = f"https://doi.org/{doi}"
        headers = {
            "Accept": "application/vnd.citationstyles.csl+json, application/rdf+xml"
        }
        
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            title = data.get("title", "Missing title")
            date = data.get("issued", {})
            year, month, day = date['date-parts'][0]
            date_obj = datetime(year, month, day)
            return {"title": title, "date": date_obj, "doi": doi}
        else:
            raise Exception("Failed to fetch the requested DOI")
    except Exception as e:
        logger.warning(f"Unable to get ISO metadata URL: {str(e)}")
        return {"title": "No title", "date": "No date"} 

def extract_doi(url):
    pattern = r'10\.(.*)'
    match = re.search(pattern, url)
    return match.group(0) if match else None
