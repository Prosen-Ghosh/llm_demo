from langchain.tools import tool

@tool(description="Search for products by name")
def search_products(query: str) -> str:
    products = {
        "wireless headphones": ["WH-1000XM5", "AirPods Pro", "Sony WF-C700N"],
        "laptop": ["MacBook Pro", "Dell XPS 15", "ThinkPad X1"]
    }
    results = products.get(query.lower(), [])
    return f"Found products: {', '.join(results)}" if results else "No products found"

@tool(description="Check if a product is in stock")
def check_inventory(product_id: str) -> str:
    inventory = {
        "WH-1000XM5": "10 units in stock",
        "AirPods Pro": "5 units in stock",
        "MacBook Pro": "Out of stock"
    }
    return inventory.get(product_id, "Product not found")

TOOLS = [search_products, check_inventory]