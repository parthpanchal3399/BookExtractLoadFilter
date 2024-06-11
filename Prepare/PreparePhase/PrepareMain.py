import sys

import mysql.connector
from lxml import etree
import argparse


def main(server, username, passwd, input):
    try:
        mydb = mysql.connector.connect(
            host=server,
            user=username,
            password=passwd,
        )
        print("Connected to database server...")

        mycursor = mydb.cursor()

        # Create Database
        mycursor.execute("CREATE DATABASE IF NOT EXISTS texttech")
        print("Created database 'texttech'")

        # Create Table

        mycursor.execute("""
        CREATE TABLE IF NOT EXISTS texttech.Books
        (
            UPC VARCHAR(50) PRIMARY KEY,
            Genre VARCHAR(50),
            Title VARCHAR(200),
            ProductType VARCHAR(50),
            Currency CHAR(1),
            PriceWOTax DOUBLE(5, 2),
            TaxAmt DOUBLE(5, 2),
            TotalPrice DOUBLE(5, 2),
            InStock TINYINT(1),
            Availability INT,
            Stars INT,
            NoOfReviews INT,
            Description VARCHAR(5000)
        )
        """)
        print("Created table 'Books'")

        # Read and parse the Books.xml file
        root = etree.parse(input)
        namespaces = {
            'ns': 'https://books.toscrape.com'
        }

        books = root.xpath('//ns:Book', namespaces=namespaces)
        for book in books:
            upc = book.xpath("@UPC")[0]
            genre = book.xpath("@Genre")[0]
            title = book.find("ns:Title", namespaces=namespaces)
            title_text = title.text
            producttype = title.xpath("@ProductType")[0]
            pricewotax = book.find("ns:Price[@WithTax='False']", namespaces=namespaces)
            currency = pricewotax.xpath("@Currency")[0]
            pricewotax_text = pricewotax.text
            taxamt = book.find("ns:TaxAmt", namespaces=namespaces).text
            totalprice = book.find("ns:Price[@WithTax='True']", namespaces=namespaces).text
            availability = book.find("ns:Availability", namespaces=namespaces)
            instock = availability.xpath("@InStock")[0]
            availability_text = availability.text
            noofreviews = book.find("ns:NoOfReviews", namespaces=namespaces)
            stars = noofreviews.xpath("@Stars")[0]
            noofreviews_text = noofreviews.text
            desc = book.find("ns:Description", namespaces=namespaces).text

            # Insert parsed data into SQL table
            insert_sql = ("""INSERT INTO texttech.Books (UPC, Genre, Title, ProductType, Currency,
                        PriceWOTax, TaxAmt, TotalPrice, InStock, Availability, Stars, NoOfReviews, Description)
                        values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""")

            values = (str(upc), str(genre), str(title_text), str(producttype), str(currency),
                      float(str(pricewotax_text)), float(str(taxamt)), float(str(totalprice)),
                      1 if bool(str(instock)) else 0, int(str(availability_text)),
                      int(str(stars)), int(str(noofreviews_text)), str(desc))

            mycursor.execute(insert_sql, values)
            mydb.commit()
            print("Record inserted successfully into 'Books' table")
            # break
    except mysql.connector.Error as error:
        print("Error: {}".format(error))
    finally:
        if mydb.is_connected():
            mycursor.close()
            mydb.close()
            print("MySQL connection is closed")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Python Program to create and load database with data from XML File",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--server", help="Database Server", required=True)
    parser.add_argument("--username", help="Database Username", required=True)
    parser.add_argument("--password", help="Database Password", required=False)
    parser.add_argument("--input", help="Full path of input XML File", required=True)
    args = parser.parse_args()
    print("Start Processing:")
    main(args.server, args.username, args.password, args.input)
    print("Done.")

