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
        {'nama': 'Barbell Bench Press', 'detail': '4 sets × 6-8 reps', 'muscle': 'Chest', 'tips': 'Arch your back slightly, retract scapula. Lower bar to lower chest. Drive through your feet. Control the eccentric.', 'foto': 'bench_press.jpg'},
        {'nama': 'Barbell Row', 'detail': '4 sets × 6-8 reps', 'muscle': 'Mid Back', 'tips': 'Hinge to 45°, brace core hard. Pull bar to your belly button. Squeeze lats at the top. Control the descent.', 'foto': 'bent_over_row.jpg'},
        {'nama': 'Overhead Press', 'detail': '3 sets × 8-10 reps', 'muscle': 'Shoulders', 'tips': 'Bar starts at clavicle. Press bar slightly back overhead. Lock out fully at top. Re-rack with control.', 'foto': 'overhead_press.jpg'},
        {'nama': 'Pull Up (Weighted)', 'detail': '3 sets × 6-10 reps', 'muscle': 'Upper Back & Biceps', 'tips': 'Add weight via belt if bodyweight is easy. Full range — dead hang to chin over bar. Control the lowering phase.', 'foto': 'pull_up.jpg'},
        {'nama': 'Incline Dumbbell Press', 'detail': '3 sets × 10-12 reps', 'muscle': 'Upper Chest', 'tips': 'Bench at 30°. Dumbbells touch at top, wide at bottom. Keep tension on chest throughout.', 'foto': 'incline_press.jpg'},
        {'nama': 'Lateral Raise', 'detail': '3 sets × 15 reps', 'muscle': 'Side Delts', 'tips': 'Slight forward lean. Lead with elbows, not wrists. Pause 1 sec at top. Lower slowly 3 seconds.', 'foto': 'lateral_raise.jpg'},
        {'nama': 'Tricep Pushdown', 'detail': '3 sets × 12-15 reps', 'muscle': 'Triceps', 'tips': 'Keep elbows locked at sides. Full extension at bottom. Squeeze triceps hard at lockout.', 'foto': 'tricep_pushdown.jpg'},
        {'nama': 'Dumbbell Curl', 'detail': '3 sets × 12 reps', 'muscle': 'Biceps', 'tips': 'Supinate at top. No elbow swinging. Slow 3-second lowering for max tension.', 'foto': 'dumbbell_curl.jpg'},
    ],
    'Core': [
        {'nama': 'Hanging Leg Raise', 'detail': '4 sets × 15-20 reps', 'muscle': 'Lower Abs', 'tips': 'Hang from bar, posterior pelvic tilt. Raise legs to 90° or higher. Avoid swinging. Lower with control.', 'foto': 'pull_up.jpg'},
        {'nama': 'Cable Crunch', 'detail': '4 sets × 15-20 reps', 'muscle': 'Upper Abs', 'tips': 'Kneel facing cable. Crunch elbows to knees. Round your spine — do not hip flex. Squeeze abs hard at bottom.', 'foto': 'face_pull.jpg'},
        {'nama': 'Ab Wheel Rollout', 'detail': '3 sets × 10-15 reps', 'muscle': 'Full Core', 'tips': 'Start on knees. Roll out slowly keeping core braced. Go as far as you can without hips dropping. Pull back with abs.', 'foto': 'bench_press.jpg'},
        {'nama': 'Russian Twist (Weighted)', 'detail': '3 sets × 20 reps', 'muscle': 'Obliques', 'tips': 'Lean back 45°, feet off floor. Rotate plate side to side. Touch plate to floor each rep. Control the rotation.', 'foto': 'lateral_raise.jpg'},
        {'nama': 'Plank', 'detail': '3 sets × 60 seconds', 'muscle': 'Deep Core', 'tips': 'Forearms on floor, body straight. Squeeze glutes and abs. Do not let hips sag or pike. Breathe steadily throughout.', 'foto': 'squat.jpg'},
        {'nama': 'Side Plank', 'detail': '3 sets × 45 sec each side', 'muscle': 'Obliques & Lateral Core', 'tips': 'Stack feet or stagger for stability. Drive hip up — do not sag. Keep body in straight line from head to feet.', 'foto': 'lateral_raise.jpg'},
    ],
    'Lower Body': [
        {'nama': 'Barbell Squat', 'detail': '4 sets × 6-8 reps', 'muscle': 'Quads, Glutes & Hamstrings', 'tips': 'Bar on traps, feet shoulder-width. Break at hips and knees simultaneously. Hit parallel or below. Drive knees out on the way up.', 'foto': 'squat.jpg'},
        {'nama': 'Romanian Deadlift', 'detail': '4 sets × 8-10 reps', 'muscle': 'Hamstrings & Glutes', 'tips': 'Push hips back, not down. Bar stays close to legs. Feel max stretch at bottom. Squeeze glutes hard at top.', 'foto': 'romanian_deadlift.jpg'},
        {'nama': 'Bulgarian Split Squat', 'detail': '3 sets × 10-12 reps each leg', 'muscle': 'Quads & Glutes', 'tips': 'Rear foot elevated on bench. Front foot far enough to keep shin vertical. Drop straight down. Lean slightly forward for more glute activation.', 'foto': 'leg_press.jpg'},
        {'nama': 'Leg Press', 'detail': '3 sets × 10-12 reps', 'muscle': 'Quads', 'tips': 'High wide foot position for glutes. Low narrow for quads. Full range — do not lock out knees. Control the lowering.', 'foto': 'leg_press.jpg'},
        {'nama': 'Leg Curl', 'detail': '3 sets × 12-15 reps', 'muscle': 'Hamstrings', 'tips': 'Curl to full contraction. Squeeze hard at top. Lower 3 seconds. Do not let hips rise off pad.', 'foto': 'leg_curl.jpg'},
        {'nama': 'Hip Thrust (Barbell)', 'detail': '3 sets × 12-15 reps', 'muscle': 'Glutes & Bokong', 'tips': 'Upper back on bench, bar on hips. Drive hips up until body is parallel to floor. Squeeze glutes max at top. Chin tucked throughout.', 'foto': 'romanian_deadlift.jpg'},
        {'nama': 'Calf Raise', 'detail': '4 sets × 15-20 reps', 'muscle': 'Calves', 'tips': 'Full stretch at bottom. Rise on big toe. Pause 2 seconds at top. Slow 3-second lowering for maximum growth.', 'foto': 'calf_raise.jpg'},
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

Your body needs recovery today!
✅ Sleep 7-8 hours
✅ Eat enough protein
✅ Stay hydrated — at least 2 liters
✅ Light stretching or walking is fine

You'll come back stronger tomorrow! 💪"""
        kirim_pesan(msg)
    else:
        latihannya = LATIHAN[nama]
        daftar = '\n'.join([f'⬜ *{l["nama"]}* — {l["detail"]} ({l["muscle"]})' for l in latihannya])
        msg = f"""🌅 *Good Morning, Ali!*

📅 {hari_str}
{emoji} *Today: {nama}*

*Workout:*
{daftar}

🔥 Let's get it! Every rep builds a better you!
⏰ Warm up 5-10 minutes first!"""
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
