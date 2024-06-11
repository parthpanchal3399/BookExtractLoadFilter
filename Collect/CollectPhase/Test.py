from lxml import etree

def validate(xml_path: str, xsd_path: str) -> bool:
    xmlschema_doc = etree.parse(xsd_path)
    xmlschema = etree.XMLSchema(xmlschema_doc)
    xml_doc = etree.parse(xml_path)
    result = xmlschema.validate(xml_doc)
    return result

# Parse the XML document
xml_doc = etree.parse('Books.xml')

# Define the namespaces
namespaces = {
    'ns': 'https://books.toscrape.com'
}

# Perform an XPath query with the namespace
titles = xml_doc.xpath('//ns:Title', namespaces=namespaces)
for title in titles:
    print(title.text)

print(validate("Books.xml", "Books.xsd"))
