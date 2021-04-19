import string
import random


def get_sku(product_type, size, stuff, color):
    return ("".join([product_type[0:3].upper()]) + "-" +
            "".join([random.choice(string.digits) for i in range(9)]) + "-" +
            "".join([size.upper()]) + "-" + ("".join([stuff[0:3].upper()])) + "-" +
            ("".join([color[0:3].upper()])))
