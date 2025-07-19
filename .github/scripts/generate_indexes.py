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