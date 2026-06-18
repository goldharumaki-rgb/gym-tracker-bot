import urllib.request
import json
import datetime
import os
import time
import uuid

TOKEN = os.environ.get('TELEGRAM_TOKEN', '')
CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID', '')

JADWAL = {
    0: ('Dada + Core', '🫁🔥'),
    1: ('Punggung', '🔙'),
    2: ('Rest Day', '😴'),
    3: ('Bahu', '🤷'),
    4: ('Kaki + Core', '🦵🔥'),
    5: ('Lengan', '💪'),
    6: ('Rest Day', '😴')
}

LATIHAN = {
    'Dada + Core': [
        {'nama': 'Bench Press', 'detail': '4 sets × 6-10 reps', 'muscle': 'Dada, Trisep, Bahu Depan', 'tips': 'Retract scapula, slight arch. Lower bar to lower chest over 3 sec. Drive explosively up.\n\n📌 Opsi: Dumbbell Bench Press', 'foto': 'bench_press.jpg'},
        {'nama': 'Incline Dumbbell Press', 'detail': '4 sets × 8-12 reps', 'muscle': 'Dada Atas, Bahu Depan', 'tips': 'Bench at 30°. Lower until elbows at shoulder height. Squeeze chest at top. Tempo 2-1-2.\n\n📌 Opsi: Incline Machine Press', 'foto': 'incline_press.jpg'},
        {'nama': 'Chest Fly', 'detail': '3 sets × 10-15 reps', 'muscle': 'Dada (isolasi)', 'tips': 'Slight elbow bend, arc the weights together. Squeeze pecs hard at top. Feel the stretch at bottom.\n\n📌 Opsi: Pec Deck Machine', 'foto': 'cable_fly.jpg'},
        {'nama': 'Push-up', 'detail': '3 sets × semampunya', 'muscle': 'Dada, Trisep, Core', 'tips': 'Hands slightly wider than shoulders. Lower chest to floor. Keep body in straight line. Push up explosively.\n\n📌 Opsi: Chest Press Machine', 'foto': 'push_up.jpg'},
        {'nama': 'Plank', 'detail': '3 sets × 60 seconds', 'muscle': 'Core (Transverse Abdominis)', 'tips': 'Forearms on floor, body in straight line. Squeeze glutes and abs hard. Breathe steadily.\n\n📌 Opsi: Dead Bug', 'foto': 'plank.jpg'},
        {'nama': 'Hanging Leg Raise', 'detail': '3 sets × 12-15 reps', 'muscle': 'Lower Abs, Hip Flexors', 'tips': 'Hang from bar, posterior pelvic tilt. Raise legs to 90° or higher. Avoid swinging.\n\n📌 Opsi: Lying Leg Raise', 'foto': 'hanging_leg_raise.jpg'},
        {'nama': 'Crunch', 'detail': '3 sets × 20 reps', 'muscle': 'Rectus Abdominis', 'tips': 'Hands behind head, knees bent. Curl shoulders off floor. Squeeze abs hard at top.\n\n📌 Opsi: Cable Crunch', 'foto': 'crunch.jpg'},
    ],
    'Punggung': [
        {'nama': 'Lat Pulldown', 'detail': '4 sets × 8-12 reps', 'muscle': 'Lats, Bisep', 'tips': 'Wide overhand grip. Pull bar to upper chest. Lean back slightly. Squeeze lats hard at bottom.\n\n📌 Opsi: Assisted Pull-up', 'foto': 'pull_up.jpg'},
        {'nama': 'Barbell Row', 'detail': '4 sets × 8-12 reps', 'muscle': 'Mid-Back, Lats, Bisep', 'tips': 'Hinge 45°, brace core hard. Pull bar to belly button. Squeeze lats 1 sec at top.\n\n📌 Opsi: T-Bar Row', 'foto': 'bent_over_row.jpg'},
        {'nama': 'Seated Cable Row', 'detail': '3 sets × 10-12 reps', 'muscle': 'Mid-Back, Rear Delt', 'tips': 'Sit tall, chest up. Pull handle to lower chest. Squeeze shoulder blades together.\n\n📌 Opsi: Chest Supported Row', 'foto': 'seated_cable_row.jpg'},
        {'nama': 'Dumbbell Row', 'detail': '3 sets × 10 reps/sisi', 'muscle': 'Mid-Back, Lats, Bisep', 'tips': 'One arm at a time. Pull elbow back and up. Squeeze shoulder blade at top.\n\n📌 Opsi: Machine Row', 'foto': 'bent_over_row.jpg'},
        {'nama': 'Face Pull', 'detail': '3 sets × 12-15 reps', 'muscle': 'Rear Delt, Rotator Cuff, Trap', 'tips': 'Pull toward face, elbows at shoulder height. Rotate hands outward at end.\n\n📌 Opsi: Reverse Pec Deck', 'foto': 'face_pull.jpg'},
    ],
    'Bahu': [
        {'nama': 'Overhead Press', 'detail': '4 sets × 6-10 reps', 'muscle': 'Deltoid, Trisep', 'tips': 'Bar at clavicle. Press slightly back overhead. Full lockout at top. Keep core tight.\n\n📌 Opsi: Smith Machine Shoulder Press', 'foto': 'overhead_press.jpg'},
        {'nama': 'Dumbbell Shoulder Press', 'detail': '3 sets × 8-12 reps', 'muscle': 'All Delt Heads, Trisep', 'tips': 'Dumbbells at ear level. Press up and slightly inward. Full lockout at top.\n\n📌 Opsi: Machine Shoulder Press', 'foto': 'dumbbell_shoulder_press.jpg'},
        {'nama': 'Lateral Raise', 'detail': '4 sets × 12-15 reps', 'muscle': 'Deltoid Lateral (Side Delts)', 'tips': 'Lead with elbows, pause 1 sec at shoulder height. Lower slowly. No swinging.\n\n📌 Opsi: Cable Lateral Raise', 'foto': 'lateral_raise.jpg'},
        {'nama': 'Rear Delt Fly', 'detail': '3 sets × 12-15 reps', 'muscle': 'Rear Delt', 'tips': 'Bend forward at hips. Raise arms out to sides, squeeze shoulder blades. Pause 1 sec at top.\n\n📌 Opsi: Reverse Pec Deck', 'foto': 'reverse_pec_deck.jpg'},
        {'nama': 'Shrug', 'detail': '3 sets × 12-15 reps', 'muscle': 'Trapezius', 'tips': 'Hold bar/dumbbells, shrug shoulders straight up toward ears. Hold 1 sec at top.\n\n📌 Opsi: Dumbbell Shrug', 'foto': 'shrug.jpg'},
    ],
    'Kaki + Core': [
        {'nama': 'Squat', 'detail': '4 sets × 6-10 reps', 'muscle': 'Quad, Glute, Hamstring, Core', 'tips': 'Feet shoulder-width, toes slightly out. Hit parallel or below. Drive knees out.\n\n📌 Opsi: Hack Squat', 'foto': 'squat.jpg'},
        {'nama': 'Leg Press', 'detail': '4 sets × 10-12 reps', 'muscle': 'Quad, Glute', 'tips': 'Full range — do not lock knees. High wide foot = glutes. Low narrow foot = quads.\n\n📌 Opsi: Bulgarian Split Squat', 'foto': 'leg_press.jpg'},
        {'nama': 'Romanian Deadlift', 'detail': '3 sets × 8-12 reps', 'muscle': 'Hamstring, Glute', 'tips': 'Push hips back — not down. Feel maximum stretch at bottom. Squeeze glutes hard at top.\n\n📌 Opsi: Stiff Leg Deadlift', 'foto': 'romanian_deadlift.jpg'},
        {'nama': 'Walking Lunge', 'detail': '3 sets × 12 reps/kaki', 'muscle': 'Quad, Glute, Stabilizer', 'tips': 'Step forward, drop back knee toward floor. Keep front shin vertical. Drive through front heel.\n\n📌 Opsi: Reverse Lunge', 'foto': 'walking_lunge.jpg'},
        {'nama': 'Leg Curl', 'detail': '3 sets × 12 reps', 'muscle': 'Hamstring (isolasi)', 'tips': 'Curl to full contraction. Squeeze 1 sec at top. Lower slowly. Do not let hips rise off pad.\n\n📌 Opsi: Nordic Curl', 'foto': 'leg_curl.jpg'},
        {'nama': 'Standing Calf Raise', 'detail': '4 sets × 15-20 reps', 'muscle': 'Gastrocnemius', 'tips': 'Rise on big toe. Hold 2 sec at top. Lower slowly — full stretch at bottom.\n\n📌 Opsi: Seated Calf Raise', 'foto': 'calf_raise.jpg'},
        {'nama': 'Russian Twist', 'detail': '3 sets × 20 reps', 'muscle': 'Oblique', 'tips': 'Lean back 45°, feet off floor. Rotate plate side to side. Touch plate to floor each rep.\n\n📌 Opsi: Cable Woodchopper', 'foto': 'russian_twist.jpg'},
        {'nama': 'Bicycle Crunch', 'detail': '3 sets × 20 reps', 'muscle': 'Rectus Abdominis, Oblique', 'tips': 'Hands behind head, alternate bringing elbow to opposite knee. Keep core engaged throughout.\n\n📌 Opsi: Mountain Climber', 'foto': 'bicycle_crunch.jpg'},
        {'nama': 'Plank', 'detail': '3 sets × 60 seconds', 'muscle': 'Core (Transverse Abdominis)', 'tips': 'Forearms on floor, body in straight line. Squeeze glutes and abs hard. Breathe steadily.\n\n📌 Opsi: Side Plank', 'foto': 'side_plank.jpg'},
    ],
    'Lengan': [
        {'nama': 'Barbell Curl', 'detail': '4 sets × 8-12 reps', 'muscle': 'Biceps', 'tips': 'Keep elbows at sides. Full range from dead hang to full contraction. Slow lowering.\n\n📌 Opsi: EZ Bar Curl', 'foto': 'dumbbell_curl.jpg'},
        {'nama': 'Hammer Curl', 'detail': '3 sets × 10-12 reps', 'muscle': 'Brachialis, Biceps', 'tips': 'Palms facing each other throughout. Full range of motion. Slow lowering.\n\n📌 Opsi: Rope Hammer Curl', 'foto': 'hammer_curl.jpg'},
        {'nama': 'Preacher Curl', 'detail': '3 sets × 10-12 reps', 'muscle': 'Biceps (isolasi)', 'tips': 'Arms on preacher pad isolates biceps fully. Full stretch at bottom, full contraction at top.\n\n📌 Opsi: Concentration Curl', 'foto': 'preacher_curl.jpg'},
        {'nama': 'Tricep Pushdown', 'detail': '4 sets × 10-12 reps', 'muscle': 'Triceps', 'tips': 'Elbows locked at sides. Full extension at bottom. Squeeze triceps hard at lockout.\n\n📌 Opsi: Close Grip Bench Press', 'foto': 'tricep_pushdown.jpg'},
        {'nama': 'Overhead Tricep Extension', 'detail': '3 sets × 10-12 reps', 'muscle': 'Triceps Long Head', 'tips': 'Elbows close to head. Lower behind head until full stretch. Extend fully at top.\n\n📌 Opsi: Rope Overhead Extension', 'foto': 'skull_crusher.jpg'},
        {'nama': 'Dips', 'detail': '3 sets × semampunya', 'muscle': 'Triceps, Dada Bawah', 'tips': 'Lean forward slightly for more chest, stay upright for more triceps. Drive up explosively.\n\n📌 Opsi: Assisted Dip Machine', 'foto': 'dips.jpg'},
    ],
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
        is_sunday = now.weekday() == 6
        if is_sunday:
            msg = f"""🌅 *Good Morning, Ali!*

📅 {hari_str}
😴 *Minggu — Istirahat Total*

Fokus pemulihan otot hari ini!
✅ Peregangan ringan
✅ Tidur cukup 7-9 jam
✅ Eat 1.8-2.2g protein per kg bodyweight
✅ Stay hydrated — minimum 2 liters

Come back stronger besok! 💪"""
        else:
            msg = f"""🌅 *Good Morning, Ali!*

📅 {hari_str}
😴 *Rabu — Istirahat*

Light activity hari ini!
🚶 Jalan santai 20-30 menit (opsional)
🧘 Stretching ringan
✅ Eat enough protein
✅ Sleep 7-9 hours tonight

Come back stronger tomorrow! 💪"""
        kirim_pesan(msg)

    else:
        latihannya = LATIHAN[nama]
        daftar = '\n'.join([f'⬜ *{l["nama"]}* — {l["detail"]}' for l in latihannya])

        notes = {
            'Dada + Core': '🫁 *CHEST + CORE DAY*\n💡 Compound dulu (bench, incline) baru isolation (fly, push-up)',
            'Punggung': '🔙 *BACK DAY*\n💡 Vertical pull dulu (lat pulldown) baru horizontal (row)',
            'Bahu': '🤷 *SHOULDER DAY*\n💡 Compound dulu (OHP) baru isolation (lateral, rear delt)',
            'Kaki + Core': '🦵 *LEG + CORE DAY*\n💡 Squat di awal saat tenaga penuh',
            'Lengan': '💪 *ARM DAY*\n💡 Biceps dulu baru triceps'
        }

        msg = f"""🌅 *Good Morning, Ali!*

📅 {hari_str}
{emoji} *Today: {nama}*

*Workout:*
{daftar}

{notes.get(nama, '')}
⏰ Warmup: 5-10 min cardio + dynamic stretch!"""

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
