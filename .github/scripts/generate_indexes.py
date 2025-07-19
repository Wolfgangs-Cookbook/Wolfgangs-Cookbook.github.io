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
    active_class = {
        'pizza': ' class="active"' if category == 'pizza' else '',
        'eats': ' class="active"' if category == 'eats' else '',
        'treats': ' class="active"' if category == 'treats' else ''
    }
    
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{category.title()} | Wolfgang's Cookbook</title>
  <link rel="stylesheet" href="../../style.css" />
  <link rel="icon" href="favicon.png" type="image/png" />
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
        <li><a href="../pizza/index.html"{active_class['pizza']}>Pizza</a></li>
        <li><a href="../eats/index.html"{active_class['eats']}>Eats</a></li>
        <li><a href="../treats/index.html"{active_class['treats']}>Treats</a></li>
        <li><a href="../../about.html">About</a></li>
      </ul>
    </nav>
  </header>

  <main>
    <section class="recipe-header">
      <h1>{category.title()} Recipes</h1>
      <p class="subtitle">{get_category_subtitle(category)}</p>
    </section>

    <section class="category-section">
      <div class="recipe-grid">
        {generate_category_cards(category)}
      </div>
    </section>
  </main>

  <footer>
    <p>&copy; 2025 Wolfgang's Cookbook</p>
  </footer>
</body>
</html>'''

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
        # Fix paths to be relative to root directory
        cards.append(f'''
        <a href="{recipe}" class="recipe-card">
            <img src="images/{category}/{filename}.png" alt="{title}">
            <h2>{title}</h2>
        </a>''')
    
    return '\n'.join(cards)

def generate_homepage():
    template = '''<!DOCTYPE html>
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
    return template.format(content=content)

def get_category_subtitle(category):
    subtitles = {
        'pizza': 'Neapolitan-style pizza doughs and sauces',
        'eats': 'Savory mains, sides, and sauces',
        'treats': 'Sweet treats and baked goods'
    }
    return subtitles.get(category, '')

# Update main execution
if __name__ == "__main__":
    # Generate category pages
    for category, emoji in {'pizza': '🍕', 'eats': '🍲', 'treats': '🍪'}.items():
        content = generate_category_section(category, emoji)
        with open(f'recipes/{category}/index.html', 'w') as f:
            f.write(content)
    
    # Generate homepage
    with open('index.html', 'w') as f:
        f.write(generate_homepage())