from .namespaces import MA, MADBDATA
from rdflib.namespace import XSD

TYPE_CONVERSION = {
    MA.relatedFirst: XSD.boolean,
    MA.notationNumber: XSD.integer,
    MADBDATA.oldDateModified: XSD.dateTime,
}