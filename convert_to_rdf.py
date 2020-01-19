#!/usr/bin/env python
import json
import re

import bonobo
from bonobo.config import use_context_processor
import rdflib
from rdflib import Literal, Namespace, URIRef
from rdflib.namespace import split_uri, RDF, RDFS, NamespaceManager
from rdflib.plugins.serializers.nt import _nt_row

from src.namespaces import DCTERMS, SCHEMA, MA, MADBDATA, MADBRES, MADBSRC, MADBAPI
from src.rules import TYPE_CONVERSION

input_files = []

nsm = NamespaceManager(rdflib.Graph())
nsm.bind('dcterm', DCTERMS)
nsm.bind('dcterms', DCTERMS)
nsm.bind('schema', SCHEMA)
nsm.bind('ma', MA)
nsm.bind('madbdata', MADBDATA)

prefix_to_ns = {}
for p, uri in nsm.namespaces():
    prefix_to_ns[p] = Namespace(uri)


def resolve_qname(qname):
    prefix, name = split_uri(qname)
    if prefix[:-1] in prefix_to_ns:
        return prefix_to_ns[prefix[:-1]][name]
    return None


def read_jsonl():
    for file in input_files:
        with open(file, 'r') as f:
            for line in f:
                yield json.loads(line)


def convert_to_ｔtriple(row):
    s = MADBRES[row['aipId']]
    for key, values in row['metadata'].items():
        for value in values:
            m = re.search(r'xml:lang="(.+)"', key)
            lang = m.group(1) if m else None
            if m:
                key = key.replace(m.group(0), '')
            p = resolve_qname(key.strip())
            if not p:
                print('unknown prefix', key)
            o = Literal(value, lang=lang)
            yield s, p, o

    yield s, DCTERMS.source, MADBAPI[row['aipId']]
    yield s, RDFS.seeAlso, MADBSRC[row['aipId']]


def cleanse(s, p, o):
    if p == RDF.type:
        o = MA[o]
    elif p == SCHEMA.isPartOf:
        o = MADBRES[o]
    elif p == RDFS.seeAlso and o.startswith('http'):
        o = URIRef(o)
    elif p == DCTERMS.creator and re.match(r'C\d+', o):
        o = MADBRES[o]
    elif p in TYPE_CONVERSION:
        o = Literal(o, datatype=TYPE_CONVERSION[p])
    return (s, p, o),


def with_opened_file(self, context):
    with context.get_service('fs').open('madb.nt', 'w') as f:
        yield f


@use_context_processor(with_opened_file)
def write_nt(f, triple):
    f.write(_nt_row(triple))


def get_graph(**options):
    graph = bonobo.Graph()
    graph.add_chain(read_jsonl, convert_to_ｔtriple, cleanse, write_nt)

    return graph


def get_services(**options):
    return {}


# The __main__ block actually execute the graph.
if __name__ == '__main__':
    parser = bonobo.get_argument_parser()
    parser.add_argument('files', nargs='*')
    with bonobo.parse_args(parser) as options:
        input_files = options['files']
        bonobo.run(
            get_graph(**options),
            services=get_services(**options)
        )
