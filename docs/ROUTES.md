# 路由與頁面設計文件 (ROUTES.md)

本文件描述系統的 Flask 路由規劃，包含每個頁面的 URL 路徑、HTTP 方法、對應的 Jinja2 模板與所需處理邏輯。

## 1. 路由總覽表格

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| :--- | :--- | :--- | :--- | :--- |
| **首頁** | | | | |
| 網站首頁 | GET | `/` | `templates/index.html` | 顯示歡迎頁或推薦清單 |
| **會員管理 (Auth)** | | | | |
| 註冊頁面 | GET | `/auth/register` | `templates/auth/register.html` | 顯示註冊表單 |
| 處理註冊 | POST | `/auth/register` | — | 接收資料存入 DB，重導向至登入 |
| 登入頁面 | GET | `/auth/login` | `templates/auth/login.html` | 顯示登入表單 |
| 處理登入 | POST | `/auth/login` | — | 驗證帳密，建立 Session，重導向 |
| 處理登出 | GET | `/auth/logout` | — | 清除 Session，重導向至首頁 |
| 會員中心 | GET | `/auth/profile` | `templates/auth/profile.html` | 顯示個人建立的食譜列表 |
| **食譜管理 (Recipe)** | | | | |
| 食譜總覽 | GET | `/recipes` | `templates/recipe/index.html` | 列出所有食譜 |
| 新增食譜頁面 | GET | `/recipes/new` | `templates/recipe/new.html` | 顯示新增食譜表單 |
| 處理新增 | POST | `/recipes/new` | — | 接收資料建立食譜與食材關聯 |
| 單一食譜詳情 | GET | `/recipes/<id>` | `templates/recipe/detail.html` | 顯示食譜詳細內容 |
| 編輯食譜頁面 | GET | `/recipes/<id>/edit` | `templates/recipe/edit.html` | 顯示舊資料的編輯表單 |
| 處理更新 | POST | `/recipes/<id>/edit` | — | 接收修改後的資料並更新 DB |
| 處理刪除 | POST | `/recipes/<id>/delete`| — | 刪除食譜並重導向 |
| **冰箱尋寶 (Search)** | | | | |
| 搜尋頁面 | GET | `/search` | `templates/search/index.html` | 顯示搜尋表單（包含多項食材） |
| 處理搜尋 | GET | `/search/results`| `templates/search/results.html`| 接收 Query String 並比對資料庫 |

## 2. 每個路由的詳細說明

### 首頁 (main.py)
* `GET /`:
  - **處理邏輯**: 查詢最近新增的數筆食譜傳遞給模板以顯示首頁。
  - **輸出**: 渲染 `index.html`。

### 會員管理 (auth.py)
* `GET /auth/register`: 
  - **輸出**: 渲染 `auth/register.html`。
* `POST /auth/register`:
  - **輸入**: `username`, `email`, `password` 表單資料。
  - **處理邏輯**: 驗證信箱是否重複，將密碼雜湊，呼叫 `User.create` 寫入。
  - **輸出**: 重導向至 `/auth/login`。
  - **錯誤處理**: 資料不全或重複時，傳遞 error string 並重新渲染註冊頁。
* `GET /auth/login`:
  - **輸出**: 渲染 `auth/login.html`。
* `POST /auth/login`:
  - **輸入**: `email`, `password` 表單資料。
  - **處理邏輯**: 以信箱查詢使用者，比對雜湊密碼。若成功則設定 `session['user_id']`。
  - **輸出**: 登入成功重導至 `/` 或是 `/auth/profile`。
* `GET /auth/logout`:
  - **處理邏輯**: 執行 `session.pop('user_id')`。
  - **輸出**: 重導向至首頁 `/`。
* `GET /auth/profile`:
  - **處理邏輯**: 需驗證登入。透過 session 取得 user_id，呼叫 `Recipe.get_by_user_id` 找回個人的食譜。
  - **輸出**: 渲染 `auth/profile.html`。

### 食譜管理 (recipe.py)
* `GET /recipes`:
  - **處理邏輯**: 呼叫 `Recipe.get_all()` 回傳全部資料。
  - **輸出**: 渲染 `recipe/index.html`。
* `GET /recipes/new`:
  - **處理邏輯**: 必須登入狀態。
  - **輸出**: 渲染 `recipe/new.html`。
* `POST /recipes/new`:
  - **輸入**: `title`, `description`, `steps`, `image_url` 以及多個食材欄位等。
  - **處理邏輯**: 呼叫 `Recipe.create()`，再將接回來的食材字串建立至 `RecipeIngredient` 中。
  - **輸出**: 重導向至 `/recipes/<id>`。
* `GET /recipes/<id>`:
  - **處理邏輯**: 呼叫 `Recipe.get_by_id()` 以及 `Ingredient.get_by_recipe()`。
  - **輸出**: 渲染 `recipe/detail.html`。
  - **錯誤處理**: 無此資料時回傳 404 頁面。
* `GET /recipes/<id>/edit`:
  - **處理邏輯**: 取得舊資料且驗證操作者為擁有者。
  - **輸出**: 渲染 `recipe/edit.html`。
* `POST /recipes/<id>/edit`:
  - **輸入**: 更新的表單資料。
  - **處理邏輯**: 呼叫 `Recipe.update()` 等。
  - **輸出**: 重導向至 `/recipes/<id>`。
* `POST /recipes/<id>/delete`:
  - **處理邏輯**: 驗證登入與擁有者。呼叫 `Recipe.delete()`。
  - **輸出**: 重導向至 `/auth/profile`。

### 冰箱尋寶 (search.py)
* `GET /search`:
  - **輸出**: 渲染 `search/index.html` 尋寶入口。
* `GET /search/results`:
  - **輸入**: URL Query String，如 `?ingredients=番茄,雞蛋` 或一般關鍵字 `?q=蘋果`。
  - **處理邏輯**: 搜尋包含該食材關聯的食譜資料，回傳交集或聯集結果。
  - **輸出**: 渲染 `search/results.html`。

## 3. Jinja2 模板清單

所有的模板將繼承自最層的 `base.html`，以保持外觀一致。

- `templates/base.html`：基底模板，包含 Header & Footer。
- `templates/index.html`：首頁。
- `templates/auth/`
  - `login.html`：登入頁面
  - `register.html`：註冊頁面
  - `profile.html`：會員中心頁面
- `templates/recipe/`
  - `index.html`：食譜列表與總覽
  - `detail.html`：單筆食譜頁面
  - `new.html`：新增食譜頁面
  - `edit.html`：編輯食譜頁面
- `templates/search/`
  - `index.html`：搜尋首頁 / 冰箱尋寶輸入
  - `results.html`：搜尋結果清單
