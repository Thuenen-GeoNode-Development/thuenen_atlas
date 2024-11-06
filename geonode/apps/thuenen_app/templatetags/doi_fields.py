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
        url = f"https://doi.org/{doi}"
        headers = {
            "Accept": "application/vnd.citationstyles.csl+json, application/rdf+xml"
        }
        
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            title = data.get("title", "Missing title")
            date_obj = extract_date(data)

            return {"title": title, "date": date_obj}
        else:
            raise Exception("Unable to fetch the requested DOI")
    except Exception as e:
        logger.warning(f"Unable to get ISO metadata URL: {str(e)}")
        return {"title": "Missing title", "date": None} 

def extract_doi(url):
    pattern = r'10\.(.*)'
    match = re.search(pattern, url)
    if not match:
        raise Exception('Unable to extract doi')
    return match.group(0)

def extract_date(response_data):
    try:
        date_parts = response_data.get('issued').get('date-parts', [[]])[0]
        
        if len(date_parts) == 1:
            year = int(date_parts[0])
            return datetime(year, 1, 1)
        elif len(date_parts) == 2:
            year, month = map(int, date_parts)
            return datetime(year, month, 1)
        elif len(date_parts) == 3:
            year, month, day = map(int, date_parts)
            return datetime(year, month, day)
        else:
            raise ValueError("Invalid date-parts structure.")
    
    except (TypeError, ValueError) as e:
        logger.warning(f"Error parsing date: {str(e)}")
        return None
