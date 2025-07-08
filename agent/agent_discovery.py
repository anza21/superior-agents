import os
import sys
import argparse
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.agent.affiliate_promoter import AliExpressAPIClient, EbayAPIClient

DEFAULT_QUERY = "smartwatch"


def discover_products(limit=10, query=DEFAULT_QUERY):
    ali_client = AliExpressAPIClient()
    ebay_client = EbayAPIClient()
    ali_products = [p for p in ali_client.search_products(query=query, limit=limit)]
    ebay_products = [p for p in ebay_client.search_products(query=query, limit=limit)]
    ali_products_dicts = [p.__dict__ for p in ali_products]
    ebay_products_dicts = [p.__dict__ for p in ebay_products]
    all_products = ali_products_dicts + ebay_products_dicts
    print(f"[DISCOVERY] AliExpress: {len(ali_products_dicts)} | eBay: {len(ebay_products_dicts)} | Total: {len(all_products)} products (query='{query}')")
    return all_products

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Product discovery from AliExpress and eBay (no filters).")
    parser.add_argument("--query", type=str, default=DEFAULT_QUERY, help="Product search query (default: 'smartwatch')")
    parser.add_argument("--limit", type=int, default=10, help="Max products per source (default: 10)")
    args = parser.parse_args()
    products = discover_products(limit=args.limit, query=args.query)
    for p in products:
        print(f"{p.get('source', '').capitalize()} | {p.get('title', '')} | Rating: {p.get('rating', '')} | Price: {p.get('price', '')} | Images: {p.get('image', '')}")
    print("\nTo run this script:")
    print("cd ~/superior-agents/agent && source ../agent-venv/bin/activate && export PYTHONPATH=.. && python agent_discovery.py --query 'smartwatch' --limit 10")
    # Save products to products.json for the next step
    import json
    with open("products.json", "w") as f:
        json.dump(products, f, indent=2)
    print("\nProducts saved to products.json for use in image/video collage script.") 