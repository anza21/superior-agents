#!/usr/bin/env python3
"""
SuggestoAI Autonomous Affiliate Agent - Auto Publisher

Usage:
$ python3 publish_post.py --title "Product Title" --desc "Short description" --img "img_url_or_path" --afflink "affiliate_url" [--review "review_html"]

- Προσθέτει νέα card στο ai-recommends.html (πάνω-πάνω)
- (Προαιρετικά) Δημιουργεί νέο HTML post (αν δοθεί --review)
"""
import argparse
import datetime
import os
from bs4 import BeautifulSoup

parser = argparse.ArgumentParser(description='Auto-publish AI product recommendation.')
parser.add_argument('--title', required=True, help='Product title')
parser.add_argument('--desc', required=True, help='Short description')
parser.add_argument('--img', required=True, help='Image URL or path')
parser.add_argument('--afflink', required=True, help='Affiliate link')
parser.add_argument('--review', help='Full HTML review (optional)')
args = parser.parse_args()

CARD_TEMPLATE = f'''
<div class="feature" style="max-width:320px;">
  <img src="{args.img}" alt="{args.title}">
  <h3>{args.title}</h3>
  <p>{args.desc}</p>
  <a href="{args.afflink}" class="cta-btn" style="font-size:1rem;" target="_blank">Buy Now</a>
  {{readmore_btn}}
</div>
'''

POST_FILENAME = None
readmore_btn = ''
if args.review:
    # Create a new HTML file for the post
    safe_title = args.title.lower().replace(' ', '-').replace('/', '-')[:40]
    date_str = datetime.datetime.now().strftime('%Y%m%d')
    POST_FILENAME = f'post-{date_str}-{safe_title}.html'
    with open(POST_FILENAME, 'w', encoding='utf-8') as f:
        f.write(args.review)
    readmore_btn = f'<a href="{POST_FILENAME}" class="cta-btn readmore-btn" style="font-size:1rem;">Read More</a>'

# Insert card at the top of the EN section in ai-recommends.html
with open('ai-recommends.html', 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f, 'html.parser')

# Find EN section
en_section = soup.find(id='recs-en')
features_div = en_section.find('div', class_='features')
if not features_div:
    # Create if not exists
    features_div = soup.new_tag('div', **{'class': 'features', 'style': 'flex-wrap:wrap;gap:2rem;'})
    en_section.append(features_div)

# Insert new card at the top
card_html = BeautifulSoup(CARD_TEMPLATE.replace('{readmore_btn}', readmore_btn), 'html.parser')
features_div.insert(0, card_html)

with open('ai-recommends.html', 'w', encoding='utf-8') as f:
    f.write(str(soup))

print(f'Post published! {args.title}')
if POST_FILENAME:
    print(f'Full review: {POST_FILENAME}') 