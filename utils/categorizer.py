# Dictionary of keywords for each category
CATEGORY_KEYWORDS = {
    'Food': ['food', 'fruit', 'vegetable', 'snack', 'restaurant', 'cafe', 'coffee', 'grocery', 'supermarket', 'dining', 'takeout', 'lunch', 'dinner', 'breakfast', 'snack'],
    'Transportation': ['gas', 'fuel', 'uber', 'lyft', 'taxi', 'transit', 'bus', 'train', 'subway', 'parking', 'toll'],
    'Housing': ['rent', 'mortgage', 'repair', 'maintenance', 'furniture', 'appliance'],
    'Utilities': ['electricity', 'water', 'gas', 'internet', 'phone', 'cable', 'utility'],
    'Entertainment': ['movie', 'theater', 'concert', 'sport', 'game', 'netflix', 'spotify', 'amazon prime', 'hulu', 'disney+', 'apple tv+', 'amazon music', 'apple music', 'spotify music', 'youtube music'],
    'Shopping': ['clothes', 'shoes', 'accessories', 'store', 'shop', 'mall', 'amazon'],
    'Healthcare': ['doctor', 'pharmacy', 'medicine', 'hospital', 'medical', 'health', 'dental'],
    'Education': ['school', 'university', 'college', 'course', 'book', 'textbook', 'education', 'learning'],
    'Savings':['investments', 'stocks', 'TFSA', 'RESP', 'insurance', 'retirement']
}

def suggest_category(description):
    """
    Analyze description and suggest a category based on keywords.
    Returns a tuple of (category, confidence_score)
    """
    description = description.lower()
    max_matches = 0
    suggested_category = 'Other'
    
    for category, keywords in CATEGORY_KEYWORDS.items():
        matches = sum(1 for keyword in keywords if keyword in description)
        if matches > max_matches:
            max_matches = matches
            suggested_category = category
    
    # Calculate confidence score (0-1)
    confidence = min(max_matches / 3, 1.0)  # Cap at 3 matches for 100% confidence
    
    return suggested_category, confidence 