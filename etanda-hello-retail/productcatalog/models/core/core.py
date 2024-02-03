from dataclasses import dataclass


@dataclass
class Category():
    type: str = "Category"
    name: str = None
    pass

    def __str__(self):
        pass

@dataclass
class Categories():
    type: str = "Categories"
    name: str = None
    pass

    def __str__(self):
        pass


@dataclass
class Product():
    type: str = "Product"
    id: str = None
    brand: str = None
    name: str = None
    description: str = None 
    image: str = None
    pass

    def __str__(self):
        pass

@dataclass
class Products():
    type: str = "Products"
    pass

    def __str__(self):
        pass