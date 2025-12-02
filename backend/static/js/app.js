const API_URL = 'http://localhost:8000/api';
let allRecipes = [];

async function fetchStats() {
    try {
        const res = await fetch(`${API_URL}/stats`);
        const data = await res.json();
        const container = document.getElementById('stats-container');
        container.innerHTML = `
            <div class="px-3 py-1 rounded-full glass-card border-emerald-500/30 text-emerald-400">
                <span class="font-bold text-white">${data.shop_only_recipes}</span> Recipes
            </div>
        `;
    } catch (e) {
        console.error("Failed to fetch stats", e);
    }
}

async function fetchRecipes() {
    const shopOnly = document.getElementById('shop-filter').checked;
    const select = document.getElementById('recipe-select');

    // Clear current selection
    select.innerHTML = '<option value="" disabled selected>Loading...</option>';
    document.getElementById('result-container').classList.add('opacity-0', 'translate-y-4');

    try {
        const res = await fetch(`${API_URL}/recipes?shop_only=${shopOnly}`);
        allRecipes = await res.json();

        // Sort alphabetically
        allRecipes.sort((a, b) => a.name.localeCompare(b.name));

        // Populate Dropdown
        select.innerHTML = '<option value="" disabled selected>Choose a recipe...</option>';
        if (allRecipes.length === 0) {
            const option = document.createElement('option');
            option.disabled = true;
            option.text = "No recipes found matching criteria";
            select.add(option);
        } else {
            allRecipes.forEach(recipe => {
                const option = document.createElement('option');
                option.value = recipe.name;
                option.text = recipe.name;
                select.add(option);
            });
        }

        fetchStats(); // Refresh stats too
    } catch (e) {
        console.error("Failed to fetch recipes", e);
        select.innerHTML = '<option value="" disabled selected>Error loading recipes</option>';
    }
}

function generateRecipe() {
    const select = document.getElementById('recipe-select');
    const selectedName = select.value;
    const container = document.getElementById('result-container');

    if (!selectedName) return;

    const recipe = allRecipes.find(r => r.name === selectedName);
    if (!recipe) return;

    // Render Card
    let ingredientsHtml = '';
    for (const [name, items] of Object.entries(recipe.ingredients)) {
        // Ensure items is an array
        const itemList = Array.isArray(items) ? items : [];

        ingredientsHtml += `
            <div class="mb-4 last:mb-0">
                <div class="text-xs uppercase tracking-wider text-gray-500 font-semibold mb-2 flex items-center gap-2">
                    <span class="w-1.5 h-1.5 rounded-full bg-emerald-500"></span>
                    ${name}
                </div>
                <div class="text-sm text-gray-300 bg-black/20 rounded-xl p-3 border border-white/5">
                    ${itemList.length > 0 ? itemList.map(i => `<span class="inline-block bg-white/5 rounded-lg px-2 py-1 text-xs mr-1 mb-1 border border-white/5 hover:bg-white/10 transition-colors cursor-default">${i}</span>`).join('') : '<span class="text-red-400 italic">No items available</span>'}
                </div>
            </div>
        `;
    }

    const IMAGE_MAP = {
        "Burger": "food_burger.webp",
        "Soup": "food_soup.png",
        "Corn Dog": "food_corn_dog.webp",
        "Hot Dog": "food_hot_dog.webp",
        "Sandwich": "food_sandwich.webp",
        "Salad": "food_salad.webp",
        "Pie": "food_pie.webp",
        "Waffle": "food_waffle.webp",
        "Pizza": "food_pizza.webp",
        "Sushi": "food_sushi.webp",
        "Donut": "food_donut.webp",
        "Ice Cream": "food_ice_cream.webp",
        "Cake": "food_cake.webp",
        "Smoothie": "food_smoothie.webp",
        "Porridge": "food_porridge.webp",
        "Spaghetti": "food_spaghetti.webp",
        "Candy Apple": "food_candy_apple.webp",
        "Sweet Tea": "food_sweet_tea.webp"
    };

    const imageFile = IMAGE_MAP[recipe.name] || "";
    const imageSrc = imageFile ? `/static/img/foods/${imageFile}` : "";
    const imageHtml = imageSrc
        ? `<img src="${imageSrc}" alt="${recipe.name}" class="w-full h-full object-cover">`
        : `<span class="text-4xl">🍲</span>`;

    container.innerHTML = `
        <div class="glass-card rounded-2xl p-8 border-t-4 border-t-emerald-500 shadow-2xl shadow-emerald-900/20">
            <div class="flex items-start justify-between mb-6">
                <div class="flex items-center gap-4">
                    <div class="w-16 h-16 rounded-2xl bg-gray-800 border border-gray-700 flex items-center justify-center overflow-hidden shadow-inner">
                        ${imageHtml}
                    </div>
                    <div>
                        <h3 class="text-3xl font-bold text-white">${recipe.name}</h3>
                        <div class="text-sm text-gray-500 flex gap-4 mt-1">
                            <span class="flex items-center gap-1">⏱️ ${recipe.base_time}s</span>
                            <span class="flex items-center gap-1">🔀 ${recipe.combinations.toLocaleString()} Combos</span>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="space-y-2 bg-gray-800/30 rounded-xl p-6 border border-white/5">
                ${ingredientsHtml}
            </div>
        </div>
    `;

    // Animate in
    container.classList.remove('opacity-0', 'translate-y-4');
}

// Initial Load
document.addEventListener('DOMContentLoaded', () => {
    fetchRecipes();
    fetchStats();

    // Add toggle animation logic
    const checkbox = document.getElementById('shop-filter');
    const dot = document.querySelector('.dot');
    checkbox.addEventListener('change', function () {
        if (this.checked) {
            dot.classList.add('translate-x-6');
        } else {
            dot.classList.remove('translate-x-6');
        }
    });
});
