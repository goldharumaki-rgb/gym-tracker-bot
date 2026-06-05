# 🏋️ Telegram Gym Tracker Bot

An automated gym workout reminder bot built with Python and GitHub Actions. Sends daily morning reminders to Telegram with exercise photos, form tips, and a structured 4-day Upper/Lower split program.

---

## 📱 Preview

The bot sends personalized daily reminders every morning at 06:00 WIB including:
- Today's workout schedule
- Exercise list with sets, reps, and rest times
- Individual exercise photos with form tips
- Progressive overload reminders
- Rest day recovery tips

---

## 🗓 Weekly Schedule

| Day | Session | Focus |
|-----|---------|-------|
| Monday | Upper A 💪🔵 | Strength — heavy compound lifts |
| Tuesday | Lower A 🦵🔵 | Strength + Quad dominant |
| Wednesday | Rest 😴 | Recovery |
| Thursday | Upper B 💪🟣 | Hypertrophy — volume + mind-muscle |
| Friday | Lower B 🦵🟣 | Hypertrophy + Posterior chain |
| Saturday | Rest 😴 | Recovery |
| Sunday | Rest 😴 | Recovery |

---

## 💪 Program Details

### Upper A — Strength (Monday)
| Exercise | Sets × Reps | Muscle |
|----------|-------------|--------|
| Barbell Bench Press | 5 × 5 | Chest, Triceps, Front Delts |
| Bent-over Barbell Row | 5 × 5 | Lats, Rhomboid, Biceps |
| Overhead Press (OHP) | 4 × 6 | Deltoid, Triceps |
| Weighted Pull-up | 4 × 6 | Lats, Biceps |
| Incline Dumbbell Press | 3 × 10-12 | Upper Chest |
| Seated Cable Row | 3 × 12 | Mid-Back, Rear Delt |
| Lateral Raise + Face Pull | 3 × 15 | Side Delts, Rear Delt |
| EZ-bar Curl + Skull Crusher | 3 × 12 | Biceps, Triceps |

### Lower A — Strength + Quad (Tuesday)
| Exercise | Sets × Reps | Muscle |
|----------|-------------|--------|
| Barbell Back Squat | 5 × 5 | Quads, Glutes, Hamstrings |
| Romanian Deadlift (RDL) | 4 × 6-8 | Hamstrings, Glutes |
| Leg Press | 4 × 10-12 | Quads, Glutes |
| Walking Lunge | 3 × 12/leg | Quads, Glutes |
| Leg Curl + Leg Extension | 3 × 15 | Hamstrings, Quads |
| Standing + Seated Calf Raise | 4 × 15-20 | Gastrocnemius, Soleus |
| Plank + Hanging Leg Raise | 3 × 45sec/12 | Core, Lower Abs |

### Upper B — Hypertrophy (Thursday)
| Exercise | Sets × Reps | Muscle |
|----------|-------------|--------|
| Dumbbell Flat Press | 4 × 10-12 | Chest, Triceps |
| Chest-supported T-bar Row | 4 × 10-12 | Mid-Back, Rhomboid |
| Cable Fly (Low to High) | 3 × 15 | Upper Chest, Pec Minor |
| Lat Pulldown (Wide Grip) | 4 × 12 | Lats, Teres Major |
| Arnold Press | 3 × 12 | All Delt Heads |
| Face Pull (Cable) | 4 × 15 | Rear Delt, Rotator Cuff |
| Hammer Curl + Overhead Extension | 3 × 12-15 | Brachialis, Triceps Long Head |
| Cable Curl + Pushdown (Finisher) | 2 × 20 | Biceps, Triceps |

### Lower B — Hypertrophy + Posterior (Friday)
| Exercise | Sets × Reps | Muscle |
|----------|-------------|--------|
| Conventional Deadlift | 4 × 5 | Posterior Chain, Glutes |
| Bulgarian Split Squat | 4 × 10/leg | Quads, Glutes |
| Barbell Hip Thrust | 4 × 12 | Glute Max, Hamstrings |
| Hack Squat / Sissy Squat | 3 × 12 | Quad Sweep, VMO |
| Good Morning / Back Extension | 3 × 12-15 | Hamstrings, Erector Spinae |
| Cable Kickback + Abductor | 3 × 15 | Glute Med, Glute Max |
| Cable Crunch + Russian Twist | 3 × 15 | Abs, Obliques |

---

## 🛠 Tech Stack

- **Language:** Python 3.11
- **Automation:** GitHub Actions (cron job)
- **Messaging:** Telegram Bot API
- **Storage:** GitHub repository (exercise photos)
- **Schedule:** Runs daily at 06:00 WIB (21:00 UTC)

---

## ⚙️ Setup

### 1. Clone this repository
```bash
git clone https://github.com/goldharumaki-rgb/gym-tracker-bot.git
cd gym-tracker-bot
```

### 2. Create a Telegram Bot
- Open Telegram → search `@BotFather`
- Send `/newbot` and follow the instructions
- Copy the bot token

### 3. Get your Chat ID
- Send a message to your bot
- Open: `https://api.telegram.org/bot{TOKEN}/getUpdates`
- Find `"chat":{"id": YOUR_CHAT_ID}`

### 4. Add GitHub Secrets
Go to repo → Settings → Secrets and variables → Actions:
- `TELEGRAM_TOKEN` — your bot token
- `TELEGRAM_CHAT_ID` — your chat ID

### 5. Done!
The bot runs automatically every morning at 06:00 WIB via GitHub Actions.
You can also trigger it manually from the Actions tab.

---

## 📂 Project Structure

```
gym-tracker-bot/
├── gym_reminder.py          # Main bot script
├── .github/
│   └── workflows/
│       └── reminder.yml     # GitHub Actions workflow
├── bench_press.jpg          # Exercise photos (30 total)
├── squat.jpg
├── romanian_deadlift.jpg
└── ...
```

---

## 📈 Progressive Overload Notes

- **Strength lifts (5×5, 4×6):** Add 2.5-5kg when all reps are completed with good form
- **Hypertrophy:** Add weight when you hit the top rep range on all sets
- **Deload:** Every 4-6 weeks, reduce volume by 40-50% for 1 week
- **Protein:** Minimum 1.8-2.2g per kg bodyweight per day

---

## 👤 Author

**Ali Mashar**  
Built as a personal fitness automation project.

---

## 📄 License

MIT License — feel free to fork and customize for your own workout program!
