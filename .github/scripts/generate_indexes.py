import os
import glob
from pathlib import Path

def generate_recipe_card(recipe_path, images_path):
    filename = Path(recipe_path).stem
    title = filename.replace('-', ' ').title()
    image_path = f"../../images/{images_path}/{filename}.png"
    relative_path = os.path.basename(recipe_path)
    
    return f'''
        <a href="{relative_path}" class="recipe-card">
          <img src="{image_path}" alt="{title}">
          <h2>{title}</h2>
        </a>'''

def generate_category_section(category, emoji):
    return f'''
    <section class="category-section">
      <h2>{emoji} {category.title()}</h2>
      <div class="recipe-grid">
        {generate_category_cards(category)}
      </div>
    </section>
    '''

def generate_category_cards(category):
    recipes_path = f"recipes/{category}"
    recipes = glob.glob(f"{recipes_path}/*.html")
    recipes = [r for r in recipes if 'index.html' not in r]
    
    return '\n'.join(generate_recipe_card(recipe, category) for recipe in recipes)

def generate_homepage_cards():
    print("Starting homepage card generation...")
    recipes = []
    for category in ['pizza', 'eats', 'treats']:
        recipe_files = glob.glob(f"recipes/{category}/*.html")
        print(f"Found {len(recipe_files)} files in {category}/")
        recipes.extend([f for f in recipe_files if 'index.html' not in f])
    
    recipes.sort(key=lambda x: os.path.getmtime(x), reverse=True)
    recent_recipes = recipes[:9]
    
    cards = []
    for recipe in recent_recipes:
        category = Path(recipe).parent.name
        filename = Path(recipe).stem
        title = filename.replace('-', ' ').title()
        cards.append(f'''
        <a href="recipes/{category}/{filename}.html" class="recipe-card">
            <img src="images/{category}/{filename}.png" alt="{title}">
            <h2>{title}</h2>
        </a>''')
    
    return '\n'.join(cards)

# Main execution
if __name__ == "__main__":
    # Generate category pages
    for category, emoji in {'pizza': '🍕', 'eats': '🍲', 'treats': '🍪'}.items():
        content = generate_category_section(category, emoji)
        with open(f'recipes/{category}/index.html', 'w') as f:
            f.write(content)
    
    # Generate homepage
    homepage_content = generate_homepage_cards()
    with open('index.html', 'w') as f:
        f.write(homepage_content)