import urllib.request
import json
import datetime
import os
import time
import uuid

TOKEN = os.environ.get('TELEGRAM_TOKEN', '')
CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID', '')

JADWAL = {
    0: ('Push Day', '🔴'),
    1: ('Pull Day', '🟢'),
    2: ('Legs Day', '🟠'),
    3: ('Push Day', '🔴'),
    4: ('Pull Day', '🟢'),
    5: ('Rest Day', '😴'),
    6: ('Rest Day', '😴')
}

LATIHAN = {
    'Push Day': [
        {'nama': 'Bench Press', 'detail': '4 sets × 8-10 reps', 'muscle': 'Chest', 'tips': 'Keep your back flat on the bench. Lower the bar slowly to your chest, then drive it up explosively. Keep elbows at 45° from your body.', 'foto': 'bench_press.jpg'},
        {'nama': 'Overhead Press', 'detail': '3 sets × 8-10 reps', 'muscle': 'Shoulders', 'tips': 'Stand tall, brace your core. Press the bar straight up until arms are fully extended. Avoid arching your lower back.', 'foto': 'overhead_press.jpg'},
        {'nama': 'Incline Dumbbell Press', 'detail': '3 sets × 10-12 reps', 'muscle': 'Upper Chest', 'tips': 'Set bench at 30-45°. Lower dumbbells until elbows are at shoulder height, then press up and squeeze at the top.', 'foto': 'incline_press.jpg'},
        {'nama': 'Lateral Raise', 'detail': '3 sets × 12-15 reps', 'muscle': 'Side Delts', 'tips': 'Raise dumbbells to shoulder height. Do not swing your body. Lower slowly over 2-3 seconds.', 'foto': 'lateral_raise.jpg'},
        {'nama': 'Tricep Pushdown', 'detail': '3 sets × 12-15 reps', 'muscle': 'Triceps', 'tips': 'Keep elbows tucked at your sides. Push down until arms are fully straight, then slowly return.', 'foto': 'tricep_pushdown.jpg'},
    ],
    'Pull Day': [
        {'nama': 'Pull Up / Lat Pulldown', 'detail': '4 sets × 8-10 reps', 'muscle': 'Upper Back', 'tips': 'Pull your elbows down and back. Imagine squeezing something in your armpits as you pull.', 'foto': 'pull_up.jpg'},
        {'nama': 'Bent Over Row', 'detail': '4 sets × 8-10 reps', 'muscle': 'Mid Back', 'tips': 'Hinge at 45°, keep back straight. Pull the bar toward your lower abdomen. Brace your core throughout.', 'foto': 'bent_over_row.jpg'},
        {'nama': 'Face Pull', 'detail': '3 sets × 15 reps', 'muscle': 'Rear Delts', 'tips': 'Pull toward your face with elbows at shoulder height. Rotate hands outward at the end of the movement.', 'foto': 'face_pull.jpg'},
        {'nama': 'Dumbbell Curl', 'detail': '3 sets × 10-12 reps', 'muscle': 'Biceps', 'tips': 'Keep elbows at your sides. Curl fully from bottom to top. Supinate your wrist at the peak.', 'foto': 'dumbbell_curl.jpg'},
        {'nama': 'Hammer Curl', 'detail': '3 sets × 10-12 reps', 'muscle': 'Biceps & Forearms', 'tips': 'Keep palms facing each other throughout. Lift alternately or together with full control.', 'foto': 'hammer_curl.jpg'},
    ],
    'Legs Day': [
        {'nama': 'Squat', 'detail': '4 sets × 8-10 reps', 'muscle': 'Quads & Glutes', 'tips': 'Feet shoulder-width apart, toes slightly out. Squat until thighs are parallel to the floor. Drive through your heels.', 'foto': 'squat.jpg'},
        {'nama': 'Romanian Deadlift', 'detail': '3 sets × 10-12 reps', 'muscle': 'Hamstrings', 'tips': 'Keep back straight, push hips back. Feel the stretch in the back of your thighs as you lower.', 'foto': 'romanian_deadlift.jpg'},
        {'nama': 'Leg Press', 'detail': '3 sets × 12 reps', 'muscle': 'Quads', 'tips': 'High foot position = hamstrings/glutes, low = quads. Never lock your knees at the top.', 'foto': 'leg_press.jpg'},
        {'nama': 'Leg Curl', 'detail': '3 sets × 12-15 reps', 'muscle': 'Hamstrings', 'tips': 'Curl slowly upward. Hold for 1 second at the top, lower over 2-3 seconds.', 'foto': 'leg_curl.jpg'},
        {'nama': 'Calf Raise', 'detail': '4 sets × 15-20 reps', 'muscle': 'Calves', 'tips': 'Rise as high as possible and hold for 1 second. Lower until your heel is below the platform for a full stretch.', 'foto': 'calf_raise.jpg'},
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
        f'--{boundary}\r\n'
        f'Content-Disposition: form-data; name="chat_id"\r\n\r\n'
        f'{CHAT_ID}\r\n'
        f'--{boundary}\r\n'
        f'Content-Disposition: form-data; name="parse_mode"\r\n\r\n'
        f'Markdown\r\n'
        f'--{boundary}\r\n'
        f'Content-Disposition: form-data; name="caption"\r\n\r\n'
    ).encode() + caption_encoded + (
        f'\r\n--{boundary}\r\n'
        f'Content-Disposition: form-data; name="photo"; filename="{nama_file}"\r\n'
        f'Content-Type: image/jpeg\r\n\r\n'
    ).encode() + foto_bytes + f'\r\n--{boundary}--\r\n'.encode()

    url = f'https://api.telegram.org/bot{TOKEN}/sendPhoto'
    req = urllib.request.Request(
        url, data=body,
        headers={'Content-Type': f'multipart/form-data; boundary={boundary}'}
    )
    try:
        res = urllib.request.urlopen(req)
        result = json.loads(res.read())
        if result.get('ok'):
            print(f'✅ Photo {nama_file} sent')
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

Your body needs recovery today!
✅ Sleep 7-8 hours
✅ Eat enough protein
✅ Stay hydrated — at least 2 liters
✅ Light stretching is fine

You'll come back stronger tomorrow! 💪"""
        kirim_pesan(msg)
    else:
        latihannya = LATIHAN[nama]
        daftar = '\n'.join([f'⬜ *{l["nama"]}* — {l["detail"]} ({l["muscle"]})' for l in latihannya])
        msg = f"""🌅 *Good Morning, Ali!*

📅 {hari_str}
{emoji} *Today's Schedule: {nama}*

*Workout for today:*
{daftar}

🔥 Let's get it! Every rep builds a better you!
⏰ Don't forget to warm up for 5-10 minutes first!"""
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
