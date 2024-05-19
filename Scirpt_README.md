# Drawing Competition Backend Script

> Author FKT

---

## Basic Knowledge


Call Script Format
呼叫腳本的基本指令格式

```shell
python manage.py <Script_Name>
```

---

### Generate Team 生成小隊

automatic generate 10 teams with distinct token
自動產生 10 個小隊，並生成對應的獨有 Token

```shell
python manage.py generate_team
```

---

### Generate Round 生成回合

automatic generate 5 rounds with CONSTANTS 
自動生成 5 個回合，回合會根據以下**常數**進行生成

- ROUND_START_HOUR = 14  # 回合開始時間-小時
- ROUND_START_MINUTE = 0  # 回合開始時間-分鐘
- ROUND_PLAY_TIME = 30  # 回合時間長度-分鐘
- ROUND_GAP_TIME = 10  # 回合間隔時間-分鐘

For according example CONSTANTS the first round will start from 14:30 and every round continue with 30 minutes and each rounds has 10 minutes gap time

用上面的常數來舉例，第一個回合會從 14:30 開始，每個回合持續 30 分鐘，且每個回合之間會間隔 10 分鐘。

```shell
python manage.py generate_round
```

---

### Generate Challenge 生成挑戰

automatic generate 10 challenges with images and store in project media
自動生成 10 個挑戰與對應圖片，並且存放在專案 media 資料夾

```shell
python manage.py generate_challenge
```

---

### Refresh Round Status 更新回合狀態

refresh all round enable status according current time
根據當前時間去更新所有回合的啟用狀態

```shell
python manage.py refresh_round
```