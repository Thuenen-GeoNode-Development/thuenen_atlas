from django import template
import logging

register = template.Library()

logger = logging.getLogger(__name__)

@register.filter
def get_iso_metadata_url(link_set):
    """
    Get the ISO metadata URL
    """
    iso_url = ''
    try:
        iso_url = link_set.get(name='ISO').url
    except Exception as e:
        logger.warning(f"Unable to get ISO metadata URL: {str(e)}")
        iso_url = ''
    return iso_url
