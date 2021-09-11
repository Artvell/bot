from models import Package,Post, ProductsInPackage
from functions import Formatter

def create_text(package_id):
    package = Package.get_by_id(package_id)
    products = ProductsInPackage().select().join(Package).where(ProductsInPackage.package == package.id)
    text = f"Пакет №{package_id}<b>{package.title}</b>\nСтоимость: {package.cost}\n"
    if products.count() > 0:
        for element in products:
            product = element.product
            if product is not None:
                formatter = Formatter(product)
                info = f'<a href="{product.telegraph}">{formatter.get_name()}</a>  {product.cost}\n'
                text += info
    return text