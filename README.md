# google-oauth-demo

## 如何啟用此專案？
1. 準備好 Docker 環境

   專案中已有定義好各自的 Dockerfile 與 docker-compose.yaml，供大家即開即用，所以要先準備好你的 Docker 環境。
   
2. 到 Google OAuth 註冊你的應用

   會需要你們先到 [Google Cloud Console](https://console.developers.google.com/) 上建立屬於自己的 OAuth 2.0 憑證。  
   從「API 和服務」->「憑證」->「+建立憑證」->「OAuth 用戶端 ID」去建立屬於自己的 OAuth 2.0 憑證。
   - 應用程式類型填「網頁應用程式」
   - 名稱隨便你填
   - 已授權的 JavaScript 來源填「http://localhost:3000」
   - 已授權的重新導向 URI 填「http://localhost:3000/callback」
    
   建立完後，就能在頁面右半部找到屬於你的「用戶端編號（CLIENT_ID）」和「用戶端密鑰（CLIENT_SECRET）」。

3. 將 CLIENT_ID 和 CLIENT_SECRET 填到專案中

   前端只要填 CLIENT_ID，搜尋一下 googleClientId 關鍵字，並將它改成你的 ID 即可。  
   後端則是使用 .env 文件來管理，首先先將 backend 目錄下的 .env.sample 改名為 .env，然後填寫其中的 GOOGLE_CLIENT_ID 與 GOOGLE_CLIENT_SECRET 即可。

4. 啟動專案

   在專案根目錄中，執行 `docker compose up` 即可。

5. 測試網站

   打開瀏覽器並前往 `http://localhost:3000/`，就可以開始 Demo 了。


## OAuth 流程圖
```mermaid
sequenceDiagram

participant 使用者
participant 前端 as 網頁前端
participant 後端 as 網頁後端
participant 授權伺服器
participant 資源伺服器

rect rgba(0, 0, 255, .1)
	使用者->>前端: 1.點擊登入
	前端->>授權伺服器: 2.發送授權請求（/oauth/authorize）
	授權伺服器->>使用者: 3.跳轉至授權伺服器頁面， <br> 以供使用者操作
	使用者->>授權伺服器: 4.輸入身份驗證資訊，並授權
	授權伺服器->>前端: 5.跳轉至 Redirect URI，<br> 並夾帶著 Authorization Code 和 State（可選）
	前端-->>前端: 若授權請求有帶 State 的話，<br> 會驗證 Redirect 回來的 State 是否相同
	前端->>後端: 6.將 Authorization Code 傳給後端，<br>因為 Access Token 較私密，要由後端來獲取
end
rect rgba(0, 255, 0, .1)
	後端->>授權伺服器: 7.根據 Authorization Code，<br>去發送令牌請求（/oauth/token）
	授權伺服器->>授權伺服器: 8.驗證 Authorization Code 與 Client ID
	授權伺服器->>後端: 9.成功後，返回 Access Token
	後端->>資源伺服器: 10.使用 Access Token 取得所需信息
	資源伺服器->>後端: 11.返回所需信息
	後端-->>後端: 12.產出自身應用的憑證（如 Session ID 或 JWT）
end
rect rgba(0, 0, 255, .1)
	後端->>前端: 13.回傳我們的 Session ID 或 JWT 給前端
	前端-->>後端: 14.帶上我們的憑證呼叫業務 API
end
```
