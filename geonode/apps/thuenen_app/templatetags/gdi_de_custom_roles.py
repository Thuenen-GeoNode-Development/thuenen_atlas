from django import template

register = template.Library()

GDI_DE_ROLE_LABEL_MAPPING = {
    'Owner': 'owner',
    'Point of Contact': 'pointOfContact',
    'Metadata Author': 'author',
    'Processor': 'processor',
    'Publisher': 'publisher',
    'Custodian': 'custodian',
    'Distributor': 'distributor',
    'Resource User': 'user',
    'Resource Provider': 'resourceProvider',
    'Originator': 'originator',
    'Principal Investigator': 'principalInvestigator'
}

@register.filter
def get_gdi_compliant_role_label(value):
    """
    Replace labels based on the GDI_DE_ROLE_LABEL_MAPPING dict.
    Example: {{ role_label_string|get_gdi_compliant_role_label }}
    """
    return GDI_DE_ROLE_LABEL_MAPPING.get(value, value)
