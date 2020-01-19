from .namespaces import MA, MADBDATA
from rdflib.namespace import XSD

TYPE_CONVERSION = {
    MA.relatedFirst: XSD.boolean,
    MADBDATA.oldDateModified: XSD.dateTime,
}