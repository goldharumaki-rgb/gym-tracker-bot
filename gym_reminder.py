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
    0: ('Rest Day', '😴'),
    1: ('Upper Body', '💪'),
    2: ('Core', '🔥'),
    3: ('Lower Body', '🦵'),
    4: ('Rest Day', '😴'),
    5: ('Rest Day', '😴'),
    6: ('Rest Day', '😴')
}

LATIHAN = {
    'Upper Body': [
        {
            'nama': 'Bench Press',
            'detail': '4 sets × 8-10 reps',
            'muscle': 'Chest, Triceps, Front Delts',
            'tips': 'Retract your scapula, arch slightly. Lower bar to lower chest. Drive through your feet. Control the eccentric for 2-3 seconds.',
            'foto': 'bench_press.jpg'
        },
        {
            'nama': 'Bent-over Barbell Row',
            'detail': '4 sets × 8-10 reps',
            'muscle': 'Upper Back, Biceps',
            'tips': 'Hinge to 45°, brace core. Pull bar to belly button. Squeeze lats at the top. Control the descent slowly.',
            'foto': 'bent_over_row.jpg'
        },
        {
            'nama': 'Overhead Press (OHP)',
            'detail': '3 sets × 10 reps',
            'muscle': 'Shoulders, Triceps',
            'tips': 'Bar starts at clavicle. Press slightly back overhead. Lock out fully at top. Keep core tight throughout.',
            'foto': 'overhead_press.jpg'
        },
        {
            'nama': 'Pull-up / Lat Pulldown',
            'detail': '3 sets × 8-12 reps',
            'muscle': 'Latissimus Dorsi, Biceps',
            'tips': 'Full range — dead hang to chin over bar. Pull elbows down and back. Squeeze lats at the bottom. Control the lowering phase.',
            'foto': 'pull_up.jpg'
        },
        {
            'nama': 'Curl + Tricep Pushdown',
            'detail': '3 sets × 12 reps each',
            'muscle': 'Biceps, Triceps (isolation)',
            'tips': 'Superset: do curls immediately followed by pushdown. Keep elbows locked at sides for both. Squeeze hard at peak contraction.',
            'foto': 'dumbbell_curl.jpg'
        },
    ],
    'Core': [
        {
            'nama': 'Plank',
            'detail': '3 sets × 45-60 seconds',
            'muscle': 'Transverse Abdominis',
            'tips': 'Forearms on floor, body in straight line. Squeeze glutes and abs hard. Do not let hips sag or pike. Breathe steadily throughout.',
            'foto': 'plank.jpg'
        },
        {
            'nama': 'Hanging Leg Raise',
            'detail': '3 sets × 12-15 reps',
            'muscle': 'Lower Abs, Hip Flexors',
            'tips': 'Hang from bar, posterior pelvic tilt. Raise legs to 90° or higher. Avoid swinging. Lower with full control.',
            'foto': 'hanging_leg_raise.jpg'
        },
        {
            'nama': 'Cable Crunch',
            'detail': '3 sets × 15 reps',
            'muscle': 'Rectus Abdominis',
            'tips': 'Kneel facing cable. Crunch elbows to knees. Round your spine — not hip flex. Squeeze abs hard at bottom.',
            'foto': 'cable_crunch.jpg'
        },
        {
            'nama': 'Russian Twist (Weighted)',
            'detail': '3 sets × 15 reps each side',
            'muscle': 'Obliques',
            'tips': 'Lean back 45°, feet off floor. Rotate plate side to side. Touch plate to floor each rep. Control the rotation.',
            'foto': 'russian_twist.jpg'
        },
        {
            'nama': 'Back Extension / Hyperextension',
            'detail': '3 sets × 12-15 reps',
            'muscle': 'Erector Spinae',
            'tips': 'Hinge at hips, not lower back. Rise until body is straight — do not hyperextend. Hold 1 second at top. Lower with control.',
            'foto': 'romanian_deadlift.jpg'
        },
    ],
    'Lower Body': [
        {
            'nama': 'Barbell Back Squat',
            'detail': '4 sets × 6-8 reps',
            'muscle': 'Quads, Glutes, Hamstrings',
            'tips': 'Bar on traps, feet shoulder-width. Break hips and knees simultaneously. Hit parallel or below. Drive knees out on the way up.',
            'foto': 'squat.jpg'
        },
        {
            'nama': 'Romanian Deadlift (RDL)',
            'detail': '4 sets × 8-10 reps',
            'muscle': 'Hamstrings, Glutes',
            'tips': 'Push hips back, not down. Bar stays close to legs. Feel max stretch at bottom. Squeeze glutes hard at the top.',
            'foto': 'romanian_deadlift.jpg'
        },
        {
            'nama': 'Leg Press + Calf Raise',
            'detail': '3 sets × 12 reps each',
            'muscle': 'Quads, Gastrocnemius',
            'tips': 'Superset: leg press full range then immediately calf raise on the same machine. Rise as high as possible on calf raise, hold 1 second at top.',
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
            print(f'✅ Photo sent: {nama_file}')
        else:
            print(f'❌ Failed: {result}')
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
✅ Eat enough protein (1.6-2g per kg bodyweight)
✅ Stay hydrated — at least 2 liters
✅ Light walk or stretching is fine

Come back stronger tomorrow! 💪"""
        kirim_pesan(msg)

    else:
        latihannya = LATIHAN[nama]
        daftar = '\n'.join([f'⬜ *{l["nama"]}* — {l["detail"]}' for l in latihannya])

        notes = {
            'Upper Body': '💡 *Note:* Compound movements first, isolation last. Rest 60-90 sec between sets.',
            'Core': '💡 *Note:* Focus on quality over quantity. Breathe out on every crunch/contraction.',
            'Lower Body': '💡 *Note:* Warm up knees well. Control every rep — especially the eccentric phase.'
        }

        msg = f"""🌅 *Good Morning, Ali!*

📅 {hari_str}
{emoji} *Today: {nama}*

*Workout — 3-Day Split Program:*
{daftar}

{notes.get(nama, '')}
⏰ Warmup 5-10 minutes before starting!"""

        kirim_pesan(msg)
        time.sleep(1)

        script_dir = os.path.dirname(os.path.abspath(__file__))
        for i, ex in enumerate(latihannya, 1):
            caption = f"""*{i}. {ex['nama']}*
🎯 Muscle: *{ex['muscle']}*
📊 {ex['detail']}

💡 *Form tips:*
{ex['tips']}"""
            foto_path = os.path.join(script_dir, ex['foto'])
            kirim_foto_lokal(foto_path, caption)
            time.sleep(2)

    print(f"✅ Morning reminder sent — {nama}")

if __name__ == '__main__':
    reminder_pagi()
    print('Done!')
