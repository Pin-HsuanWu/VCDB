# VCDB - Version Control Database System

## 介紹影片連結
https://drive.google.com/file/d/12skf12dS-oU6YAfCo8nStF_mO_ptHjNT/view?usp=drive_link

## 系統介紹
在現代的軟體開發環境中，多人協作開發是一個十分常見的開發模式。這代表，不同的開發人員可能會在同一時間對資料庫的 Schema 進行修改，以滿足各自的需求。然而，當每個人修改的內容不同時，將這些修改整合到一個共同的資料庫版本就會變得複雜而困難。
在這樣的情況下，需要一個能夠針對資料庫 Schema 進行版本控制的解決方案。然而，現有的版本控制系統主要以檔案系統為基礎，無法直接處理資料庫的 Schema 變化。若開發人員想要針對資料庫的 Schema 進行版本控制，開發人員通常需要手動匯出 SQL 檔，然後使用檔案系統的版本控制工具來管理這些檔案。這種方法不僅繁瑣，而且容易出錯。
鑑於這些需求和難題，我們決定開發一個名為 VCDB 的資料庫版本控制系統。 VCDB 的目標是要提供一個方便、直觀且有效的方法，來管理資料庫 Schema 的版本變化。我們希望透過 VCDB 解決多人協作開發中資料庫 Schema 變化所帶來的挑戰，提高團隊的協作效率，並減少錯誤和衝突的發生。

## 系統架構
在 VCDB 資料庫版本控制系統內，主要可分為四個部分：
- GUI：當使用者要使用 VCDB 這個資料庫版本控制系統時，他必須透過 GUI 介面來選擇他想使用的服務，這個 GUI 介面會是一個簡單且直觀的介面，讓使用者能快速並方便地找到他想要的功能。
- 版本控制服務：VCDB 內提供了多個功能讓使用者使用，包含：commit、hop、checkout、merge 等，當使用者呼叫這些功能後，這些功能就會去影響使用者的 UserDB 以及我們內部使用的 VCDB，其中有些功能會去儲存 UserDB 內的 schema。
- VCDB：這是資料庫版控系統內部所使用的資料庫，內部全部共有四張資料表，分別是 user、branch、commit、merge。
- schema 暫存區：在資料庫版控系統中，有些功能會去儲存 UserDB 內的 schema。這些 schema 就會被放至 schema 暫存區，以供其他功能使用。

## 系統功能
我們將主要功能分為三大類：使用者操作、單一分支操作、跨分支操作。使用者在使用本系統時，會將自己正在使用的資料庫 (以下簡稱 UserDB) 與本系統進行連動，並且針對 UserDB 進行版本控制。
### 使用者操作
- Init：使用者用以連接 UserDB 的初始化功能，需輸入 UserDB 資料庫相關資訊，如使用者帳號密碼、Host、Port 等，即可連動 UserDB 與本系統。
- Register：使用者以姓名、email 作為註冊資料。
- Login：使用者以姓名、email 登入系統，系統會將其紀錄目前位置的版本號與分支號。
### 單一分支操作
- Commit：紀錄 UserDB 當下的資料 Schema。在觸發後會從 UserDB dump 出當下的狀態，並且與前一版本的 Commit 進行比較，產出 Upgrade, Downgrade 的結果，存於 VCDB 的 Commit Table 中。
- Log：印出同一分支的所有 Commit 資訊。
- Hop：在同一分支上切換到不同版本，使用本服務時，系統會根據 Upgrade, Downgrade 語法不斷調整到不同版本。
### 跨分支操作
- Checkout：從該分支切換到其他分支之最新版本。
- Merge：將兩分支之最新版本合併。合併時，系統會先進行衝突判定。對於本系統來說，「新增」表格與欄位皆不被視為衝突，而「更新」、「刪除」表格與欄位皆被視為衝突。合併分支時，若經由衝突判定結果為沒有衝突，則系統會自行合併兩分支。然而，若是有衝突，系統會提供衝突的 SQL script，並且標記兩個分支差異之部分，供使用者調整內容，並且將使用者調整後結果作為兩分支合併後的版本。
- Graph：提供類似 Git Graph 的有向循環圖 (DAG) 供使用者參考目前所有 Commit 版本與分支狀態。

