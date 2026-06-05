import urllib.request
import json
import datetime
import os
import time
import uuid

TOKEN = os.environ.get('TELEGRAM_TOKEN', '')
CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID', '')

# Mon=0, Tue=1, Wed=2, Thu=3, Fri=4, Sat=5, Sun=6
JADWAL = {
    0: ('Upper Body', '💪'),
    1: ('Rest Day', '😴'),
    2: ('Core', '🔥'),
    3: ('Rest Day', '😴'),
    4: ('Lower Body', '🦵'),
    5: ('Rest Day', '😴'),
    6: ('Rest Day', '😴')
}

LATIHAN = {
    'Upper Body': [
        {
            'nama': 'Bench Press',
            'detail': '4 sets × 8-10 reps',
            'muscle': 'Dada, Trisep, Bahu Depan',
            'tips': '🔹 COMPOUND #1\nRetract scapula, slight arch. Lower bar to lower chest over 3 sec. Drive explosively up. Rest 60-90 sec between sets.',
            'foto': 'bench_press.jpg'
        },
        {
            'nama': 'Bent-over Barbell Row',
            'detail': '4 sets × 8-10 reps',
            'muscle': 'Punggung Lebar, Bisep',
            'tips': '🔹 COMPOUND #2\nHinge 45°, brace core hard. Pull bar to belly button. Squeeze lats 1 sec at top. Lower slowly 3 sec. Rest 60-90 sec.',
            'foto': 'bent_over_row.jpg'
        },
        {
            'nama': 'Overhead Press (OHP)',
            'detail': '3 sets × 10 reps',
            'muscle': 'Bahu, Trisep',
            'tips': '🔹 COMPOUND #3\nBar at clavicle, press slightly back overhead. Full lockout at top. Lower over 3 sec. Keep core tight throughout.',
            'foto': 'overhead_press.jpg'
        },
        {
            'nama': 'Pull-up / Lat Pulldown',
            'detail': '3 sets × 8-12 reps',
            'muscle': 'Latissimus Dorsi, Bisep',
            'tips': '🔹 COMPOUND #4\nFull range — dead hang to chin over bar. Pull elbows down and back. Squeeze lats hard at bottom. Control lowering 3 sec.',
            'foto': 'pull_up.jpg'
        },
        {
            'nama': 'Curl + Tricep Pushdown',
            'detail': '3 sets × 12 reps each',
            'muscle': 'Bisep, Trisep (isolasi)',
            'tips': '🔹 SUPERSET\nDo curls immediately followed by pushdown — no rest between.\n• Curl: supinate at top, slow 3 sec lowering\n• Pushdown: elbows locked at sides, squeeze hard at lockout\nRest 60 sec after each superset.',
            'foto': 'dumbbell_curl.jpg'
        },
    ],
    'Core': [
        {
            'nama': 'Plank',
            'detail': '3 sets × 45-60 seconds',
            'muscle': 'Transverse Abdominis',
            'tips': '🔹 STABILITY\nForearms on floor, body in straight line. Squeeze glutes and abs hard. Do not let hips sag or pike. Breathe steadily throughout.',
            'foto': 'plank.jpg'
        },
        {
            'nama': 'Hanging Leg Raise',
            'detail': '3 sets × 12-15 reps',
            'muscle': 'Lower Abs, Hip Flexors',
            'tips': '🔹 COMPOUND CORE\nHang from bar, posterior pelvic tilt. Raise legs to 90° or higher. Avoid swinging. Lower with full control 3 sec.',
            'foto': 'hanging_leg_raise.jpg'
        },
        {
            'nama': 'Cable Crunch + Russian Twist',
            'detail': '3 sets × 15 reps each',
            'muscle': 'Rectus Abdominis, Oblique',
            'tips': '🔹 SUPERSET\nDo cable crunch immediately followed by Russian twist — no rest between.\n• Cable Crunch: round spine — not hip flex. Squeeze abs hard at bottom.\n• Russian Twist: lean back 45°, feet off floor. Rotate side to side, touch floor each rep.\nRest 60 sec after each superset.',
            'foto': 'cable_crunch.jpg'
        },
        {
            'nama': 'Back Extension / Hyperextension',
            'detail': '3 sets × 12-15 reps',
            'muscle': 'Erector Spinae',
            'tips': '🔹 LOWER BACK\nHinge at hips — not lower back. Rise until body is straight. Hold 1 sec at top. Lower with control 3 sec. Add plate for extra resistance.',
            'foto': 'romanian_deadlift.jpg'
        },
    ],
    'Lower Body': [
        {
            'nama': 'Barbell Back Squat',
            'detail': '4 sets × 6-8 reps',
            'muscle': 'Quad, Glute, Hamstring',
            'tips': '🔹 COMPOUND #1\nBar on traps, feet shoulder-width, toes slightly out. Break hips and knees simultaneously. Hit parallel or below. Drive knees out on way up. Rest 90 sec.',
            'foto': 'squat.jpg'
        },
        {
            'nama': 'Romanian Deadlift (RDL)',
            'detail': '4 sets × 8-10 reps',
            'muscle': 'Hamstring, Glute',
            'tips': '🔹 COMPOUND #2\nPush hips back — not down. Bar stays close to legs. Feel maximum stretch at bottom. Squeeze glutes hard at top. Lower 3 sec. Rest 90 sec.',
            'foto': 'romanian_deadlift.jpg'
        },
        {
            'nama': 'Leg Press + Calf Raise',
            'detail': '3 sets × 12 reps each',
            'muscle': 'Quad, Gastrocnemius',
            'tips': '🔹 SUPERSET\nDo leg press immediately followed by calf raise on the same machine — no rest between.\n• Leg Press: full range, do not lock knees. High wide foot = glutes, low narrow = quads.\n• Calf Raise: rise on big toe, hold 2 sec at top, lower 3 sec.\nRest 90 sec after each superset.',
            'foto': 'leg_press.jpg'
        },
    ]
}

def kirim_pesan(teks):
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    data = json.dumps({'chat_id': CHAT_ID, 'text': teks, 'parse_mode': 'Markdown'}).encode()
    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
    res = urllib.request.urlopen(req)
    return json.loads(res.read())

def kirim_foto_lokal(path_foto, caption):
    if not os.path.exists(path_foto):
        print(f'File not found: {path_foto}')
        return None
    with open(path_foto, 'rb') as f:
        foto_bytes = f.read()
    nama_file = os.path.basename(path_foto)
    boundary = uuid.uuid4().hex
    caption_encoded = caption.encode('utf-8')
    body = (
        f'--{boundary}\r\nContent-Disposition: form-data; name="chat_id"\r\n\r\n{CHAT_ID}\r\n'
        f'--{boundary}\r\nContent-Disposition: form-data; name="parse_mode"\r\n\r\nMarkdown\r\n'
        f'--{boundary}\r\nContent-Disposition: form-data; name="caption"\r\n\r\n'
    ).encode() + caption_encoded + (
        f'\r\n--{boundary}\r\nContent-Disposition: form-data; name="photo"; filename="{nama_file}"\r\nContent-Type: image/jpeg\r\n\r\n'
    ).encode() + foto_bytes + f'\r\n--{boundary}--\r\n'.encode()
    url = f'https://api.telegram.org/bot{TOKEN}/sendPhoto'
    req = urllib.request.Request(url, data=body, headers={'Content-Type': f'multipart/form-data; boundary={boundary}'})
    try:
        res = urllib.request.urlopen(req)
        result = json.loads(res.read())
        if result.get('ok'):
            print(f'✅ {nama_file}')
        else:
            print(f'❌ {result}')
        return result
    except Exception as e:
        print(f'Error: {e}')
        return None

def get_jadwal_hari():
    now = datetime.datetime.utcnow() + datetime.timedelta(hours=9)
    return now, JADWAL[now.weekday()]

def reminder_pagi():
    now, (nama, emoji) = get_jadwal_hari()
    hari_str = now.strftime('%A, %d %B %Y')

    if nama == 'Rest Day':
        msg = f"""🌅 *Good Morning, Ali!*

📅 {hari_str}
{emoji} *Rest Day*

Your body grows during rest — not just during training!
✅ Sleep 7-8 hours
✅ Eat 1.6-2g protein per kg bodyweight
✅ Stay hydrated — minimum 2 liters
✅ Light walk or stretching is fine

*Tip:* Every 4-6 weeks, take a deload week — reduce volume by 40-50% to allow full recovery. 💪"""
        kirim_pesan(msg)

    else:
        latihannya = LATIHAN[nama]
        daftar = '\n'.join([f'⬜ *{l["nama"]}* — {l["detail"]} | _{l["muscle"]}_' for l in latihannya])

        notes = {
            'Upper Body': '💡 Compound first → Superset isolation last\n⏱ Rest 60-90 sec between sets',
            'Core': '💡 Stability → Compound core → Superset → Lower back\n⏱ Rest 60 sec between sets',
            'Lower Body': '💡 Compound first → Superset isolation last\n⏱ Rest 90 sec between sets'
        }

        msg = f"""🌅 *Good Morning, Ali!*

📅 {hari_str}
{emoji} *Today: {nama}*

*3-Day Split — Warmup 5-10 mins first!*

{daftar}

{notes.get(nama, '')}"""

        kirim_pesan(msg)
        time.sleep(1)

        script_dir = os.path.dirname(os.path.abspath(__file__))
        for i, ex in enumerate(latihannya, 1):
            caption = f"""*{i}. {ex['nama']}*
🎯 *{ex['muscle']}*
📊 {ex['detail']}

{ex['tips']}"""
            foto_path = os.path.join(script_dir, ex['foto'])
            kirim_foto_lokal(foto_path, caption)
            time.sleep(2)

    print(f"✅ Morning reminder sent — {nama}")

if __name__ == '__main__':
    reminder_pagi()
    print('Done!')
