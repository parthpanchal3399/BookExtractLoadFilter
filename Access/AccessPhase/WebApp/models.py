from django.db import models

# Create your models here.
class Book():
    def __init__(self, upc, genre, title, prod_type, currency, pricewotax, taxamt, totalprice, instock, availability, stars, noofreviews, description):
        self.UPC = upc
        self.Genre = genre
        self.Title = title,
        self.ProductType = prod_type,
        self.Currency = currency,
        self.PriceWOTax = pricewotax,
        self.TaxAmt = taxamt,
        self.TotalPrice = totalprice,
        self.InStock = instock,
        self.Availability = availability,
        self.Stars = stars,
        self.NoOfReviews = noofreviews,
        self.Description = description
