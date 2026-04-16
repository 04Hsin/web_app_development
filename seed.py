import os
from app.models import User, Recipe, Ingredient
from werkzeug.security import generate_password_hash

def seed_data():
    print("開始匯入示範食譜資料...")
    
    # 1. 建立一個預設使用者 (若不存在)
    user = User.get_by_email('demo@example.com')
    if user:
        user_id = user.id
        print("已存在示範帳號")
    else:
        try:
            user_id = User.create('食譜達人 (示範)', 'demo@example.com', generate_password_hash('demo123', method='pbkdf2:sha256'))
            print("建立了全新的示範帳號")
        except Exception as e:
            print(f"建立使用者失敗: {e}")
            return

    # 2. 定義示範食譜庫
    recipes_data = [
        {
            "title": "經典番茄炒蛋",
            "description": "大人小孩都愛的下飯神菜，酸酸甜甜的超讚！",
            "steps": "1. 將番茄切塊，蔥切段備用。\n2. 雞蛋打散，下熱油鍋炒至半熟後先盛出。\n3. 鍋中留少許油，放入蔥白爆香，接著放入番茄炒出紅油與軟爛。\n4. 加入少許番茄醬與糖調味。\n5. 將半熟蛋倒回鍋中拌勻，灑上蔥花即可起鍋。",
            "image_url": "https://images.unsplash.com/photo-1598514982205-f36b96d1e8d4?q=80&w=600",
            "category": "台式家常",
            "ingredients": ["番茄", "雞蛋", "青蔥"]
        },
        {
            "title": "滑嫩洋蔥炒牛肉",
            "description": "超強的便當菜色，醬汁淋飯可以吃三碗。",
            "steps": "1. 牛肉切絲或切片，使用少許醬油、米酒、太白粉醃製 10 分鐘。\n2. 洋蔥切絲備用。\n3. 熱鍋下少許油，將牛肉下鍋快炒至變色後盛出。\n4. 利用原鍋將洋蔥絲炒軟、炒出甜味。\n5. 倒入牛肉，加入少許醬油膏與烏醋拌炒均勻即可。",
            "image_url": "https://images.unsplash.com/photo-1603048297172-c92544798d5e?q=80&w=600",
            "category": "便當菜",
            "ingredients": ["洋蔥", "牛肉", "醬油"]
        },
        {
            "title": "元氣番茄牛肉湯",
            "description": "冬天喝最舒服，充滿蔬菜甜味與牛肉香氣的濃湯。",
            "steps": "1. 牛肋條或牛楠切塊，冷水下鍋川燙去血水後洗淨。\n2. 番茄切塊，大顆洋蔥切大塊，紅蘿蔔切塊。\n3. 鍋內加少許油，將洋蔥與番茄炒香出汁。\n4. 加入牛肉塊拌炒，隨後倒入淹過食材的水。\n5. 大火煮滾後轉小火燉煮約 1.5 小時，直到牛肉軟爛。\n6. 起鍋前加鹽巴調味。",
            "image_url": "https://images.unsplash.com/photo-1548943487-a2e4f43b4853?q=80&w=600",
            "category": "湯品",
            "ingredients": ["番茄", "牛肉", "洋蔥", "紅蘿蔔"]
        },
        {
            "title": "青椒炒肉絲",
            "description": "健康營養又快速的簡單快炒。",
            "steps": "1. 豬肉絲用少許醬油、胡椒粉醃製。\n2. 青椒洗淨去籽切絲，蒜頭切末。\n3. 熱鍋下油爆香蒜末，放入肉絲過油炒至八分熟。\n4. 加入青椒絲大火快炒約 1 分鐘，加鹽調味即完成。",
            "image_url": "https://images.unsplash.com/photo-1627308595171-d1b5d67129c4?q=80&w=600",
            "category": "快炒",
            "ingredients": ["青椒", "豬肉", "蒜頭"]
        }
    ]

    # 3. 寫入資料庫
    added_count = 0
    for data in recipes_data:
        try:
            recipe_id = Recipe.create(
                user_id=user_id,
                title=data["title"],
                steps=data["steps"],
                description=data["description"],
                image_url=data["image_url"],
                category=data["category"]
            )
            # 寫入關聯食材
            for ing_name in data["ingredients"]:
                ing = Ingredient.get_by_name(ing_name)
                if not ing:
                    ing_id = Ingredient.create(ing_name)
                else:
                    ing_id = ing.id
                
                Ingredient.add_to_recipe(recipe_id, ing_id)
            print(f"成功加入食譜: {data['title']}")
            added_count += 1
        except Exception as e:
            print(f"加入 {data['title']} 失敗: {e}")

    print(f"匯入完成！一共新增了 {added_count} 筆食譜的關聯！可以去冰箱尋寶試試看了。")

if __name__ == "__main__":
    seed_data()
