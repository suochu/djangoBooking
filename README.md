# 專案名稱

專案名稱：愛旅行
主要目的：旅遊、創作性質很貼近我內心，想練習將嗜好與程式開發專業連結在一起。


## 專案基本資料

在這裡提供專案的基本資訊，如作者、許可證、版本號等。

## 功能介紹


案例圖

訪客：網站的未註冊用戶。<br />
註冊用戶：已註冊並登錄的用戶。<br />
管理員：具有管理網站內容和訂單的權限的用戶。<br />

<img width="636" alt="截圖 2024-03-01 下午11 13 27" src="https://github.com/suochu/djangoBooking/assets/89134683/ea4468f0-0210-4165-a957-9e875706e2b2">



數據模型圖

<img width="794" alt="截圖 2024-03-01 下午9 20 21" src="https://github.com/suochu/djangoBooking/assets/89134683/4c1dabb6-f917-4e0e-9dfa-cc773b5f3ae0">

已開發功能
1. **用戶註冊與個人資料創建** - 為用戶提供註冊並創建個人資料的能力是基礎設施的一部分，這是進行任何預訂之前的必要條件。
2. **添加新的房間信息** - 在用戶能夠預訂之前，系統中需要有房間數據。這是供應方面的基礎。
3. **房間列表與詳情頁面** - 允許用戶瀏覽房間並查看詳細信息是核心功能，用戶基於這些信息做出預訂決策。
4. **顯示房間可用性** - 為用戶提供實時的房間可用性信息，以幫助他們做出決策。
5. **創建新的預訂** - 允許用戶基於他們的需求（如日期、人數等）進行房間預訂。
6. **預訂查詢** - 使用戶能夠查看他們的預訂記錄，包括即將到來和歷史預訂。
7. **取消預訂** - 提供一個簡單的方式讓用戶取消他們的預訂，這是基本的客戶服務功能。

欲開發功能
1. **更新用戶個人資料** - 允許用戶更新他們的個人信息，如聯繫方式或密碼。
2. **修改預訂信息** - 用戶可能需要更改他們的預訂細節，如日期或取消預訂。
3. **更新房間詳情** - 允許房東或管理員更新房間的詳細信息，以保持信息的準確性和最新性。
4. **刪除用戶評論** - 為管理員提供刪除不恰當或過時評論的能力，以維護網站質量。
5. **移除房間列表** - 讓管理員或房東能夠從系統中移除不再提供的房間。
6. **用戶評論展示** - 展示用戶評論可以增加透明度並幫助其他用戶做出更好的預訂決策。
7. **個性化房間推薦** - 根據用戶的瀏覽和預訂歷史來推薦房間，這是增加用戶滿意度和提高轉化率的高級功能。


## 使用教學

登入會員執行預訂
1. 步驟一：登入
2. 步驟二：以設施服務條件篩選
3. 步驟三：輸入入住日期、退房日期、房型找到空房
4. 步驟四：按下查看詳情
5. 步驟五：查看房內設施
6. 步驟六：按下立即下訂
7. 步驟七：buy now
8. 步驟八：交易款項由paypal處理
9. 專案操作影片
<br />[![未登入會員執行預訂](https://img.youtube.com/vi/bkpNEjA0BkM/0.jpg)](https://www.youtube.com/watch?v=bkpNEjA0BkM)


未登入會員執行預訂-降低用戶預訂房間的障礙，增加頁面轉換率
1. 步驟一：以設施服務條件篩選
2. 步驟二：輸入入住日期、退房日期、房型找到空房
3. 步驟三：按下查看詳情
4. 步驟四：查看房內設施
5. 步驟五：無會員下訂
6. 步驟六：輸入個人資料，按下最後預定確認
7. 步驟七：交易款項由paypal處理
8. 專案操作影片
<br />[![未登入會員執行預訂](https://img.youtube.com/vi/DROtUmNnnPs/0.jpg)](https://www.youtube.com/watch?v=DROtUmNnnPs)




## 涵蓋的技術

- django
- bootstrap
- chatgpt4

## 技術亮點

在這裡突顯一些您認為特別重要或有趣的技術亮點或其他相關資訊。

- 亮點 1：串接第三方支付服務paypal處理交易



