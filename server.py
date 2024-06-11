from flask import Flask, render_template, request, jsonify
from markupsafe import Markup, escape
import re

app = Flask(__name__)

def highlight(text, query):
    """Highlight instances of query in text, ignoring case, with special handling for dollar sign"""
    if not query:
        return escape(text)

    text_escaped = escape(text)
    query_escaped = escape(query)

    if query_escaped == "$":
        # Use regex to replace only the first $ in any sequence of $ with highlighted version
        highlighted_text = re.sub(r'\$', Markup('<mark>$</mark>'), text_escaped, count=1)
    else:
        # Create a regex pattern for the query, ignoring case
        pattern = re.compile(re.escape(query_escaped), re.IGNORECASE)

        # Function to replace matched query with highlighted version
        def replacer(match):
            return Markup('<mark>') + match.group() + Markup('</mark>')

        highlighted_text = pattern.sub(replacer, text_escaped)

    return Markup(highlighted_text)

app.jinja_env.filters['highlight'] = highlight


def format_key(key):
    """Convert a snake_case string to Title Case"""
    return ' '.join(word.capitalize() for word in key.split('_'))

cafes = {
    "1": {
        "name": "Blue Bottle Coffee",
        "image": "https://lh3.googleusercontent.com/p/AF1QipPrz8Jr0fntkC-7Iw8ljH_A1dDDNpnQRPuzwv1P=s1360-w1360-h1020",
        "neighbourhood": "Columbia University",
        "address": "2901 Broadway, New York, NY, 10025",
        "summary": "A trendy cafe chain known for its upscale coffee drinks and freshly baked pastries. They offer a "
                   "selection of premium beans and brewing equipment for coffee aficionados. Each location provides a "
                   "minimalist and inviting atmosphere, perfect for enjoying a high-quality coffee experience. "
                   "Renowned for its commitment to freshness and sustainability, Blue Bottle is a favorite among "
                   "discerning coffee lovers",
        "price_range": "$$",
        "stars": 5,
        "menu_highlights": ["New Orleans-style Iced Coffee", "Drip Coffee", "Matcha Latte", "Pour Over"],
        "amenities": ["Wi-Fi", "Restroom", "Indoor Seating", "Outdoor Seating", "Quiet"],
        "similar_cafes": ["5", "6", "7", "10"]
    },
    "2": {
        "name": "Blank Street Coffee",
        "image": "https://lh3.googleusercontent.com/p/AF1QipPh0-0Bqob2FkwFB2e6jGzEo7jdOzzI22yP56Q=s1360-w1360-h1020",
        "neighbourhood": "Upper West Side",
        "address": "2345 Broadway, New York, NY, 10024",
        "summary": "We’re a small-format coffee shop built around the idea that great coffee should be affordable "
                   "enough to be part of your every day. Find us on Broadway between W 85th and 86th next to Bravo "
                   "West Pizza! Can’t wait to meet you.",
        "price_range": "$",
        "stars": 3,
        "menu_highlights": ["Iced Latte", "Iced Pistachio Latte", "Iced Matcha Latte", "Chocolate Croissant"],
        "amenities": ["Quiet", "Indoor seating", "Pet-Friendly area"],
        "similar_cafes": ["3", "4"]
    },
    "3": {
        "name": "Daily Provisions - Upper West Side",
        "image": "https://lh5.googleusercontent.com/p/AF1QipMPn8PJEYEZvA7rfIPX4MXZ2-FbYiVH5jjUgiSH=w260-h175-n-k-no",
        "neighbourhood": "Upper West Side",
        "address": "375 Amsterdam Avenue, New York, NY 10024",
        "summary": "Daily Provisions is your neighborhood kitchen, serving breakfast, lunch, and dinner from Danny "
                   "Meyer’s Union Square Hospitality Group. With pick-up, delivery, and in restaurant dining, "
                   "we are sure to add a smile to your day. Located in the Upper West Side, we open early in the "
                   "morning with fresh baked goods and breakfast sandwiches. Throughout the afternoon and evening, "
                   "we offer made-to-order sandwiches, slow-roasted chicken, seasonal sides, and a selection of "
                   "cocktails, beer, and wine to toast the day.",
        "price_range": "$$",
        "stars": 4,
        "menu_highlights": ["Cold Brew", "Drip Coffee", "Matcha Latte", "Avocado Toast", "Chicken Milanese Sandwich", "Bacon, Egg & Cheese Sandwich"],
        "amenities": ["Restroom", "Wi-Fi", "Indoor Seating", "Outdoor Seating"],
        "similar_cafes": ["2", "4"]
    },
    "4": {
        "name": "Joe & The Juice",
        "image": "https://lh3.googleusercontent.com/p/AF1QipMqFB5cD0o_mfs_tk-rlNEnvTfwUWiRf8zFuMfP=s1360-w1360-h1020",
        "neighbourhood": "Midtown",
        "address": "1758 Broadway, New York, NY 10019",
        "summary": "Joe & The Juice is a Danish chain founded in 2002, known for its health-focused menu of coffee, "
                   "fresh juices, smoothies, and sandwiches. With a trendy, urban atmosphere, it caters to a young "
                   "demographic across its global locations in Europe, North America, Asia, and Australia. The brand "
                   "is celebrated for its modern interiors, vibrant music, and commitment to quality and convenience "
                   "in healthy eating and drinking.",
        "price_range": "$$",
        "stars": 4,
        "menu_highlights": ["Iced Vanilla Latte", "Latte", "Tunacado Sandwich", "Green Shield Juice"],
        "amenities": ["Restroom", "Free Wi-Fi", "Indoor Seating", "Outdoor Seating"],
        "similar_cafes": ["2", "3"]
    },
    "5": {
        "name": "Starbucks Reserve Roastery New York",
        "image": "https://images.ctfassets.net/1aemqu6a6t65/2S1AylczBMG8oZLr5km9jP/b247592a005a086ce79bf45ca48dff70/rw-to-go_starbucks-reserve-roastery_4d185b13-5056-a36f-23b56b111cb582e8-4d1859e55056a36_4d185b75-5056-a36f-23450747ab048c4d?q=72&w=1200&h=630&fit=fill",
        "neighbourhood": "Chelsea",
        "address": "61 9th Avenue, New York, NY 10011",
        "summary": "Starbucks Reserve in Chelsea, New York, represents an upscale experience from the global coffee "
                   "giant, offering a more premium and artisanal approach to coffee compared to its regular outlets. "
                   "Located in the vibrant neighborhood of Chelsea, this location showcases exclusive, "
                   "small-lot Starbucks Reserve coffees brewed through various methods, along with a menu of unique "
                   "beverages and food pairings. The interior boasts a stylish and sophisticated design, providing a "
                   "welcoming space for coffee enthusiasts to explore rare blends and learn about coffee culture from "
                   "skilled baristas. It's a destination for those seeking a high-end coffee experience in the heart "
                   "of New York City.",
        "price_range": "$$",
        "stars": 4,
        "menu_highlights": ["Pistachio Latte", "Espresso Martini", "Iced Latte Bali Blend", "Frappuccino", "Chocolate Croissant"],
        "amenities": ["Bar Onsite", "Restroom", "Indoor Seating", "Outdoor Seating", "Free Wi-Fi"],
        "similar_cafes": ["1", "6", "7", "10"]
    },
    "6": {
        "name": "Stumptown Coffee Roasters",
        "image": "https://photostorage.explorest.com/usa/new-york/jthomas-stump-compressed.jpg",
        "neighbourhood": "Greenwich Village",
        "address": "30 West 8th St., New York, NY 10011",
        "summary": "A prominent outpost of the Portland-based specialty coffee roaster known for its strong "
                   "commitment to quality, ethical sourcing, and expertly roasted beans. Situated in the historic and "
                   "culturally rich neighborhood of Greenwich Village, this café attracts both locals and visitors "
                   "with its cozy ambiance, knowledgeable baristas, and an exceptional selection of single-origin "
                   "coffees and blends. It's a favored spot for coffee lovers looking to enjoy high-quality brews in "
                   "a charming and inviting setting.",
        "price_range": "$$",
        "stars": 5,
        "menu_highlights": ["Pour-Over", "Latte", "Blueberry Muffin", "Espresso", "Ham and Cheese Croissant"],
        "amenities": ["Restrooms", "Free Wi-Fi", "Indoor Seating"],
        "similar_cafes": ["1", "5", "7", "10"]
    },
    "7": {
        "name": "787 Coffee",
        "image": "https://lh3.googleusercontent.com/p/AF1QipOTwLXsXIlomhvcJFKvRlQGxRr4q9SaZr8su4t3=s1360-w1360-h1020",
        "neighbourhood": "Chelsea",
        "address": "256 West 15th St., New York, NY, 10011",
        "summary": "A from farm go cup coffee experience. We grow, process and roast our own beans at our coffee farm "
                   "in Puerto Rico giving you the freshest cup of coffee. We have quick grab and go bites, "
                   "empanadas and pastries. Keto, gluten free pastries available Best coffee shop in NYC Come try the "
                   "freshest cup of coffee We recommend our wow drinks- dulce de leche latte, tres leches latte, "
                   "coquito latte, mazapan latte, horchata latte and our iced tamarind and hibiscus tea.",
        "price_range": "$$",
        "stars": 5,
        "menu_highlights": ["Rum-infused Coffee", "Cold Brew", "Cortado", "Chicken Empanadas", "Coquito"],
        "amenities": ["Restrooms", "Indoor Seating", "Outdoor Seating", "Quiet"],
        "similar_cafes": ["1", "5", "6", "10"]
    },
    "8": {
        "name": "Ralph's Coffee",
        "image": "https://cititour.com/NYC_Restaurants/photos/17082_Ralph's%20Coffee,%20Ralph%20Lauren,%20Flatiron,%20NYC%207.jpg",
        "neighbourhood": "Flatiron",
        "address": "160 5th Avenue, New York, NY 10010",
        "summary": "A chic coffee shop nestled within the Ralph Lauren store, offering a unique blend of fashion and "
                   "coffee culture. This elegantly designed café exudes the classic Ralph Lauren style, "
                   "combining green and white decor with a touch of old-world charm. It serves a selection of premium "
                   "coffees, teas, and light fare, making it a stylish spot for shoppers and coffee aficionados "
                   "alike. Located in the bustling Flatiron District, Ralph's Coffee provides a serene escape with "
                   "its warm ambiance and high-quality brews, embodying the luxurious lifestyle associated with the "
                   "Ralph Lauren brand.",
        "price_range": "$$",
        "stars": 4,
        "menu_highlights": ["Hot Chocolate", "Matcha Latte", "Croissant", "Vanilla Iced Latte"],
        "amenities": ["Free Wi-Fi", "Outdoor Seating", "Indoor Seating", "Quiet"],
        "similar_cafes": ["9"]
    },
    "9": {
        "name": "Joe Coffee",
        "image": "https://lh3.googleusercontent.com/p/AF1QipOMetArjkpOVclJn7p_B5KNe4i0woy6WDaOmsLr=s1360-w1360-h1020",
        "neighbourhood": "Midtown South",
        "address": "55 West 40th St., New York, NY 10018",
        "summary": "Renowned for its high-quality, sustainably sourced coffee, this café serves a variety of expertly "
                   "crafted espresso drinks, pour-overs, and house-made pastries in a cozy, inviting atmosphere. "
                   "Situated close to Bryant Park, it provides a perfect spot for locals and tourists alike to enjoy "
                   "a peaceful coffee break amidst the bustling city life. With its friendly baristas and commitment "
                   "to community and sustainability, Joe Coffee at Bryant Park has become a beloved destination for "
                   "coffee aficionados in the city.",
        "price_range": "$",
        "stars": 3,
        "menu_highlights": ["Latte", "Cappuccino", "Espresso", "Matcha Latte"],
        "amenities": ["Outdoor Seating"],
        "similar_cafes": ["8"]
    },
    "10": {
        "name": "Devoción",
        "image": "https://lh3.googleusercontent.com/p/AF1QipMGPmtdWdCzTM4KvpbgW6QeLbNDXwWH4aWiD5Pp=s1360-w1360-h1020",
        "neighbourhood": "Flatiron",
        "address": "25 East 20th St., New York, NY 10003",
        "summary": "A standout location of the renowned Colombian coffee roaster known for its commitment to "
                   "freshness and sustainability. This spacious, light-filled café boasts an eye-catching interior "
                   "featuring lush greenery and a welcoming atmosphere, creating a tranquil oasis for coffee lovers "
                   "in the heart of Manhattan. Devoción sources its beans directly from farms in Colombia and is "
                   "celebrated for offering some of the freshest coffee in the city, with beans often roasted just "
                   "days after being harvested. Visitors can enjoy a variety of single-origin coffees and espresso "
                   "drinks, prepared by skilled baristas, in an environment that emphasizes the beauty and "
                   "biodiversity of Colombia.",
        "price_range": "$$",
        "stars": 5,
        "menu_highlights": ["Pour Over", "Croissant", "Cortado", "Latte", "Cold Brew On Tap"],
        "amenities": ["Indoor Seating", "Free Wi-Fi", "Restroom"],
        "similar_cafes": ["1", "5", "6", "7"]
    }
}
popular_ids = ["1", "7", "10"]

@app.route('/')
def main():
    popular_cafes = {k: cafes[k] for k in popular_ids}
    return render_template('main.html', popular_cafes=popular_cafes)

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '').strip()

    if not query:
        return render_template('search.html', cafes={}, result_message="Enter a valid search query", query="")

    fields = ["name", "neighbourhood", "address", "price_range"]
    matching_cafes = {}
    for k, cafe in cafes.items():
        match_found = False
        for field in fields:
            # if field in ["menu_highlights", "amenities"]: # Fields that are lists
            #     if any(query.lower() in item.lower() for item in cafe[field]):
            #         match_found = True
            #         break
            # else: # Fields that are strings
            if query.lower() in cafe[field].lower():
                match_found = True
                break
        if match_found:
            matching_cafes[k] = cafe

    result_message = "No results found" if not matching_cafes else f'Showing Results for "{query}"'

    return render_template('search.html', cafes=matching_cafes, result_message=result_message, query=query)

@app.route('/view/<id>')
def view_item(id):
    item = cafes.get(id)
    if item:
        item['stars'] = int(item['stars'])
        return render_template('view_item.html', cafes=cafes, item=item, id=id)
    else:
        return "Item not found", 404

def is_valid_url(url):
    # Regular expression for validating a URL
    regex = re.compile(
        r'^(https?://)?'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return re.match(regex, url) is not None

@app.route('/add', methods=['GET', 'POST'])
def add_item():
    if request.method == 'POST':
        data = request.get_json()
        errors = {}
        new_cafe = {
            'name': data.get('name', '').strip(),
            'image': data.get('image_url', '').strip(),
            'neighbourhood': data.get('neighbourhood', '').strip(),
            'address': data.get('address', '').strip(),
            'summary': data.get('summary', '').strip(),
            'price_range': data.get('price_range', '').strip(),
            'stars': data.get('stars', ''),
            'menu_highlights': data.get('menu_highlights', []),
            'amenities': data.get('amenities', []),
            'similar_cafes': data.get('similar_cafes', [])
        }

        # Validate Image_URL to ensure it's a HRL
        if not is_valid_url(new_cafe['image']):
            errors['image'] = 'Image URL must be a valid URL'

        # Validate price_range to ensure it consists only of $s
        if not re.match(r'^\$+$', new_cafe['price_range']):
            errors['price_range'] = 'Price range must consist only of $ characters'

        # Fields expected to be lists
        list_fields = ['menu_highlights', 'amenities', 'similar_cafes']
        for field in list_fields:
            if not isinstance(new_cafe[field], list):
                errors[field] = f'{format(field)} must be a list'

        if errors:
            return jsonify({'success': False, 'errors': errors}), 400

        new_id = str(max([int(k) for k in cafes.keys()]) + 1)  # Calculate new unique ID

        # Perform any additional validations as needed
        cafes[new_id] = new_cafe

        return jsonify({'success': True, 'id': new_id})

    # For GET request, render the form template
    return render_template('add_item.html', cafes=cafes)

@app.route('/edit/<id>', methods=['GET', 'POST'])
def edit_item(id):
    item = cafes.get(id)

    if not item:
        return "Item not found", 404

    if request.method == 'GET':
        return render_template('edit_item.html', item=item, id=id, cafes=cafes)

    elif request.method == 'POST':
        data = request.get_json(force=True) if request.get_json() else {}
        errors = {}

        # Validate fields
        new_data = {
            'name': data.get('name', '').strip(),
            'image': data.get('image_url', '').strip(),
            'neighbourhood': data.get('neighbourhood', '').strip(),
            'address': data.get('address', '').strip(),
            'summary': data.get('summary', '').strip(),
            'price_range': data.get('price_range', '').strip(),
            'stars': data.get('stars', ''),
            'menu_highlights': data.get('menu_highlights', []),
            'amenities': data.get('amenities', []),
            'similar_cafes': data.get('similar_cafes', [])
        }

        if not is_valid_url(new_data['image']):
            errors['image'] = 'Image URL must be a valid URL'
        if not re.match(r'^\$+$', new_data['price_range']):
            errors['price_range'] = 'Price range must consist only of $ characters'
        try:
            if not 1 <= int(new_data['stars']) <= 5:
                errors['stars'] = 'Stars must be a value between 1 and 5'
        except ValueError:
            errors['stars'] = 'Stars must be a numeric value'

        if errors:
            return jsonify({'success': False, 'errors': errors}), 400

        # Update item
        cafes[id] = new_data

        return jsonify({'success': True, 'id': id}), 200

    # If not GET/POST request
    return "Method not allowed", 405



if __name__ == '__main__':
    app.run(debug=True)
