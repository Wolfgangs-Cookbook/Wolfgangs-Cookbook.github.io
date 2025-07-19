import os
import glob
from pathlib import Path

def generate_recipe_card(recipe_path, images_path):
    filename = Path(recipe_path).stem
    title = filename.replace('-', ' ').title()
    image_path = f"../../images/{images_path}/{filename}.png"  # Note the extra ../
    relative_path = os.path.basename(recipe_path)  # Just the filename for category pages
    
    return f'''
        <a href="{relative_path}" class="recipe-card">
          <img src="{image_path}" alt="{title}">
          <h3>{title}</h3>
        </a>'''

def generate_category_index(category, emoji):
    category_template = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>{category.title()} - Wolfgang's Cookbook</title>
  <link rel="stylesheet" href="../../style.css" />
</head>
<body>
  <header>
    <div class="hero">
      <a href="../../index.html">
        <img src="../../logo.png" alt="Wolfgang's Cookbook Logo" class="logo">
      </a>
      <p class="tagline">Health-considerate, high-flavor recipes made from scratch.</p>
    </div>
    <nav>
      <ul>
        <li><a href="../../index.html">Home</a></li>
        <li><a href="../index.html">Recipe Index</a></li>
        <li><a href="../pizza/index.html">Pizza</a></li>
        <li><a href="../eats/index.html">Eats</a></li>
        <li><a href="../treats/index.html">Treats</a></li>
        <li><a href="../../about.html">About</a></li>
      </ul>
    </nav>
  </header>

  <section class="recipe-header">
    <h1>{category.title()}</h1>
    <p class="subtitle">{get_category_subtitle(category)}</p>
  </section>

  <main>
    <div class="recipe-grid">
      {generate_category_cards(category)}
    </div>
  </main>

  <footer>
    <p>&copy; 2025 Wolfgang's Cookbook</p>
  </footer>
</body>
</html>'''
    
    # Write category index file
    with open(f'recipes/{category}/index.html', 'w') as f:
        f.write(category_template)

def get_category_subtitle(category):
    subtitles = {
        'pizza': 'Low-sodium doughs and classic toppings.',
        'eats': 'Savory mains, sides, sauces, and more.',
        'treats': 'Sweet treats and baked goods with balanced flavors.'
    }
    return subtitles.get(category, '')

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
    
    print(f"Total recipes found: {len(recipes)}")
    
    # Sort by modification time, newest first
    recipes.sort(key=lambda x: os.path.getmtime(x), reverse=True)
    recent_recipes = recipes[:9]
    
    print(f"Processing {len(recent_recipes)} recent recipes:")
    for r in recent_recipes:
        print(f"  - {r}")
    
    cards = []
    for recipe in recent_recipes:
        category = Path(recipe).parent.name
        filename = Path(recipe).stem
        title = filename.replace('-', ' ').title()
        print(f"Creating card for {title} from {category}")
        
        card = f'''
        <a href="recipes/{category}/{filename}.html" class="recipe-card">
            <img src="images/{category}/{filename}.png" alt="{title}">
            <h2>{title}</h2>
        </a>'''
        cards.append(card)
    
    final_html = '\n'.join(cards)
    print(f"Generated {len(cards)} cards")
    return final_html

def generate_homepage():
    homepage_template = '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Wolfgang's Cookbook</title>
  <link rel="stylesheet" href="style.css" />
  <link rel="icon" href="favicon.png" type="image/png" />
</head>
<body>
  <header>
    <div class="hero">
      <a href="index.html">
        <img src="logo.png" alt="Wolfgang's Cookbook Logo" class="logo">
      </a>
      <p class="tagline">Health-considerate, high-flavor recipes made from scratch.</p>
    </div>
    <nav>
      <ul>
        <li><a href="recipes/index.html">Recipe Index</a></li>
        <li><a href="recipes/pizza/index.html">Pizza</a></li>
        <li><a href="recipes/eats/index.html">Eats</a></li>
        <li><a href="recipes/treats/index.html">Treats</a></li>
        <li><a href="about.html">About</a></li>
      </ul>
    </nav>
  </header>

  <main>
    <section class="intro">
      <p>Welcome to Wolfgang's Cookbook — a collection of full-flavor recipes rooted in tradition and aspiring to be as healthy as possible. I'm always open to suggestions and tips, so if you find any, email them to ofstedal.wolfgang@gmail.com while we work on implementing a comment function.</p>
    </section>

    <section class="featured-recipes">
      <h2>Latest Recipes</h2>
      <div class="recipe-grid">
        {content}
      </div>
    </section>
  </main>

  <footer>
    <p>&copy; 2025 Wolfgang's Cookbook</p>
  </footer>
</body>
</html>'''

    content = generate_homepage_cards()
    
    with open('index.html', 'w') as f:
        f.write(homepage_template.format(content=content))

# Generate both main index and category pages
categories = {
    'pizza': '🍕',
    'eats': '🍲',
    'treats': '🍪'
}

# Generate category index pages
for category in categories:
    generate_category_index(category, categories[category])

# Main index template
index_template = '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>All Recipes | Wolfgang's Cookbook</title>
  <link rel="stylesheet" href="../style.css">
</head>
<body>
  <header>
    <div class="hero">
      <a href="../index.html">
        <img src="../logo.png" alt="Wolfgang's Cookbook Logo" class="logo">
      </a>
      <p class="tagline">Health-considerate, high-flavor recipes made from scratch.</p>
    </div>
    <nav>
      <ul>
        <li><a href="../index.html">Home</a></li>
        <li><a href="index.html" class="active">Recipe Index</a></li>
        <li><a href="pizza/index.html">Pizza</a></li>
        <li><a href="eats/index.html">Eats</a></li>
        <li><a href="treats/index.html">Treats</a></li>
        <li><a href="../about.html">About</a></li>
      </ul>
    </nav>
  </header>

  <section class="recipe-header">
    <h1>All Recipes</h1>
    <p class="subtitle">Browse our complete collection.</p>
  </section>

  <main>
    {content}
  </main>

  <footer>
    <p>&copy; 2025 Wolfgang's Cookbook</p>
  </footer>
</body>
</html>
'''

# Generate main index
categories = {
    'pizza': '🍕',
    'eats': '🍲',
    'treats': '🍪'
}

content = '\n'.join(generate_category_section(cat, emoji) 
                   for cat, emoji in categories.items())

with open('recipes/index.html', 'w') as f:
    f.write(index_template.format(content=content))

# Add this to your main execution section
if __name__ == "__main__":
    # ...existing category index generation code...
    generate_homepage()