import requests
import json

BasicInfo = {
  "Format": {
    "standard": "標準",
    "wild": "開放"
  }
}

class CardOverview:
    def __init__(self, id, manaCost, name, amount):
      self.id = id
      self.manaCost = manaCost
      self.name = name
      self.amount = amount

def getDeckInfo(deckCode):
  # deckCode = input("請輸入牌組代碼：")
  # 替換為你所觀察到的目標 API URL
  api_url = 'https://api.blizzard.com/hearthstone/deck?code=' + deckCode + '&locale=zh_TW'

  headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
    'Accept': '*/*',
    'Content-Type': 'application/json',
    'Authorization': 'Bearer KRWpkSRImus70XdDJxtFmU78r8l2hXSIpR'
  }
  # 發送 GET 請求到 API
  response = requests.get(api_url, headers=headers)

  # 確認請求成功
  if response.status_code == 200:
    try:
      # 嘗試解析 JSON 數據
      data = response.json()
      print(data)
      # print(json.dumps(data, indent=4, ensure_ascii=False))
      print(BasicInfo.get("Format").get(data["format"]) + data["class"]["name"] + "牌組")

      # 創建 Card 物件並儲存特定資料
      deckCardsArray = []
      for card in data["cards"]:
        # 在暫存的 list 中找是否已有相同id的卡片物件
        existingCard = next((item for item in deckCardsArray if item.id == card["id"]), None)
        # 若在發現已有相同 id 的卡片物件，則將其 amount+1
        if existingCard:
          existingCard.amount+=1
        # 若沒有，則新增該卡片物件
        else:
          tempCard = CardOverview(card["id"], card["manaCost"], card["name"], 1)
          deckCardsArray.append(tempCard)

      # 將結果寫入文件內確認用
      # with open('result.txt', 'w', encoding='utf-8') as file:
      #   file.write(json.dumps(data, indent=4, ensure_ascii=False))
      #   print("JSON 數據已寫入 result.txt 文件")

      # 將卡片陣列依照消耗費用排序
      deckCardsArray.sort(key=lambda card: card.manaCost)

      # 印出牌組
      for card in deckCardsArray:
        print(str(card.amount) + " × (" + str(card.manaCost) + ")" + card.name)

      # 印出有多個組合的卡片內容(E.g. 齊里亞斯、菁英牛頭大佬)
      if "sideboardCards" in data and len(data["sideboardCards"]) > 0:
        for sideboardCard in data["sideboardCards"]:
          print(sideboardCard["sideboardCard"]["name"])
          if len(sideboardCard["cardsInSideboard"]) > 0:
            for cardsInSideboard in sideboardCard["cardsInSideboard"]:
              print("  (" + str(cardsInSideboard["manaCost"]) + ")" + cardsInSideboard["name"])
      print("1231313132123")
      return data
    except requests.exceptions.JSONDecodeError:
      print("響應內容不是有效的 JSON")
      print("響應文本內容:", response.text)

  else:
    print(f"請求失敗，狀態碼：{response.status_code}")