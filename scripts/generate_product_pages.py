#!/usr/bin/env python3
"""
Product Page Generator for Janis Flow
Generates standalone product detail pages with basket/quotation system
CSV Source: products.csv
"""

import csv
import os
import json
from pathlib import Path
from datetime import datetime

def slugify(name):
    """Convert product name to URL-friendly slug"""
    return name.lower().replace(' ', '-').replace('.', '').replace(',', '').replace('"', '')

def parse_csv_list(value):
    """Parse comma-separated values from CSV"""
    if not value or value == '':
        return []
    return [item.strip() for item in value.split(',')]

def parse_color_swatches(colors_str, hex_str):
    """Parse colors and hex codes into array of objects"""
    colors = parse_csv_list(colors_str)
    hexes = parse_csv_list(hex_str)
    
    # If hex codes provided, use them; otherwise generate from color names
    if len(hexes) == len(colors) and hexes:
        return [{'name': colors[i], 'hex': hexes[i]} for i in range(len(colors))]
    else:
        # Default color mapping
        default_colors = {
            'Natural Wood': '#D2B48C',
            'Black': '#000000',
            'White': '#FFFFFF',
            'Green': '#4CAF50',
            'Red': '#F44336',
            'Blue': '#2196F3',
            'Yellow': '#FFEB3B'
        }
        return [{'name': c, 'hex': default_colors.get(c, '#CCCCCC')} for c in colors]

def generate_product_page(product, lang='en'):
    """Generate complete product detail HTML with basket system"""
    
    # Language-specific content
    if lang == 'th':
        name = product.get('name_th', product['name'])
        description = product.get('full_description_th', product['full_description'])
        lang_prefix = '/th'
        lang_dir = 'th/'
        stock_labels = {
            'In Stock': 'มีสินค้า',
            'Low Stock': 'สินค้าใกล้หมด',
            'Out of Stock': 'สินค้าหมด',
            'Pre-order': 'สั่งจองล่วงหน้า'
        }
        stock_status_text = stock_labels.get(product['stock_status'], product['stock_status'])
    else:
        name = product['name']
        description = product['full_description']
        lang_prefix = ''
        lang_dir = ''
        stock_status_text = product['stock_status']
    
    # Parse data
    gallery_images = parse_csv_list(product.get('gallery_images', product['main_image']))
    colors_data = parse_color_swatches(
        product.get('colors', ''),
        product.get('color_hex', '')
    )
    sizes = parse_csv_list(product.get('options', ''))
    features = parse_csv_list(product.get('feature_details', ''))
    
    # Get first color and size as default
    default_color = colors_data[0]['name'] if colors_data else 'Default'
    default_size = sizes[0] if sizes else 'Standard'
    
    # Stock status class
    stock_class = {
        'In Stock': 'in-stock',
        'Low Stock': 'low-stock',
        'Out of Stock': 'out-stock',
        'Pre-order': 'pre-order'
    }.get(product['stock_status'], 'in-stock')
    
    # Build HTML
    html = f'''<!DOCTYPE html>
<html lang="{lang}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=yes">
    <title>{name} | Janis Flow</title>
    
    <!-- SEO -->
    <meta name="description" content="{description[:150]}">
    <meta property="og:title" content="{name}">
    <meta property="og:description" content="{description[:150]}">
    <meta property="og:image" content="{product['main_image']}">
    <meta property="og:url" content="https://flow.janishammer.com{lang_prefix}/product/{slugify(product['name'])}.html">
    
    <!-- Font Awesome -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    
    <!-- Google Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Inter', sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            min-height: 100vh;
            padding: 1rem;
        }}
        
        /* Floating Cart Button */
        .cart-floating {{
            position: fixed;
            bottom: 2rem;
            right: 2rem;
            background: linear-gradient(135deg, #D4E157, #AED581);
            width: 60px;
            height: 60px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            box-shadow: 0 8px 20px rgba(0,0,0,0.2);
            transition: all 0.3s ease;
            z-index: 1000;
            border: 2px solid rgba(255,255,255,0.3);
        }}
        
        .cart-floating:hover {{
            transform: scale(1.1);
            box-shadow: 0 12px 30px rgba(0,0,0,0.3);
        }}
        
        .cart-floating i {{
            font-size: 1.5rem;
            color: #33691E;
        }}
        
        .cart-count {{
            position: absolute;
            top: -5px;
            right: -5px;
            background: #F44336;
            color: white;
            border-radius: 50%;
            width: 24px;
            height: 24px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 0.75rem;
            font-weight: bold;
        }}
        
        /* Main Container */
        .product-container {{
            max-width: 1280px;
            margin: 0 auto;
            background: rgba(255,255,255,0.95);
            border-radius: 32px;
            overflow: hidden;
            box-shadow: 0 25px 50px -12px rgba(0,0,0,0.25);
        }}
        
        /* Product Detail Section */
        .product-detail {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 2rem;
            padding: 2rem;
            background: white;
        }}
        
        /* LEFT COLUMN - GALLERY */
        .product-gallery {{
            position: relative;
        }}
        
        .main-image-container {{
            position: relative;
            cursor: pointer;
            overflow: hidden;
            border-radius: 24px;
            background: #f8f9fa;
            aspect-ratio: 1 / 1;
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        }}
        
        .main-image {{
            width: 100%;
            height: 100%;
            object-fit: contain;
            transition: transform 0.4s ease;
        }}
        
        .main-image-container:hover .main-image {{
            transform: scale(1.05);
        }}
        
        .zoom-icon {{
            position: absolute;
            bottom: 1rem;
            right: 1rem;
            background: rgba(0,0,0,0.7);
            color: white;
            width: 40px;
            height: 40px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            transition: all 0.3s ease;
            backdrop-filter: blur(5px);
        }}
        
        .zoom-icon:hover {{
            background: #D4E157;
            color: #33691E;
            transform: scale(1.1);
        }}
        
        /* Thumbnail Gallery */
        .thumbnail-gallery {{
            display: flex;
            gap: 0.75rem;
            margin-top: 1rem;
            overflow-x: auto;
            padding-bottom: 0.5rem;
        }}
        
        .thumbnail {{
            width: 70px;
            height: 70px;
            border-radius: 16px;
            cursor: pointer;
            transition: all 0.3s ease;
            border: 3px solid transparent;
            object-fit: cover;
            flex-shrink: 0;
        }}
        
        .thumbnail:hover {{
            transform: translateY(-4px);
            border-color: #D4E157;
        }}
        
        .thumbnail.active {{
            border-color: #D4E157;
            box-shadow: 0 4px 12px rgba(212,225,87,0.3);
        }}
        
        /* RIGHT COLUMN - INFO */
        .product-info {{
            display: flex;
            flex-direction: column;
            gap: 1rem;
        }}
        
        .product-category {{
            display: inline-block;
            background: rgba(212,225,87,0.2);
            color: #33691E;
            padding: 0.4rem 1rem;
            border-radius: 40px;
            font-size: 0.85rem;
            font-weight: 600;
            width: fit-content;
        }}
        
        .product-name {{
            font-size: 2rem;
            font-weight: 800;
            color: #1a1a2e;
            line-height: 1.2;
        }}
        
        .product-brand {{
            font-size: 0.9rem;
            color: #666;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }}
        
        .product-brand i {{
            color: #D4E157;
        }}
        
        .product-price {{
            font-size: 2.2rem;
            font-weight: 800;
            color: #D4E157;
            margin: 0.25rem 0;
        }}
        
        .product-price::before {{
            content: "฿";
            font-size: 1.6rem;
        }}
        
        /* Stock Status */
        .stock-status {{
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            padding: 0.5rem 1rem;
            border-radius: 40px;
            font-weight: 600;
            font-size: 0.85rem;
            width: fit-content;
        }}
        
        .stock-status.in-stock {{
            background: rgba(76,175,80,0.1);
            color: #4CAF50;
            border: 1px solid rgba(76,175,80,0.3);
        }}
        
        .stock-status.low-stock {{
            background: rgba(255,152,0,0.1);
            color: #FF9800;
            border: 1px solid rgba(255,152,0,0.3);
        }}
        
        .stock-status.out-stock {{
            background: rgba(244,67,54,0.1);
            color: #F44336;
            border: 1px solid rgba(244,67,54,0.3);
        }}
        
        .stock-status.pre-order {{
            background: rgba(33,150,243,0.1);
            color: #2196F3;
            border: 1px solid rgba(33,150,243,0.3);
        }}
        
        /* Features */
        .features-section h3 {{
            font-size: 1rem;
            color: #1a1a2e;
            margin-bottom: 0.75rem;
            font-weight: 700;
        }}
        
        .features-list {{
            list-style: none;
            display: flex;
            flex-direction: column;
            gap: 0.5rem;
        }}
        
        .features-list li {{
            display: flex;
            align-items: center;
            gap: 0.75rem;
            color: #555;
            font-size: 0.85rem;
        }}
        
        .features-list li i {{
            color: #D4E157;
            font-size: 0.9rem;
            width: 20px;
        }}
        
        /* Color Options */
        .color-options, .size-options {{
            margin: 0.5rem 0;
        }}
        
        .color-options h3, .size-options h3 {{
            font-size: 0.9rem;
            color: #1a1a2e;
            margin-bottom: 0.5rem;
            font-weight: 600;
        }}
        
        .color-swatches {{
            display: flex;
            gap: 0.5rem;
            flex-wrap: wrap;
        }}
        
        .color-swatch {{
            width: 40px;
            height: 40px;
            border-radius: 50%;
            cursor: pointer;
            transition: all 0.3s ease;
            border: 3px solid transparent;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        
        .color-swatch:hover {{
            transform: scale(1.1);
        }}
        
        .color-swatch.selected {{
            border-color: #D4E157;
            transform: scale(1.1);
            box-shadow: 0 0 0 2px white, 0 0 0 4px #D4E157;
        }}
        
        .size-buttons {{
            display: flex;
            gap: 0.5rem;
            flex-wrap: wrap;
        }}
        
        .size-btn {{
            background: #f0f0f0;
            border: 2px solid #e0e0e0;
            padding: 0.5rem 1rem;
            border-radius: 40px;
            cursor: pointer;
            transition: all 0.3s ease;
            font-weight: 500;
            font-size: 0.85rem;
            color: #666;
        }}
        
        .size-btn:hover {{
            background: #D4E157;
            border-color: #D4E157;
            color: #33691E;
        }}
        
        .size-btn.selected {{
            background: #D4E157;
            border-color: #D4E157;
            color: #33691E;
            font-weight: 700;
        }}
        
        /* Quantity Selector */
        .quantity-selector {{
            margin: 0.5rem 0;
        }}
        
        .quantity-selector h3 {{
            font-size: 0.9rem;
            color: #1a1a2e;
            margin-bottom: 0.5rem;
            font-weight: 600;
        }}
        
        .quantity-control {{
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }}
        
        .qty-btn {{
            width: 36px;
            height: 36px;
            border-radius: 12px;
            background: #f0f0f0;
            border: 1px solid #e0e0e0;
            cursor: pointer;
            font-size: 1.2rem;
            font-weight: bold;
            transition: all 0.2s;
        }}
        
        .qty-btn:hover {{
            background: #D4E157;
            border-color: #D4E157;
        }}
        
        .quantity-input {{
            width: 60px;
            height: 36px;
            text-align: center;
            border: 1px solid #e0e0e0;
            border-radius: 12px;
            font-size: 1rem;
            font-weight: 600;
        }}
        
        /* Action Buttons */
        .action-buttons {{
            display: flex;
            gap: 0.75rem;
            margin-top: 0.5rem;
        }}
        
        .btn-add-to-cart {{
            flex: 2;
            background: linear-gradient(135deg, #D4E157, #AED581);
            color: #33691E;
            border: none;
            padding: 0.8rem;
            border-radius: 60px;
            font-weight: 700;
            font-size: 0.9rem;
            cursor: pointer;
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 0.5rem;
        }}
        
        .btn-add-to-cart:hover {{
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(212,225,87,0.3);
        }}
        
        .btn-wishlist {{
            background: rgba(0,0,0,0.05);
            border: 2px solid #e0e0e0;
            padding: 0.8rem;
            border-radius: 60px;
            cursor: pointer;
            transition: all 0.3s ease;
            color: #666;
            aspect-ratio: 1;
        }}
        
        .btn-wishlist:hover {{
            background: rgba(212,225,87,0.1);
            border-color: #D4E157;
            color: #D4E157;
        }}
        
        /* YOU MAY LIKE SECTION */
        .you-may-like {{
            background: #f8f9fa;
            padding: 2rem;
            border-top: 1px solid #e0e0e0;
        }}
        
        .you-may-like h2 {{
            font-size: 1.5rem;
            color: #1a1a2e;
            margin-bottom: 1.5rem;
            font-weight: 700;
        }}
        
        .slider-track {{
            display: flex;
            gap: 1rem;
            overflow-x: auto;
            scroll-behavior: smooth;
            padding-bottom: 1rem;
        }}
        
        .slider-track::-webkit-scrollbar {{
            height: 6px;
        }}
        
        .slider-track::-webkit-scrollbar-track {{
            background: #e0e0e0;
            border-radius: 10px;
        }}
        
        .slider-track::-webkit-scrollbar-thumb {{
            background: #D4E157;
            border-radius: 10px;
        }}
        
        .recommend-card {{
            flex: 0 0 calc(25% - 0.75rem);
            min-width: 200px;
            background: white;
            border-radius: 20px;
            overflow: hidden;
            transition: all 0.4s ease;
            cursor: pointer;
            box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        }}
        
        .recommend-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 15px 30px rgba(0,0,0,0.15);
        }}
        
        .recommend-card-image {{
            width: 100%;
            aspect-ratio: 1 / 1;
            object-fit: cover;
        }}
        
        .recommend-card-info {{
            padding: 0.75rem;
        }}
        
        .recommend-card-name {{
            font-size: 0.9rem;
            font-weight: 700;
            color: #33691E;
            margin-bottom: 0.25rem;
        }}
        
        .recommend-card-price {{
            font-size: 1rem;
            font-weight: 800;
            color: #D4E157;
        }}
        
        .recommend-card-price::before {{
            content: "฿";
            font-size: 0.8rem;
        }}
        
        .slider-nav {{
            display: flex;
            justify-content: center;
            gap: 0.5rem;
            margin-top: 1rem;
        }}
        
        .nav-btn {{
            width: 36px;
            height: 36px;
            border-radius: 50%;
            background: white;
            border: 1px solid #e0e0e0;
            cursor: pointer;
            transition: all 0.3s;
        }}
        
        .nav-btn:hover {{
            background: #D4E157;
            border-color: #D4E157;
        }}
        
        /* Cart Modal */
        .cart-modal {{
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.8);
            z-index: 10001;
            justify-content: center;
            align-items: center;
        }}
        
        .cart-modal.active {{
            display: flex;
        }}
        
        .cart-content {{
            max-width: 600px;
            width: 90%;
            max-height: 80vh;
            background: white;
            border-radius: 32px;
            overflow: hidden;
            display: flex;
            flex-direction: column;
        }}
        
        .cart-header {{
            padding: 1.5rem;
            background: linear-gradient(135deg, #D4E157, #AED581);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        
        .cart-header h2 {{
            color: #33691E;
            font-size: 1.3rem;
        }}
        
        .cart-close {{
            font-size: 1.5rem;
            cursor: pointer;
            color: #33691E;
        }}
        
        .cart-items {{
            flex: 1;
            overflow-y: auto;
            padding: 1rem;
        }}
        
        .cart-item {{
            display: flex;
            gap: 1rem;
            padding: 1rem;
            border-bottom: 1px solid #e0e0e0;
        }}
        
        .cart-item-image {{
            width: 70px;
            height: 70px;
            object-fit: cover;
            border-radius: 12px;
        }}
        
        .cart-item-details {{
            flex: 1;
        }}
        
        .cart-item-name {{
            font-weight: 700;
            color: #33691E;
            margin-bottom: 0.25rem;
        }}
        
        .cart-item-variant {{
            font-size: 0.75rem;
            color: #888;
        }}
        
        .cart-item-price {{
            color: #D4E157;
            font-weight: 700;
        }}
        
        .cart-item-actions {{
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }}
        
        .cart-qty-btn {{
            width: 28px;
            height: 28px;
            border-radius: 8px;
            background: #f0f0f0;
            border: none;
            cursor: pointer;
        }}
        
        .cart-item-qty {{
            width: 40px;
            text-align: center;
        }}
        
        .cart-item-remove {{
            color: #F44336;
            cursor: pointer;
            font-size: 1.2rem;
        }}
        
        .cart-summary {{
            padding: 1.5rem;
            background: #f8f9fa;
            border-top: 2px solid #e0e0e0;
        }}
        
        .cart-total {{
            display: flex;
            justify-content: space-between;
            font-size: 1.2rem;
            font-weight: 800;
            margin-bottom: 1rem;
        }}
        
        .btn-quotation {{
            width: 100%;
            background: linear-gradient(135deg, #D4E157, #AED581);
            color: #33691E;
            border: none;
            padding: 1rem;
            border-radius: 60px;
            font-weight: 800;
            font-size: 1rem;
            cursor: pointer;
            transition: all 0.3s;
        }}
        
        .btn-quotation:hover {{
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(212,225,87,0.3);
        }}
        
        /* Toast */
        .toast {{
            position: fixed;
            bottom: 2rem;
            left: 50%;
            transform: translateX(-50%) translateY(100px);
            background: #4CAF50;
            color: white;
            padding: 0.8rem 1.5rem;
            border-radius: 60px;
            font-weight: 600;
            z-index: 10002;
            transition: transform 0.3s;
            white-space: nowrap;
        }}
        
        .toast.show {{
            transform: translateX(-50%) translateY(0);
        }}
        
        /* Lightbox */
        .lightbox {{
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.95);
            z-index: 10000;
            justify-content: center;
            align-items: center;
        }}
        
        .lightbox.active {{
            display: flex;
        }}
        
        .lightbox-img {{
            max-width: 90%;
            max-height: 90%;
            object-fit: contain;
        }}
        
        .lightbox-close {{
            position: absolute;
            top: 20px;
            right: 30px;
            color: white;
            font-size: 40px;
            cursor: pointer;
        }}
        
        /* Responsive */
        @media (max-width: 768px) {{
            body {{
                padding: 0.5rem;
            }}
            
            .product-detail {{
                grid-template-columns: 1fr;
                gap: 1rem;
                padding: 1rem;
            }}
            
            .product-name {{
                font-size: 1.5rem;
            }}
            
            .product-price {{
                font-size: 1.8rem;
            }}
            
            .you-may-like {{
                padding: 1rem;
            }}
            
            .recommend-card {{
                flex: 0 0 calc(50% - 0.5rem);
            }}
            
            .action-buttons {{
                flex-direction: column;
            }}
            
            .btn-wishlist {{
                aspect-ratio: auto;
                padding: 0.8rem;
            }}
            
            .cart-floating {{
                bottom: 1rem;
                right: 1rem;
                width: 50px;
                height: 50px;
            }}
        }}
        
        @media (max-width: 480px) {{
            .recommend-card {{
                flex: 0 0 100%;
            }}
        }}
    </style>
</head>
<body>
    <!-- Floating Cart Button -->
    <div class="cart-floating" id="cartFloating">
        <i class="fas fa-shopping-bag"></i>
        <span class="cart-count" id="cartCount">0</span>
    </div>
    
    <div class="product-container">
        <!-- PRODUCT DETAIL SECTION -->
        <div class="product-detail">
            <!-- LEFT: Gallery -->
            <div class="product-gallery">
                <div class="main-image-container" id="mainImageContainer">
                    <img src="{product['main_image']}" alt="{name}" class="main-image" id="mainImage">
                    <div class="zoom-icon" id="zoomIcon">
                        <i class="fas fa-expand"></i>
                    </div>
                </div>
                
                <div class="thumbnail-gallery" id="thumbnailGallery">
                    {self.generate_thumbnails(gallery_images, product['main_image'])}
                </div>
            </div>
            
            <!-- RIGHT: Product Info -->
            <div class="product-info">
                <div>
                    <span class="product-category">{product['category']}</span>
                </div>
                
                <h1 class="product-name">{name}</h1>
                
                <div class="product-brand">
                    <i class="fas fa-tag"></i>
                    <span>{product['brand']} · {product.get('collection', 'Limited Edition')}</span>
                </div>
                
                <div class="product-price">{int(product['price']):,}</div>
                
                <div class="stock-status {stock_class}">
                    <i class="fas fa-{'check-circle' if product['stock_status'] == 'In Stock' else 'clock' if product['stock_status'] == 'Pre-order' else 'exclamation-circle'}"></i>
                    <span>{stock_status_text}</span>
                </div>
                
                <!-- Features -->
                <div class="features-section">
                    <h3>Key Features</h3>
                    <ul class="features-list">
                        {self.generate_features(features)}
                    </ul>
                </div>
                
                <!-- Color Options -->
                {self.generate_color_options(colors_data)}
                
                <!-- Size Options -->
                {self.generate_size_options(sizes)}
                
                <!-- Quantity Selector -->
                <div class="quantity-selector">
                    <h3>Quantity</h3>
                    <div class="quantity-control">
                        <button class="qty-btn" onclick="updateQuantity(-1)">-</button>
                        <input type="number" id="quantity" class="quantity-input" value="1" min="1" max="99" readonly>
                        <button class="qty-btn" onclick="updateQuantity(1)">+</button>
                    </div>
                </div>
                
                <!-- Action Buttons -->
                <div class="action-buttons">
                    <button class="btn-add-to-cart" onclick="addToCart()">
                        <i class="fas fa-shopping-cart"></i>
                        Add to Cart
                    </button>
                    <button class="btn-wishlist" onclick="toggleWishlist(this)">
                        <i class="far fa-heart"></i>
                    </button>
                </div>
            </div>
        </div>
        
        <!-- YOU MAY LIKE SECTION (will be populated by JavaScript) -->
        <div class="you-may-like">
            <h2>✨ You May Also Like</h2>
            <div class="slider-track" id="sliderTrack"></div>
            <div class="slider-nav">
                <button class="nav-btn" onclick="scrollSlider(-1)"><i class="fas fa-chevron-left"></i></button>
                <button class="nav-btn" onclick="scrollSlider(1)"><i class="fas fa-chevron-right"></i></button>
            </div>
        </div>
    </div>
    
    <!-- CART MODAL -->
    <div id="cartModal" class="cart-modal">
        <div class="cart-content">
            <div class="cart-header">
                <h2><i class="fas fa-shopping-bag"></i> Your Cart</h2>
                <span class="cart-close" onclick="closeCart()">&times;</span>
            </div>
            <div class="cart-items" id="cartItems">
                <div style="text-align: center; padding: 2rem; color: #888;">
                    Your cart is empty
                </div>
            </div>
            <div class="cart-summary">
                <div class="cart-total">
                    <span>Total</span>
                    <span id="cartTotal">฿0</span>
                </div>
                <button class="btn-quotation" onclick="requestQuotation()">
                    <i class="fas fa-file-invoice"></i> Get Your Quotation
                </button>
            </div>
        </div>
    </div>
    
    <!-- QUOTATION MODAL -->
    <div id="quotationModal" class="cart-modal">
        <div class="cart-content" style="max-width: 500px;">
            <div class="cart-header">
                <h2><i class="fas fa-check-circle"></i> Quotation Request</h2>
                <span class="cart-close" onclick="closeQuotationModal()">&times;</span>
            </div>
            <div style="padding: 2rem; text-align: center;">
                <i class="fas fa-envelope" style="font-size: 3rem; color: #D4E157; margin-bottom: 1rem;"></i>
                <h3 style="color: #33691E; margin-bottom: 0.5rem;">Thank You!</h3>
                <p style="color: #666; margin-bottom: 1rem;">We've received your quotation request.</p>
                <p style="color: #888; font-size: 0.9rem;">Our team will contact you within 24 hours with your quotation details.</p>
                <button class="btn-quotation" style="margin-top: 1.5rem;" onclick="closeQuotationModal()">
                    Continue Shopping
                </button>
            </div>
        </div>
    </div>
    
    <!-- LIGHTBOX -->
    <div id="lightbox" class="lightbox" onclick="closeLightbox()">
        <span class="lightbox-close">&times;</span>
        <img class="lightbox-img" id="lightboxImg">
    </div>
    
    <!-- TOAST -->
    <div id="toast" class="toast"></div>
    
    <script>
        // Product Data
        const currentProduct = {{
            id: {product['id']},
            name: "{name}",
            brand: "{product['brand']}",
            price: {product['price']},
            image: "{product['main_image']}",
            colors: {json.dumps([c['name'] for c in colors_data])},
            sizes: {json.dumps(sizes)},
            defaultColor: "{default_color}",
            defaultSize: "{default_size}"
        }};
        
        // Current selections
        let currentColor = currentProduct.defaultColor;
        let currentSize = currentProduct.defaultSize;
        let currentQuantity = 1;
        
        // Cart Data
        let cart = JSON.parse(localStorage.getItem('flowCart')) || [];
        
        // Update cart UI
        function updateCartUI() {{
            const cartCount = cart.reduce((sum, item) => sum + item.quantity, 0);
            document.getElementById('cartCount').innerText = cartCount;
            localStorage.setItem('flowCart', JSON.stringify(cart));
            renderCartItems();
        }}
        
        // Render cart items
        function renderCartItems() {{
            const container = document.getElementById('cartItems');
            const cartTotal = document.getElementById('cartTotal');
            
            if (cart.length === 0) {{
                container.innerHTML = '<div style="text-align: center; padding: 2rem; color: #888;">Your cart is empty</div>';
                cartTotal.innerText = '฿0';
                return;
            }}
            
            let total = 0;
            container.innerHTML = cart.map((item, index) => {{
                const itemTotal = item.price * item.quantity;
                total += itemTotal;
                return `
                    <div class="cart-item">
                        <img src="${{item.image}}" class="cart-item-image">
                        <div class="cart-item-details">
                            <div class="cart-item-name">${{item.name}}</div>
                            <div class="cart-item-variant">${{item.color || 'Default'}} · ${{item.size || 'Standard'}}</div>
                            <div class="cart-item-price">฿${{item.price.toLocaleString()}}</div>
                        </div>
                        <div class="cart-item-actions">
                            <button class="cart-qty-btn" onclick="updateCartItem(${{index}}, -1)">-</button>
                            <span class="cart-item-qty">${{item.quantity}}</span>
                            <button class="cart-qty-btn" onclick="updateCartItem(${{index}}, 1)">+</button>
                            <i class="fas fa-trash-alt cart-item-remove" onclick="removeCartItem(${{index}})"></i>
                        </div>
                    </div>
                `;
            }}).join('');
            
            cartTotal.innerText = `
