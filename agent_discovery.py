import os
from agent.src.agent.affiliate_promoter import AliExpressAPIClient, EbayAPIClient

MIN_RATING = 4.3

# Real AliExpress and eBay API integration

def discover_products(min_rating=MIN_RATING, limit=10):
    ali_client = AliExpressAPIClient()
    ebay_client = EbayAPIClient()
    ali_products = [p for p in ali_client.search_products(limit=limit) if getattr(p, "rating", 0) and p.rating >= min_rating]
    ebay_products = [p for p in ebay_client.search_products(limit=limit) if getattr(p, "rating", 0) and p.rating >= min_rating and getattr(p, "description", "new").lower() == "new"]
    # Convert ProductData objects to dicts for uniformity
    ali_products_dicts = [p.__dict__ for p in ali_products]
    ebay_products_dicts = [p.__dict__ for p in ebay_products]
    all_products = ali_products_dicts + ebay_products_dicts
    print(f"[DISCOVERY] AliExpress: {len(ali_products_dicts)} | eBay: {len(ebay_products_dicts)} | Total: {len(all_products)} products (min_rating={min_rating})")
    return all_products

if __name__ == "__main__":
    products = discover_products()
    for p in products:
        print(f"{p.get('source', '').capitalize()} | {p.get('title', '')} | Rating: {p.get('rating', '')} | Price: {p.get('price', '')} | Images: {p.get('image', '')}") 