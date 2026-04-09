# 系統架構設計：食譜收藏夾

## 1. 技術架構說明

### 選用技術與原因
- **後端運算**：Python 3 + Flask。Flask 輕量且容易上手，適合快速建構具有食譜增刪改查 (CRUD) 與進階搜尋邏輯的網站。
- **資料庫管理**：SQLite。免安裝架設伺服器，對個人開發或是小型網站來說十分便利，能順暢處理使用者與食譜間的關聯資料。
- **畫面呈現**：HTML / CSS + Jinja2 模板引擎。採用伺服器渲染頁面，前後端不會分離，架構相對單純直覺。CSS 可採用原生的 Vanilla CSS 或引入輕量的 CDN 框架（如 Bootstrap）協助 RWD 版面。

### Flask MVC 模式說明
雖然我們不拆分前後端，但仍運用 MVC（Model-View-Controller）的設計概念來維持程式碼的整潔：
- **Model (資料模型)**：負責定義資料結構與操作資料庫的對象，例如 `User`、`Recipe`、`Ingredient`。
- **View (視圖)**：負責呈現給使用者的畫面介面，也就是我們寫在 `templates/` 裡的 `.html` 檔案 (含有 Jinja2 語法)。
- **Controller (控制器)**：由 Flask 的路由 (Route) 負責。當收到來自瀏覽器的請求時，路由會向 Model 取得或更新資料，然後把資料傳遞給 View 進行渲染，最後把生好的 HTML 結果吐給使用者。

---

## 2. 專案資料夾結構

本專案預計採用的原始碼結構如下圖所示：

```text
web_app_development/
├── app.py                 # Flask 應用程式的入口檔案
├── requirements.txt       # Python 套件相依清單 (Flask 等)
├── docs/                  # 專案文件目錄
│   ├── PRD.md             # 產品需求文件
│   └── ARCHITECTURE.md    # 系統架構設計文件 (本文件)
├── instance/              # 放機器本地資訊的目錄 (預設不用上傳版控)
│   └── database.db        # SQLite 資料庫檔案
└── app/                   # 主程式邏輯與資源
    ├── __init__.py        # 讓 app 成為 Python package，並初始化 Flask instance
    ├── models/            # 資料庫模型 (Models)
    │   ├── user.py        # 處理使用者邏輯
    │   ├── recipe.py      # 處理食譜邏輯
    │   └── ingredient.py  # 處理食材與關聯邏輯
    ├── routes/            # 路由設計 (Controllers)
    │   ├── auth.py        # 註冊登入與會員路由
    │   ├── recipe.py      # 食譜瀏覽、新增與編輯路由
    │   └── search.py      # 食材搜尋演算法的路由
    ├── static/            # 靜態資源檔案
    │   ├── css/
    │   │   └── style.css  # 自訂樣式表
    │   ├── js/
    │   │   └── main.js    # 各式前端互動 (如防呆、提示等)
    │   └── images/        # 食譜圖或預設圖放置處 (初期可直接儲存於此)
    └── templates/         # Jinja2 HTML 樣板 (Views)
        ├── base.html      # 最基礎的共同排版樣板 (包含 Header/Footer)
        ├── index.html     # 首頁
        ├── auth/          # 註冊/登入視圖
        └── recipe/        # 食譜相關視圖
```

---

## 3. 元件關係圖

以下圖示呈現了整個系統在接收到使用者瀏覽或送出表單請求時的資料流向關係：

```mermaid
graph TD
    User([網頁瀏覽器 (使用者)]) -->|HTTP 請求 (GET/POST)| Router[Flask 路由 (Controller)]
    
    subgraph "Flask 後端"
        Router -->|1. 查詢或修改資料| Model[資料模型 (Model)]
        Model -->|2. 回傳或確認| Router
        Router -->|3. 傳遞資料並渲染此視圖| View[Jinja2 模板 (View)]
    end
    
    Model <-->|SQL 語法/ORM 操作| DB[(SQLite 資料庫)]
    View -->|4. 將產生的 HTML 傳回| User
```

---

## 4. 關鍵設計決策

1. **不拆分前後端的 Monolithic 架構 (單體式)**  
   * **原因**：為了在有限的時間與開發資源下，快速產生 MVP 原型供驗證，並避免同時維護兩套系統（與其通訊 API）。利用 Jinja2 在後端渲染好頁面，可以減少初學者在處理 AJAX 與非同步請求時碰到的麻煩。

2. **目錄結構化與模組化 (Blueprints 概念)**  
   * **原因**：即便系統不大，但把所有的路徑設定與資料庫邏輯全塞入單一檔案將很快變得難以維護。因此設計了 `models/`, `routes/`, `templates/` 分離關注點 (Separation of Concerns)，有助於未來的職責切分與程式碼擴充。

3. **食材組合搜尋機制的實作策略**  
   * **原因**：因應此專案「透過擁有的多項食材，找尋可做料理」的最大特色。資料庫設計必須重視食材標籤與食譜之間的關聯結構。我們將在 `search.py` 中集中處理跨表的查詢演算法，以此切開複雜的商業邏輯與一般視圖呈現。

4. **採用原生技術與輕量工具**  
   * **原因**：不依賴龐大的 JavaScript 框架 (如 React) 來建置介面，能以更純粹的 HTML / Vanilla CSS 來實作出流暢且直覺乾淨的環境。
