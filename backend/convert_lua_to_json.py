import json
import re
from typing import Dict, List, Any, Tuple
from pathlib import Path

class LuaConverter:
    def __init__(self, data_dir: str):
        self.data_dir = Path(data_dir)
        self.traits_file = self.data_dir / "plant_traits.json"
        self.lua_file = self.data_dir / "FoodRecipeData.lua"
        self.recipes_output = self.data_dir / "recipes.json"
        self.cooking_output = self.data_dir / "cooking.json"
        
        self.traits: Dict[str, List[str]] = {}
        self.items_by_trait: Dict[str, List[str]] = {}
        self.lua_vars: Dict[str, Any] = {}
        self.recipes: Dict[str, Any] = {}
        self.cooking_categories: Dict[str, List[str]] = {}
        
    def convert(self):
        print("Loading traits...")
        self._load_traits()
        print("Parsing Lua...")
        self._parse_lua_file()
        print(f"Saving {len(self.recipes)} recipes to {self.recipes_output}...")
        self._save_recipes()
        print(f"Saving {len(self.cooking_categories)} cooking categories to {self.cooking_output}...")
        self._save_cooking()
        print("Done.")

    def _load_traits(self):
        with open(self.traits_file, 'r') as f:
            self.traits = json.load(f)
            
        for item, trait_list in self.traits.items():
            for trait in trait_list:
                if trait not in self.items_by_trait:
                    self.items_by_trait[trait] = []
                self.items_by_trait[trait].append(item)

    def _resolve_value(self, val_str: str) -> Any:
        val_str = val_str.strip().rstrip(',')
        
        # Handle inline lists: { "A", "B" }
        if val_str.startswith('{') and val_str.endswith('}'):
            content = val_str[1:-1].strip()
            if not content:
                return []
            return [x.strip().strip('"') for x in content.split(',')]

        if val_str.startswith('"') and val_str.endswith('"'):
            return val_str.strip('"')
        if val_str.isdigit():
            return int(val_str)
        try:
            return float(val_str)
        except ValueError:
            pass
        
        # Check if it's a variable reference
        if val_str in self.lua_vars:
            return self.lua_vars[val_str]
        
        if val_str.startswith('v2.Traits.'):
            trait = val_str.split('.')[-1]
            return self.items_by_trait.get(trait, [])
        
        if 'v3:MakeTable' in val_str:
            return self._handle_function_call(val_str)
            
        if 'v3:SetSubtract' in val_str:
            return self._handle_function_call(val_str)

        return val_str

    def _handle_function_call(self, line: str) -> List[str]:
        if 'v3:MakeTable' in line:
            args_match = re.search(r'v3:MakeTable\((.+)\)', line)
            if args_match:
                args = [x.strip() for x in args_match.group(1).split(',')]
                result = []
                for arg in args:
                    resolved = self._resolve_value(arg)
                    if isinstance(resolved, list):
                        result.extend(resolved)
                    elif isinstance(resolved, str):
                        result.append(resolved)
                return list(set(result))
        
        if 'v3:SetSubtract' in line:
            content = line.split('v3:SetSubtract(')[1].split(')')[0]
            parts = [p.strip() for p in content.split(',')]
            if len(parts) >= 2:
                set1 = set(self._resolve_value(parts[0]) if isinstance(self._resolve_value(parts[0]), list) else [])
                set2 = set(self._resolve_value(parts[1]) if isinstance(self._resolve_value(parts[1]), list) else [])
                return list(set1 - set2)
        
        return []

    def _parse_table(self, lines: List[str], start_index: int) -> Tuple[Any, int]:
        data_dict = {}
        data_list = []
        is_dict = False
        
        field_assign = re.compile(r'\["(.+?)"\] = (.+)')
        
        i = start_index
        while i < len(lines):
            line = lines[i].strip()
            
            if line.startswith('}') or line.startswith('},'):
                return (data_dict if is_dict else data_list, i)
            
            # ["Key"] = Value
            field_match = field_assign.search(line)
            if field_match:
                is_dict = True
                key = field_match.group(1)
                val_str = field_match.group(2).strip().rstrip(',')
                
                if val_str.startswith('{') and not val_str.endswith('}'):
                    # Recurse
                    val, i = self._parse_table(lines, i + 1)
                    data_dict[key] = val
                else:
                    data_dict[key] = self._resolve_value(val_str)
            
            # "Value",
            elif line.startswith('"'):
                val = line.strip('", ')
                data_list.append(val)

            i += 1
            
        return (data_dict if is_dict else data_list, i)

    def _parse_lua_file(self):
        with open(self.lua_file, 'r') as f:
            lines = f.readlines()

        local_list_start = re.compile(r'local (v\d+) = \{')
        
        # Map variable names to cooking category names
        var_to_category = {
            'v5': 'Bread',
            'v6': 'Meat', 
            'v7': 'Leafy',
            'v8': 'Pastry',
            'v9': 'Tomato'
        }
        
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            
            if line.startswith('--') or not line:
                i += 1
                continue

            # local vX = { ... }
            match = local_list_start.search(line)
            if match:
                var_name = match.group(1)
                
                if line.strip().endswith('{}'):
                    self.lua_vars[var_name] = {}
                    i += 1
                    continue
                
                # Parse table starting from next line
                val, i = self._parse_table(lines, i + 1)
                self.lua_vars[var_name] = val
                
                # If this is a cooking category variable, save it
                if var_name in var_to_category and isinstance(val, list):
                    category_name = var_to_category[var_name]
                    self.cooking_categories[category_name] = val
            
            # vX.Prop = Val
            prop_assign = re.match(r'(v\d+)\.(\w+) = (.+)', line)
            if prop_assign:
                target_var = prop_assign.group(1)
                prop_name = prop_assign.group(2)
                value_src = prop_assign.group(3)
                
                if target_var in self.lua_vars:
                    val = self._resolve_value(value_src)
                    if isinstance(self.lua_vars[target_var], list):
                         if not self.lua_vars[target_var]:
                             self.lua_vars[target_var] = {}
                    
                    if isinstance(self.lua_vars[target_var], dict):
                        self.lua_vars[target_var][prop_name] = val

            # v10.RecipeName = vX
            recipe_match = re.match(r'v10\.(\w+) = (v\d+)', line)
            if recipe_match:
                recipe_name = recipe_match.group(1)
                var_ref = recipe_match.group(2)
                
                if var_ref in self.lua_vars:
                    recipe_data = self.lua_vars[var_ref]
                    
                    # Extract ingredient requirements with counts
                    ingredients = {}
                    if 'Requires' in recipe_data:
                        requires = recipe_data['Requires']
                        count = requires.get('Count', 0)
                        
                        if 'Ingredients' in requires:
                            # Store just the category names, not the actual items
                            # RecipeService will resolve these at runtime
                            for category in requires['Ingredients'].keys():
                                ingredients[category] = 1  # Each category needs 1 item
                        elif count == 1:
                            # Special case for Soup - accepts any single ingredient
                            ingredients['Any'] = 1

                    self.recipes[recipe_name] = {
                        "id": recipe_data.get('Id', ''),
                        "image_id": recipe_data.get('ImageId', ''),
                        "ingredients": ingredients,
                        "count": recipe_data.get('Requires', {}).get('Count', 0),
                        "priority": recipe_data.get('Priority', 0),
                        "base_time": recipe_data.get('BaseTime', 0),
                        "base_weight": float(recipe_data.get('BaseWeight', 0)),
                        "description": f"Requires {recipe_data.get('Requires', {}).get('Count', 0)} ingredients"
                    }

            i += 1

    def _save_recipes(self):
        with open(self.recipes_output, 'w') as f:
            json.dump(self.recipes, f, indent=2)

    def _save_cooking(self):
        # Add additional categories that are derived or special
        cooking_data = {
            **self.cooking_categories,
            "Bamboo": ["Bamboo"],
            "Wrap": self.cooking_categories.get("Leafy", []),
            "Rice": self.cooking_categories.get("Bread", []) + ["Coconut"],
            "Apple": ["Apple", "Green Apple", "Sugar Apple", "Maple Apple"],
            "Batter": ["Corn", "Violet Corn"],
            "Pasta": self.cooking_categories.get("Bread", []),
            "Vegetables": [],  # Will be resolved from traits
            "Main": []  # Will be resolved from Meat + Vegetables
        }
        
        with open(self.cooking_output, 'w') as f:
            json.dump(cooking_data, f, indent=2)

if __name__ == "__main__":
    converter = LuaConverter("e:/RecipeGenerator/data")
    converter.convert()
