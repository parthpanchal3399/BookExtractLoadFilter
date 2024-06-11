import sys

import requests
from lxml import html, etree
from word2number import w2n
import xml.etree.ElementTree as ET
import argparse


def validate(xml_path: str, xsd_path: str) -> bool:
    xmlschema_doc = etree.parse(xsd_path)
    xmlschema = etree.XMLSchema(xmlschema_doc)
    xml_doc = etree.parse(xml_path)
    result = xmlschema.validate(xml_doc)
    return result


def main(schema, output):
    ET.register_namespace('xmlns', "https://books.toscrape.com")
    XBooks = ET.Element('Books')
    XBooks.set('xmlns', "https://books.toscrape.com")
    XBooks.set('xmlns:xsi', "http://www.w3.org/2001/XMLSchema-instance")
    XBooks.set('xsi:schemaLocation', f'https://books.toscrape.com {schema}')

    for i in range(1, 51):  # Loop through 1-51 Pages
        url = f"https://books.toscrape.com/catalogue/category/books_1/page-{i}.html"
        response = requests.get(url)
        tree = html.fromstring(html=response.text)

        base_url = "https://books.toscrape.com/catalogue/"
        all_articles = tree.xpath("//ol/li/article")

        for article in all_articles:
            book_url = article.xpath("div[@class='image_container']/a/@href")[0]

            response2 = requests.get(base_url + book_url[6:])
            tree2 = html.fromstring(html=response2.text)

            product_main = tree2.xpath("//article[@class='product_page']")[0]
            genre = product_main.xpath("//ul[@class='breadcrumb']/li[3]/a/text()")[0]
            table = product_main.xpath("//table")[0]
            upc = table.xpath("tr[1]/td/text()")[0]
            prod_type = table.xpath("tr[2]/td/text()")[0]
            price_wo_tax = table.xpath("tr[3]/td/text()")[0][1:]
            price_w_tax = table.xpath("tr[4]/td/text()")[0][1:]
            tax = table.xpath("tr[5]/td/text()")[0][1:]
            no_reviews = table.xpath("tr[7]/td/text()")[0]
            title = product_main.xpath(".//h1/text()")[0]
            stars_text = product_main.xpath("//p[contains(@class, 'star-rating')]/@class")[0].split()[1]
            stars = w2n.word_to_num(stars_text)
            availibility = product_main.xpath(".//p[2]/text()")[1].strip()
            in_stock = ''.join(list(filter(lambda x: x.isdigit(), availibility)))
            description = tree2.xpath("//div[@id='product_description']/following-sibling::p/text()")
            if len(description) > 0:
                description = description[0]

            # Start generating the XML file
            XBook = ET.SubElement(XBooks, 'Book', UPC=upc, Genre=genre)
            ET.SubElement(XBook, 'Title', ProductType=prod_type).text = title
            ET.SubElement(XBook, 'Price', WithTax=str(False), Currency=price_wo_tax[0]).text = price_wo_tax[1:]
            ET.SubElement(XBook, 'TaxAmt', Currency=tax[0]).text = tax[1:]
            ET.SubElement(XBook, 'Price', WithTax=str(True), Currency=price_w_tax[0]).text = price_w_tax[1:]
            ET.SubElement(XBook, 'Availability', InStock=str(True) if in_stock != '' else str(False)).text = in_stock
            ET.SubElement(XBook, 'NoOfReviews', Stars=str(stars)).text = no_reviews
            ET.SubElement(XBook, 'Description').text = description

            ## Debug Info
            print(f"DEBUG: i = {i}\tUPC = {upc}\tTITLE = {title}")
            print("----------------------------------------------------------")
            # break

    # Write the generated XML to a file
    tree = ET.ElementTree(XBooks)
    ET.indent(tree, space="\t", level=0)
    tree.write(output, xml_declaration=True, encoding='utf-8', method="xml")
    print("Output written to file.")
    print()
    print("Validating XML against given Schema....")

    if validate(output, schema):
        print("Generated XML is valid!")
    else:
        print("Generated XML is invalid!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Python Program to Scrape https://books.toscrape.com and saving the data to XML",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--output", help="Output Path of XML file", required=True)
    parser.add_argument("--schema", help="Schema File Location", required=True)
    args = parser.parse_args()
    print("Start Processing:")
    main(args.schema, args.output)
    print("Done.")

