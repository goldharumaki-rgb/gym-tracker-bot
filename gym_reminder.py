import urllib.request
import json
import datetime
import os
import time

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

BASE_URL = "https://github.com/goldharumaki-rgb/gym-tracker-bot/raw/main"

LATIHAN = {
    'Push Day': [
        {
            'nama': 'Bench Press',
            'detail': '4 set × 8-10 rep',
            'muscle': 'Dada',
            'tips': 'Punggung rata di bangku. Turunkan bar ke dada perlahan, dorong eksplosif ke atas. Siku 45° dari badan.',
            'foto': f'{BASE_URL}/bench_press.jpg'
        },
        {
            'nama': 'Overhead Press',
            'detail': '3 set × 8-10 rep',
            'muscle': 'Bahu',
            'tips': 'Berdiri tegak, core kencang. Dorong bar lurus ke atas sampai lengan ekstensi penuh.',
            'foto': f'{BASE_URL}/overhead_press.jpg'
        },
        {
            'nama': 'Incline Dumbbell Press',
            'detail': '3 set × 10-12 rep',
            'muscle': 'Dada Atas',
            'tips': 'Sudut bangku 30-45°. Turunkan sampai siku sejajar bahu, tekan ke atas.',
            'foto': f'{BASE_URL}/incline_press.jpg'
        },
        {
            'nama': 'Lateral Raise',
            'detail': '3 set × 12-15 rep',
            'muscle': 'Bahu Samping',
            'tips': 'Angkat ke samping sampai sejajar bahu. Jangan ayun badan. Turunkan 2-3 detik.',
            'foto': f'{BASE_URL}/lateral_raise.jpg'
        },
        {
            'nama': 'Tricep Pushdown',
            'detail': '3 set × 12-15 rep',
            'muscle': 'Tricep',
            'tips': 'Siku tetap di samping badan. Tekan ke bawah sampai lengan lurus, naikan perlahan.',
            'foto': f'{BASE_URL}/tricep_pushdown.jpg'
        },
    ],
    'Pull Day': [
        {
            'nama': 'Pull Up / Lat Pulldown',
            'detail': '4 set × 8-10 rep',
            'muscle': 'Punggung Atas',
            'tips': 'Tarik siku ke bawah dan belakang. Bayangkan menghancurkan sesuatu di ketiak kamu.',
            'foto': f'{BASE_URL}/pull_up.jpg'
        },
        {
            'nama': 'Bent Over Row',
            'detail': '4 set × 8-10 rep',
            'muscle': 'Punggung Tengah',
            'tips': 'Condong 45°, punggung lurus. Tarik bar ke perut bawah. Core kencang.',
            'foto': f'{BASE_URL}/bent_over_row.jpg'
        },
        {
            'nama': 'Face Pull',
            'detail': '3 set × 15 rep',
            'muscle': 'Bahu Belakang',
            'tips': 'Tarik ke arah wajah, siku setinggi bahu. Putar tangan ke luar di akhir gerakan.',
            'foto': f'{BASE_URL}/face_pull.jpg'
        },
        {
            'nama': 'Dumbbell Curl',
            'detail': '3 set × 10-12 rep',
            'muscle': 'Bicep',
            'tips': 'Siku tetap di samping. Curl penuh dari bawah ke atas. Supinasikan tangan di puncak.',
            'foto': f'{BASE_URL}/dumbbell_curl.jpg'
        },
        {
            'nama': 'Hammer Curl',
            'detail': '3 set × 10-12 rep',
            'muscle': 'Bicep & Lengan Bawah',
            'tips': 'Telapak saling berhadapan. Angkat bergantian atau bersamaan dengan kontrol.',
            'foto': f'{BASE_URL}/hammer_curl.jpg'
        },
    ],
    'Legs Day': [
        {
            'nama': 'Squat',
            'detail': '4 set × 8-10 rep',
            'muscle': 'Quad & Glute',
            'tips': 'Kaki selebar bahu, jari sedikit keluar. Turun sampai paha sejajar lantai. Dorong melalui tumit.',
            'foto': f'{BASE_URL}/squat.jpg'
        },
        {
            'nama': 'Romanian Deadlift',
            'detail': '3 set × 10-12 rep',
            'muscle': 'Hamstring',
            'tips': 'Punggung lurus, dorong pinggul ke belakang. Rasakan tarikan kuat di belakang paha.',
            'foto': f'{BASE_URL}/romanian_deadlift.jpg'
        },
        {
            'nama': 'Leg Press',
            'detail': '3 set × 12 rep',
            'muscle': 'Quad',
            'tips': 'Kaki atas = hamstring/glute, kaki bawah = quad. Jangan kunci lutut di atas.',
            'foto': f'{BASE_URL}/leg_press.jpg'
        },
        {
            'nama': 'Leg Curl',
            'detail': '3 set × 12-15 rep',
            'muscle': 'Hamstring',
            'tips': 'Curl kaki ke atas perlahan. Tahan 1 detik di atas, turunkan 2-3 detik.',
            'foto': f'{BASE_URL}/leg_curl.jpg'
        },
        {
            'nama': 'Calf Raise',
            'detail': '4 set × 15-20 rep',
            'muscle': 'Betis',
            'tips': 'Angkat setinggi mungkin, tahan 1 detik. Turunkan sampai tumit di bawah platform.',
            'foto': f'{BASE_URL}/calf_raise.jpg'
        },
    ]
}

def kirim_pesan(teks):
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    data = json.dumps({
        'chat_id': CHAT_ID,
        'text': teks,
        'parse_mode': 'Markdown'
    }).encode()
    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
    res = urllib.request.urlopen(req)
    return json.loads(res.read())

def kirim_foto(foto_url, caption):
    url = f'https://api.telegram.org/bot{TOKEN}/sendPhoto'
    data = json.dumps({
        'chat_id': CHAT_ID,
        'photo': foto_url,
        'caption': caption,
        'parse_mode': 'Markdown'
    }).encode()
    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
    try:
        res = urllib.request.urlopen(req)
        result = json.loads(res.read())
        if not result.get('ok'):
            print(f'Foto gagal: {result}')
        return result
    except Exception as e:
        print(f'Error foto: {e}')
        return None

def get_jadwal_hari():
    now = datetime.datetime.utcnow() + datetime.timedelta(hours=9)
    return now, JADWAL[now.weekday()]

def reminder_pagi():
    now, (nama, emoji) = get_jadwal_hari()
    hari_str = now.strftime('%A, %d %B %Y')

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
        kirim_pesan(msg)
    else:
        latihannya = LATIHAN[nama]
        daftar = '\n'.join([f'⬜ *{l["nama"]}* — {l["detail"]} ({l["muscle"]})' for l in latihannya])

        msg = f"""🌅 *Selamat Pagi, Ali!*

📅 {hari_str}
{emoji} *Jadwal: {nama}*

*Latihan hari ini:*
{daftar}

🔥 Ayo semangat! Setiap rep membentuk tubuhmu!
⏰ Warm up 5-10 menit dulu ya!"""
        kirim_pesan(msg)
        time.sleep(1)

        for i, ex in enumerate(latihannya, 1):
            caption = f"""*{i}. {ex['nama']}*
🎯 Otot: *{ex['muscle']}*
📊 {ex['detail']}

💡 *Tips teknik:*
{ex['tips']}"""
            kirim_foto(ex['foto'], caption)
            time.sleep(2)

    print(f"✅ Reminder pagi terkirim — {nama}")

def reminder_malam():
    now, (nama, emoji) = get_jadwal_hari()
    hari_str = now.strftime('%A, %d %B %Y')

    if nama == 'Istirahat':
        msg = f"""🌙 *Rekap Malam — Ali*

📅 {hari_str}
{emoji} Hari istirahat selesai!

Semoga tubuhmu sudah recovery dengan baik.
Besok siap latihan lagi! 💪
Tidur yang cukup malam ini! 🛌"""
    else:
        latihannya = LATIHAN[nama]
        daftar = '\n'.join([f'⬜ {l["nama"]} — {l["detail"]}' for l in latihannya])
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
    print(f"✅ Rekap malam terkirim — {nama}")

if __name__ == '__main__':
    import sys
    mode = sys.argv[1] if len(sys.argv) > 1 else 'pagi'
    if mode == 'pagi':
        reminder_pagi()
    elif mode == 'malam':
        reminder_malam()
    print('Selesai!')
