import json
import re
import os
from typing import Dict, List, Set, Any, Tuple, Union
from pathlib import Path

class LuaConverter:
    def __init__(self, data_dir: str):
        self.data_dir = Path(data_dir)
        self.traits_file = self.data_dir / "plant_traits.json"
        self.lua_file = self.data_dir / "FoodRecipeData.lua"
        self.output_file = self.data_dir / "recipes.json"
        
        self.traits: Dict[str, List[str]] = {}
        self.items_by_trait: Dict[str, List[str]] = {}
        self.lua_vars: Dict[str, Any] = {}
        self.recipes: Dict[str, Any] = {}
        
    def convert(self):
        print("Loading traits...")
        self._load_traits()
        print("Parsing Lua...")
        self._parse_lua_file()
        print(f"Saving {len(self.recipes)} recipes to {self.output_file}...")
        self._save_json()
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
                set1 = set(self._resolve_value(parts[0]))
                set2 = set(self._resolve_value(parts[1]))
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
            
            # Value (variable reference or number in list)
            elif not line.startswith('[') and not line.startswith('local'):
                 # Heuristic for list items that aren't strings
                 val = self._resolve_value(line)
                 data_list.append(val)

            i += 1
            
        return (data_dict if is_dict else data_list, i)

    def _parse_lua_file(self):
        with open(self.lua_file, 'r') as f:
            lines = f.readlines()

        local_list_start = re.compile(r'local (v\d+) = \{')
        
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
                    
                    # Clean up ingredients
                    ingredients = {}
                    if 'Requires' in recipe_data and 'Ingredients' in recipe_data['Requires']:
                        raw_ingredients = recipe_data['Requires']['Ingredients']
                        for key, val in raw_ingredients.items():
                            if isinstance(val, list):
                                ingredients[key] = val
                            elif isinstance(val, str):
                                if val in self.lua_vars:
                                    ingredients[key] = self.lua_vars[val]
                                else:
                                    ingredients[key] = [val]
                            else:
                                ingredients[key] = []

                    self.recipes[recipe_name] = {
                        "id": recipe_data.get('Id', ''),
                        "name": recipe_name,
                        "image_id": recipe_data.get('ImageId', ''),
                        "ingredients": ingredients,
                        "results": recipe_data.get('Results', [recipe_name]),
                        "base_time": recipe_data.get('BaseTime', 0),
                        "base_weight": float(recipe_data.get('BaseWeight', 0)),
                        "priority": recipe_data.get('Priority', 0)
                    }

            i += 1

    def _save_json(self):
        with open(self.output_file, 'w') as f:
            json.dump(self.recipes, f, indent=2)

if __name__ == "__main__":
    converter = LuaConverter("e:/RecipeGenerator/data")
    converter.convert()
