# Railway Deploy

Bu loyiha Telegram bot bo'lib, `long polling` orqali ishlaydi. Shuning uchun Railway'da `web` servis emas, oddiy `worker` sifatida ishga tushiriladi.

## 1. Railway project yaratish

1. GitHub repo'ni Railway'ga ulang
2. `New Project` -> `Deploy from GitHub Repo`
3. Shu repo'ni tanlang

## 2. Variables

Railway `Variables` bo'limida quyidagilarni kiriting:

```env
BOT_TOKEN=YOUR_BOT_TOKEN_HERE
ADMIN_ID=YOUR_TELEGRAM_NUMERIC_ID
DATA_DIR=/data
```

`ADMIN_ID` ixtiyoriy, lekin admin panel uchun tavsiya qilinadi.

## 3. Persistent volume

SQLite fayl Railway container ichida saqlansa, redeploydan keyin yo'qolishi mumkin. Shuning uchun `Volumes` orqali persistent disk ulang va mount path'ni `/data` qiling.

Saqlanadigan fayllar:

- `/data/mars_intern.db`
- `/data/interns_reports.xlsx`

## 4. Start command

Repo ichida tayyorlangan:

- `Procfile`
- `railway.json`

Start command:

```bash
python main.py
```

## 5. Deploydan keyin tekshirish

Deploy logida quyidagilar chiqishi kerak:

```text
✅ Bot started successfully!
Waiting for messages...
```

Keyin Telegram ichida:

1. `/start`
2. `📚 Dars kiritish`
3. test hisobot yuborish
4. `/admin` bilan admin panelni tekshirish

## Muhim eslatma

`.env.example` ichida ilgari haqiqiy token bor edi. Uni darhol BotFather orqali `revoke` qilib, yangi token olish kerak.
