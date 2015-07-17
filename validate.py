#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    @author Joelmir Ribacki 2015
"""

from lxml import etree

def incorporate_imports(tags, location,imports):
    '''
        Get file's tags to incorporate on the base xsd file.
    '''
    xsd_doc = etree.XML(open(location).read())
    for import_tag in xsd_doc.iter():
        #No import 'Comments' elements
        if type(import_tag) == 'lxml.etree._Element' and not 'schema' not in tag.tag:
            if 'import' in import_tag.tag:
                #Verify the file name if is the first time to import, 
                if import_tag.attrib['schemaLocation'] not in imports:
                    imports.append(import_tag.attrib['schemaLocation'])
                    #append tags recursive from others imports
                    tags.append(incorporate_imports(xsd_root, import_tag.attrib['schemaLocation']))
            else:
                tags.append(import_tag)

def validate(xml_filename, xsd_filename):
    '''
    xml_filename: File to validate
    xsd_filename: File with the schema rules

    '''
    #List of imports
    imports = []

    #Open Files
    xml_file = open(xml_filename)
    xsd_file = open(xsd_filename)
        
    #Get Objects
    xml_doc = etree.XML(xml_file.read())
    xsd_doc = etree.XML(xsd_file.read())
    
    #list of tags to append on the xsd file
    tags_import = []
    
    #verify the import tags
    for import_tag in [tag for tag in xsd_doc.iter() if type(tag) == 'lxml.etree._Element' and 'import' in tag.tag]:
        imports.append(import_tag.attrib['schemaLocation'])
        #get tags from import file
        sub_element = incorporate_imports(tags_import, import_tag.attrib['schemaLocation'], imports)

    #Append tags from files
    for tag in tags_import:
        xsd_doc.append(tag)

    #Create a schema object
    xmlschema = etree.XMLSchema(xsd_doc)
    
    #Try validade
    xmlschema.assertValid(xml_doc)
    return xml_doc

