from django.shortcuts import render
from django.http import HttpResponse
from django.db import connection
from drb.xquery import DrbXQuery
import drb.topics.resolver as resolver


def index(request):
    c = connection.cursor()

    sql = "SELECT * FROM books;"
    c.execute(sql)
    all_books = c.fetchall()


    if request.GET:
        print(request.GET)
        if request.GET.get('i_Title') != '':
            title = request.GET.get('i_Title')
            title_pattern = "%" + title.lower() + "%"
            sql = "SELECT * FROM books WHERE LOWER(Title) LIKE %s;"
            c.execute(sql, (title_pattern,))
            all_books = c.fetchall()
        if request.GET.get('i_Desc') != '':
            desc = request.GET.get('i_Desc')
            desc_pattern = "%" + desc.lower() + "%"
            sql = "SELECT * FROM books WHERE LOWER(Description) LIKE %s;"
            c.execute(sql, (desc_pattern,))
            all_books = c.fetchall()
        if request.GET.get('i_Genre') is not None:
            genre = request.GET.get('i_Genre')
            sql = "SELECT * FROM books WHERE Genre = %s;"
            c.execute(sql, (genre,))
            all_books = c.fetchall()
        if request.GET.get('hid_Price') == 'on':
            minprice = request.GET.get('i_minPrice')
            maxprice = request.GET.get('i_maxPrice')
            sql = "SELECT * FROM books WHERE TotalPrice BETWEEN %s AND %s"
            c.execute(sql, (int(minprice), int(maxprice), ))
            all_books = c.fetchall()
        if request.GET.get('hid_instock') == '1':
            instock = request.GET.get('hid_instock')
            sql = "SELECT * FROM books WHERE InStock = %s"
            c.execute(sql, (int(instock), ))
            all_books = c.fetchall()
        if request.GET.get('hid_stars') == 'on':
            stars = request.GET.get('i_starsRange')
            sql = "SELECT * FROM books WHERE Stars >= %s"
            c.execute(sql, (int(stars), ))
            all_books = c.fetchall()
        if request.GET.get('hid_Avail') == 'on':
            avail = request.GET.get('i_availRange')
            sql = "SELECT * FROM books WHERE Availability >= %s"
            c.execute(sql, (int(avail), ))
            all_books = c.fetchall()

    return render(request, 'index.html', {'all_books': all_books[0:50], 'sql': c._executed.decode("utf-8")})


# def XQuery(request):
#     all_outputs = []
#     node = resolver.create(r"WebApp/Books.xml")
#     doc = r"WebApp/Books.xml"
#     namespace_uri = "https://books.toscrape.com"
#     query_string = f"""
#     declare default element namespace "{namespace_uri}";
#     for $x in doc("{doc}")/Books/Book
#     return $x"""
#     query = DrbXQuery(query_string)
#     result = query.execute(node)
#     for x in result:
#         all_outputs.append(create_output_dict(x, namespace_uri))
#         # break
#     # print(all_outputs[0])
#     return render(request, 'xquery.html', {"all_outputs": all_outputs[0:50], 'xquery': query_string})

def XQuery(request):
    all_outputs = []
    node = resolver.create(r"WebApp/Books.xml")
    doc = r"WebApp/Books.xml"
    namespace_uri = "https://books.toscrape.com"

    base_query = f"""
    declare default element namespace "{namespace_uri}";
    for $x in doc("{doc}")/Books/Book
    """

    conditions = []

    if request.GET:
        if request.GET.get('i_Title'):
            title = request.GET.get('i_Title').lower()
            conditions.append(f'contains(lower-case($x/Title), "{title}")')

        if request.GET.get('i_Desc'):
            desc = request.GET.get('i_Desc').lower()
            conditions.append(f'contains(lower-case($x/Description), "{desc}")')

        if request.GET.get('i_Genre'):
            genre = request.GET.get('i_Genre')
            conditions.append(f'$x/@Genre = "{genre}"')

        if request.GET.get('hid_Price') == 'on':
            minprice = request.GET.get('i_minPrice')
            maxprice = request.GET.get('i_maxPrice')
            conditions.append(f'$x/Price[@WithTax="True"] >= {minprice} and $x/Price[@WithTax="True"] <= {maxprice}')

        if request.GET.get('hid_instock') == '1':
            conditions.append('$x/Availability/@InStock = "True"')

        if request.GET.get('hid_stars') == 'on':
            stars = request.GET.get('i_starsRange')
            conditions.append(f'$x/NoOfReviews/@Stars >= {stars}')

        if request.GET.get('hid_Avail') == 'on':
            avail = request.GET.get('i_availRange')
            conditions.append(f'$x/Availability >= {avail}')

    if conditions:
        where_clause = "where " + " and ".join(conditions)
    else:
        where_clause = ""

    query_string = f"{base_query} {where_clause} return $x"

    query = DrbXQuery(query_string)
    result = query.execute(node)

    for x in result:
        all_outputs.append(create_output_dict(x, namespace_uri))

    return render(request, 'xquery.html', {"all_outputs": all_outputs[0:50], 'xquery': query_string})


def create_output_dict(context, namespace_uri):
    output_dict = dict()
    if context.is_node:
        for attr, val in context.node.attributes.items():
            output_dict[attr[0]] = val

        output_dict["Title"] = context.node.children[0].value
        output_dict["ProductType"] = context.node.children[0].attributes.get(('ProductType', None))
        output_dict["TotalPrice"] = context.node.children[1].attributes.get(('Currency', None)) + context.node.children[1].value
        output_dict["TaxAmt"] = context.node.children[2].attributes.get(('Currency', None)) + context.node.children[2].value
        output_dict["PriceWOTax"] = context.node.children[3].attributes.get(('Currency', None)) + context.node.children[3].value
        output_dict["Availability"] = context.node.children[4].value
        output_dict["InStock"] = 1 if context.node.children[4].attributes.get(('InStock', None)) == "True" else 0
        output_dict["NoOfReviews"] = context.node.children[5].value
        output_dict["Stars"] = context.node.children[5].attributes.get(('Stars', None))
        output_dict["Description"] = context.node.children[6].value



    return output_dict



