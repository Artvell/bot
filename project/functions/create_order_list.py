from models import Post, Package
from functions.text_formatter import Formatter
import emoji
def create_order_list(basket):
    data = []
    for elem in basket:
        if not elem["is_package"]:
            product = Post.get(Post.id==elem["id"])
            name = Formatter(product).get_name()
            summ = int(elem["kol"])*product.cost
            data.append(
                {
                    "is_package":False,
                    "id":elem["id"],
                    "name":name,
                    "ammount":summ
                }
            )
        else:
            package = Package.get_by_id(elem["id"])
            data.append(
                {
                    "is_package":True,
                    "id":elem["id"],
                    "name":package.title,
                    "ammount":package.cost
                }
            )
    return data