import urllib.request
import json
import datetime
import os

TOKEN = os.environ.get('TELEGRAM_TOKEN', '')
CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID', '')

JADWAL = {
    0: ('Push Day', '🔴'),
    1: ('Pull Day', '🟢'),
    2: ('Legs Day', '🟠'),
    3: ('Push Day', '🔴'),
    4: ('Pull Day', '🟢'),
    5: ('Istirahat', '😴'),
    6: ('Istirahat', '😴')
}

LATIHAN = {
    'Push Day': [
        'Bench Press — 4×8-10 rep',
        'Overhead Press — 3×8-10 rep',
        'Incline Dumbbell Press — 3×10-12 rep',
        'Lateral Raise — 3×12-15 rep',
        'Tricep Pushdown — 3×12-15 rep'
    ],
    'Pull Day': [
        'Pull Up / Lat Pulldown — 4×8-10 rep',
        'Bent Over Row — 4×8-10 rep',
        'Face Pull — 3×15 rep',
        'Dumbbell Curl — 3×10-12 rep',
        'Hammer Curl — 3×10-12 rep'
    ],
    'Legs Day': [
        'Squat — 4×8-10 rep',
        'Romanian Deadlift — 3×10-12 rep',
        'Leg Press — 3×12 rep',
        'Leg Curl — 3×12-15 rep',
        'Calf Raise — 4×15-20 rep'
    ]
}

def kirim_pesan(teks):
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    data = json.dumps({
        'chat_id': CHAT_ID,
        'text': teks,
        'parse_mode': 'Markdown'
    }).encode()
    req = urllib.request.Request(
        url, data=data,
        headers={'Content-Type': 'application/json'}
    )
    res = urllib.request.urlopen(req)
    hasil = json.loads(res.read())
    print('Pesan terkirim!' if hasil['ok'] else f'Gagal: {hasil}')
    return hasil

def reminder_pagi():
    now = datetime.datetime.utcnow()
    # UTC+9 (Yokohama/Japan)
    now_local = now + datetime.timedelta(hours=9)
    dow = now_local.weekday()
    nama, emoji = JADWAL[dow]
    hari_str = now_local.strftime('%A, %d %B %Y')

    if nama == 'Istirahat':
        msg = f"""🌅 *Selamat Pagi, Ali!*

📅 {hari_str}
{emoji} *Hari Istirahat*

Tubuhmu butuh recovery hari ini!
✅ Tidur cukup 7-8 jam
✅ Makan protein yang cukup
✅ Minum air minimal 2 liter
✅ Stretching ringan boleh

Besok kamu akan lebih kuat! 💪"""
    else:
        daftar = '\n'.join([f'⬜ {l}' for l in LATIHAN[nama]])
        msg = f"""🌅 *Selamat Pagi, Ali!*

📅 {hari_str}
{emoji} *Jadwal: {nama}*

*Latihan hari ini:*
{daftar}

🔥 Ayo semangat! Setiap rep membentuk tubuhmu!
⏰ Jangan lupa warm up 5-10 menit dulu!"""

    kirim_pesan(msg)

def reminder_malam():
    now = datetime.datetime.utcnow()
    now_local = now + datetime.timedelta(hours=9)
    dow = now_local.weekday()
    nama, emoji = JADWAL[dow]
    hari_str = now_local.strftime('%A, %d %B %Y')

    if nama == 'Istirahat':
        msg = f"""🌙 *Rekap Malam — Ali*

📅 {hari_str}
{emoji} Hari istirahat selesai!

Semoga tubuhmu sudah recovery dengan baik.
Besok siap latihan lagi! 💪
Tidur yang cukup malam ini! 🛌"""
    else:
        daftar = '\n'.join([f'⬜ {l}' for l in LATIHAN[nama]])
        msg = f"""🌙 *Rekap Malam — Ali*

📅 {hari_str}
{emoji} Jadwal tadi: *{nama}*

Checklist latihan:
{daftar}

Sudah selesai semua? 
Jangan lupa:
✅ Makan protein setelah latihan
✅ Minum air yang cukup
✅ Tidur 7-8 jam untuk recovery 🛌"""

    kirim_pesan(msg)

if __name__ == '__main__':
    import sys
    mode = sys.argv[1] if len(sys.argv) > 1 else 'pagi'
    if mode == 'pagi':
        reminder_pagi()
    elif mode == 'malam':
        reminder_malam()
    print('Selesai!')
