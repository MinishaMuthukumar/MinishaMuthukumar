from bs4 import BeautifulSoup
import pandas as pd

# Read the HTML file
with open("Amazon.html", "r", encoding="utf-8") as file:
    content = file.read()

# Parse the HTML with BeautifulSoup
soup = BeautifulSoup(content, "html.parser")

# Initialize lists to store product details
product_names = []  # List to store product names
product_prices = []  # List to store product prices
product_reviews = []  # List to store product reviews

# Find all divs with class="a-section"
divs = soup.find_all('div', class_="a-section")

# Iterate over the divs to extract product name, price, and reviews
for div in divs:
    try:
        # Find the product name (correct: access .text attribute)
        name_span = div.find('span', class_="a-size-medium a-color-base a-text-normal")
        product_name = name_span.text.strip() if name_span else " "
    except:
        product_name = " "
    
    try:
        # Find the product price (correct: access .text attribute)
        price_span = div.find('span', class_="a-offscreen")
        product_price = price_span.text.strip() if price_span else " "
    except:
        product_price = " "
    
    try:
        # Find the product reviews (correct: access .text attribute)
        reviews_span = div.find('span', class_="a-size-base s-underline-text")
        product_review = reviews_span.text.strip() if reviews_span else " "
    except:
        product_review = " "
    
    # Append the extracted details to the lists
    product_names.append(product_name)
    product_prices.append(product_price)
    product_reviews.append(product_review)

# Create a DataFrame to store the results
df = pd.DataFrame({
    'Product_Name': product_names,
    'Product_Price': product_prices,
    'Product_Reviews': product_reviews
})

# Specify a file path for the Excel file
output_path = "amazon_products.xlsx"  # You can change this to a specific path

# Write the DataFrame to an Excel file
df.to_excel(output_path, index=False)

print(f"Excel file has been created: {output_path}")
