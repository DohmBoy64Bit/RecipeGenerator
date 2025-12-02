-- Saved by UniversalSynSaveInstance (Join to Copy Games) https://discord.gg/wx4ThpAsmw

--Decompiled by Medal, I take no credit I only Made The dumper and I I.. I iron man
local v1 = game:GetService("ReplicatedStorage")
v1:WaitForChild("Assets"):WaitForChild("Models")
local v2 = require(v1.Modules.PlantTraitsData)
local v3 = require(v1.Modules.TableUtils)
local v4 = {}
local v5 = {
	"Corn",
	"Violet Corn",
	"Cauliflower",
	"Banana",
	"Sugarglaze"
}
local v6 = {
	"Pepper",
	"Bell Pepper",
	"Ember Lily",
	"Cactus",
	"Mushroom",
	"Eggplant",
	"Venus Fly Trap",
	"Glowshroom",
	"Bone Blossom",
	"Tall Asparagus",
	"Taco Fern"
}
local v7 = {
	"Tomato",
	"Bamboo",
	"Taro Flower",
	"Sunflower",
	"Avocado",
	"Pineapple",
	"Bell Pepper",
	"Onion",
	"Jalapeno",
	"Grand Tomato",
	"Artichoke"
}
local v8 = {
	"Coconut",
	"Pumpkin",
	"Crown Melon",
	"Sugarglaze"
}
local v9 = { "Tomato", "Grand Tomato" }
local v10 = {}
local v11 = {
	["Id"] = "c",
	["ImageId"] = "rbxassetid://100029889334054",
	["Priority"] = 10
}
local v12 = {
	["Count"] = 3,
	["Ingredients"] = {
		["Bread"] = v5,
		["Meat"] = v6,
		["Leafy"] = v7
	}
}
v11.Requires = v12
v11.Results = { "Burger" }
v11.BaseTime = 400
v11.BaseWeight = 2
v10.Burger = v11
local v13 = {
	["Id"] = "d",
	["ImageId"] = "rbxassetid://122580735203073",
	["Priority"] = 0,
	["Requires"] = {
		["Count"] = 1
	},
	["Results"] = { "Soup" },
	["BaseTime"] = 300,
	["BaseWeight"] = 0.5
}
v10.Soup = v13
local v14 = {
	["Id"] = "cdog",
	["ImageId"] = "rbxassetid://123984061977008",
	["Priority"] = 5
}
local v15 = {
	["Count"] = 2,
	["Ingredients"] = {
		["Stick"] = v2.Traits.Woody,
		["Meat"] = v6,
		["Batter"] = { "Corn", "Violet Corn" }
	}
}
v14.Requires = v15
v14.Results = { "Corndog" }
v14.BaseTime = 400
v14.BaseWeight = 1.5
v10.Corndog = v14
local v16 = {
	["Id"] = "e",
	["ImageId"] = "rbxassetid://136455657586960",
	["Priority"] = 5
}
local v17 = {
	["Count"] = 2,
	["Ingredients"] = {
		["Bread"] = v5,
		["Meat"] = v6
	}
}
v16.Requires = v17
v16.Results = { "HotDog" }
v16.BaseTime = 400
v16.BaseWeight = 1.5
v10.HotDog = v16
local v18 = {
	["Id"] = "f",
	["ImageId"] = "rbxassetid://139763254124497",
	["Priority"] = 3
}
local v19 = {
	["Count"] = 3,
	["Ingredients"] = {
		["Bread"] = v5,
		["Leafy"] = v7,
		["Tomato"] = v9
	}
}
v18.Requires = v19
v18.Results = { "Sandwich" }
v18.BaseTime = 350
v18.BaseWeight = 1
v10.Sandwich = v18
local v20 = {
	["Id"] = "g",
	["ImageId"] = "rbxassetid://96781873740831",
	["Priority"] = 2
}
local v21 = {
	["Count"] = 2,
	["Ingredients"] = {
		["Leafy"] = v7,
		["Vegetable"] = v2.Traits.Vegetable
	}
}
v20.Requires = v21
v20.Results = { "Salad" }
v20.BaseTime = 350
v20.BaseWeight = 0.2
v10.Salad = v20
local v22 = {
	["Id"] = "i",
	["ImageId"] = "rbxassetid://126935428774858",
	["Priority"] = 8
}
local v23 = {
	["Count"] = 2,
	["Ingredients"] = {
		["Pastry"] = v8,
		["Filling"] = v3:MakeTable(v2.Traits.Vegetable, v6)
	}
}
v22.Requires = v23
v22.Results = { "Pie" }
v22.BaseTime = 400
v22.BaseWeight = 3
v10.Pie = v22
local v24 = {
	["Id"] = "j",
	["ImageId"] = "rbxassetid://112367385396275",
	["Priority"] = 6
}
local v25 = {
	["Count"] = 3,
	["Ingredients"] = {
		["Pastry"] = v8,
		["Sweet"] = v2.Traits.Sweet
	}
}
v24.Requires = v25
v24.Results = { "Waffle" }
v24.BaseTime = 350
v24.BaseWeight = 1.2
v10.Waffle = v24
local v26 = {
	["Id"] = "k",
	["ImageId"] = "rbxassetid://99865068747737",
	["Priority"] = 7
}
local v27 = {
	["Count"] = 4,
	["Ingredients"] = {
		["Bread"] = v5,
		["Meat"] = v6,
		["Vegetable"] = v2.Traits.Vegetable,
		["Sauce"] = v2.Traits.Fruit
	}
}
v26.Requires = v27
v26.Results = { "Pizza" }
v26.BaseTime = 500
v26.BaseWeight = 2
v10.Pizza = v26
local v28 = {
	["Id"] = "l",
	["ImageId"] = "rbxassetid://124413058833848",
	["Priority"] = 20
}
local v29 = {
	["Count"] = 3,
	["Ingredients"] = {
		["Bamboo"] = { "Bamboo" },
		["Wrap"] = v7,
		["Main"] = v3:MakeTable(v6, v2.Traits.Vegetable),
		["Rice"] = v3:MakeTable(v5, "Coconut")
	}
}
v28.Requires = v29
v28.Results = { "Sushi" }
v28.BaseTime = 300
v28.BaseWeight = 2
v10.Sushi = v28
local v30 = {
	["Id"] = "m",
	["ImageId"] = "rbxassetid://103702025640123",
	["Priority"] = 9
}
local v31 = {
	["Count"] = 3,
	["Ingredients"] = {
		["Bread"] = v5,
		["Icing"] = v2.Traits.Sweet,
		["Sprinkles"] = v2.Traits.Sweet
	}
}
v30.Requires = v31
v30.Results = { "Donut" }
v30.BaseTime = 200
v30.BaseWeight = 2
v10.Donut = v30
local v32 = {
	["Id"] = "n",
	["ImageId"] = "rbxassetid://80440750183765",
	["Priority"] = 10
}
local v33 = {
	["Count"] = 2,
	["Ingredients"] = {
		["Cone"] = v5,
		["Cream"] = v2.Traits.Sweet
	}
}
v32.Requires = v33
v32.Results = { "IceCream" }
v32.BaseTime = 300
v32.BaseWeight = 2
v10.IceCream = v32
local v34 = {
	["Id"] = "o",
	["ImageId"] = "rbxassetid://133935704392240",
	["Priority"] = 10
}
local v35 = {
	["Count"] = 4,
	["Ingredients"] = {
		["Bread"] = v5,
		["Icing"] = v2.Traits.Sweet,
		["Filling"] = v2.Traits.Sweet,
		["Fruit"] = v2.Traits.Fruit
	}
}
v34.Requires = v35
v34.Results = { "Cake" }
v34.BaseTime = 350
v34.BaseWeight = 2
v10.Cake = v34
local v36 = {
	["Id"] = "p",
	["ImageId"] = "rbxassetid://99520717630343",
	["Priority"] = 6
}
local v37 = {
	["Count"] = 2,
	["Ingredients"] = {
		["Fruit"] = v2.Traits.Fruit
	}
}
v36.Requires = v37
v36.Results = { "Smoothie" }
v36.BaseTime = 400
v36.BaseWeight = 1.2
v10.Smoothie = v36
local v38 = {
	["Id"] = "r",
	["ImageId"] = "rbxassetid://121467388211046",
	["Priority"] = 3
}
local v39 = {
	["Count"] = 3,
	["Ingredients"] = {
		["Base"] = v5,
		["Cream"] = v5,
		["Fruit"] = v2.Traits.Fruit
	}
}
v38.Requires = v39
v38.Results = { "Porridge" }
v38.BaseTime = 250
v38.BaseWeight = 2
v10.Porridge = v38
local v40 = {
	["Id"] = "t",
	["ImageId"] = "rbxassetid://118816141566924",
	["Priority"] = 6
}
local v41 = {
	["Count"] = 4,
	["Ingredients"] = {
		["Pasta"] = v5,
		["Sauce"] = v9,
		["Meat"] = v6,
		["Vegetables"] = v2.Traits.Vegetable
	}
}
v40.Requires = v41
v40.Results = { "Spaghetti" }
v40.BaseTime = 350
v40.BaseWeight = 2.5
v10.Spaghetti = v40
local v42 = {
	["Id"] = "v",
	["ImageId"] = "rbxassetid://98794672893031",
	["Priority"] = 10
}
local v43 = {
	["Count"] = 2,
	["Ingredients"] = {
		["Apple"] = {
			"Apple",
			"Green Apple",
			"Sugar Apple",
			"Maple Apple"
		},
		["CandyCoating"] = v2.Traits.Sweet
	}
}
v42.Requires = v43
v42.Results = { "CandyApple" }
v42.BaseTime = 200
v42.BaseWeight = 0.7
v10.CandyApple = v42
local v44 = {
	["Id"] = "y",
	["ImageId"] = "rbxassetid://114245564378378",
	["Priority"] = 4
}
local v45 = {
	["Count"] = 2,
	["Ingredients"] = {
		["HerbalBase"] = v3:MakeTable(v3:SetSubtract(v2.Traits.Flower, v2.Traits.Toxic), "Mint"),
		["Sweetener"] = v2.Traits.Sweet
	}
}
v44.Requires = v45
v44.Results = { "SweetTea" }
v44.BaseTime = 270
v44.BaseWeight = 0.5
v10.SweetTea = v44
v4.Recipes = v10
local v46 = {}
for v47, _ in v4.Recipes do
	v46[v47] = v47
end
v4.RecipeNames = v46
return v4
