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
        {
            'nama': 'Bench Press',
            'detail': '4 sets × 6-10 reps',
            'muscle': 'Dada, Trisep, Bahu Depan',
            'tips': '🔹 CHEST #1\nRetract scapula, slight arch. Lower bar to lower chest over 3 sec. Drive explosively up. Log weight every session.',
            'foto': 'bench_press.jpg',
            'opsi': [('Dumbbell Bench Press', 'bench_press.jpg')]
        },
        {
            'nama': 'Incline Dumbbell Press',
            'detail': '4 sets × 8-12 reps',
            'muscle': 'Dada Atas, Bahu Depan',
            'tips': '🔹 CHEST #2\nBench at 30°. Lower until elbows at shoulder height. Squeeze chest at top. Tempo 2-1-2.',
            'foto': 'incline_press.jpg',
            'opsi': [('Incline Machine Press', 'chest_press_machine.jpg')]
        },
        {
            'nama': 'Chest Fly',
            'detail': '3 sets × 10-15 reps',
            'muscle': 'Dada (isolasi)',
            'tips': '🔹 ISOLATION\nSlight elbow bend, arc the weights together. Squeeze pecs hard at top. Feel the stretch at bottom. Slow controlled movement.',
            'foto': 'cable_fly.jpg',
            'opsi': [('Pec Deck Machine', 'cable_fly.jpg')]
        },
        {
            'nama': 'Push-up',
            'detail': '3 sets × semampunya',
            'muscle': 'Dada, Trisep, Core',
            'tips': '🔹 BODYWEIGHT\nHands slightly wider than shoulders. Lower chest to floor. Keep body in straight line throughout. Push up explosively.',
            'foto': 'push_up.jpg',
            'opsi': [('Chest Press Machine', 'chest_press_machine.jpg')]
        },
        {
            'nama': 'Plank',
            'detail': '3 sets × 60 seconds',
            'muscle': 'Core (Transverse Abdominis)',
            'tips': '🔹 STABILITY\nForearms on floor, body in straight line. Squeeze glutes and abs hard. Do not let hips sag or pike. Breathe steadily.',
            'foto': 'plank.jpg',
            'opsi': [('Dead Bug', 'plank.jpg')]
        },
        {
            'nama': 'Hanging Leg Raise',
            'detail': '3 sets × 12-15 reps',
            'muscle': 'Lower Abs, Hip Flexors',
            'tips': '🔹 CORE\nHang from bar, posterior pelvic tilt. Raise legs to 90° or higher. Avoid swinging. Lower with full control.',
            'foto': 'hanging_leg_raise.jpg',
            'opsi': [('Lying Leg Raise', 'hanging_leg_raise.jpg')]
        },
        {
            'nama': 'Crunch',
            'detail': '3 sets × 20 reps',
            'muscle': 'Rectus Abdominis',
            'tips': '🔹 CORE\nHands behind head, knees bent. Curl shoulders off floor. Squeeze abs hard at top. Slow controlled return.',
            'foto': 'crunch.jpg',
            'opsi': [('Cable Crunch', 'cable_crunch.jpg')]
        },
    ],
    'Punggung': [
        {
            'nama': 'Lat Pulldown',
            'detail': '4 sets × 8-12 reps',
            'muscle': 'Lats, Bisep',
            'tips': '🔹 BACK #1\nWide overhand grip. Pull bar to upper chest. Lean back slightly. Squeeze lats hard at bottom. Slow 3 sec return.',
            'foto': 'pull_up.jpg',
            'opsi': [('Assisted Pull-up', 'assisted_pull_up.jpg')]
        },
        {
            'nama': 'Barbell Row',
            'detail': '4 sets × 8-12 reps',
            'muscle': 'Mid-Back, Lats, Bisep',
            'tips': '🔹 BACK #2\nHinge 45°, brace core hard. Pull bar to belly button. Squeeze lats 1 sec at top. Lower slowly 3 sec.',
            'foto': 'bent_over_row.jpg',
            'opsi': [('T-Bar Row', 'bent_over_row.jpg')]
        },
        {
            'nama': 'Seated Cable Row',
            'detail': '3 sets × 10-12 reps',
            'muscle': 'Mid-Back, Rear Delt',
            'tips': '🔹 BACK #3\nSit tall, chest up. Pull handle to lower chest. Squeeze shoulder blades together. Slow 3 sec return.',
            'foto': 'seated_cable_row.jpg',
            'opsi': [('Chest Supported Row', 'seated_cable_row.jpg')]
        },
        {
            'nama': 'Dumbbell Row',
            'detail': '3 sets × 10 reps/sisi',
            'muscle': 'Mid-Back, Lats, Bisep',
            'tips': '🔹 UNILATERAL\nOne arm at a time. Pull elbow back and up. Squeeze shoulder blade at top. Full stretch at bottom. No rotation.',
            'foto': 'bent_over_row.jpg',
            'opsi': [('Machine Row', 'seated_cable_row.jpg')]
        },
        {
            'nama': 'Face Pull',
            'detail': '3 sets × 12-15 reps',
            'muscle': 'Rear Delt, Rotator Cuff, Trap',
            'tips': '🔹 SHOULDER HEALTH\nPull toward face, elbows at shoulder height. Rotate hands outward at end. Essential for posture and shoulder health.',
            'foto': 'face_pull.jpg',
            'opsi': [('Reverse Pec Deck', 'reverse_pec_deck.jpg')]
        },
    ],
    'Bahu': [
        {
            'nama': 'Overhead Press',
            'detail': '4 sets × 6-10 reps',
            'muscle': 'Deltoid, Trisep',
            'tips': '🔹 SHOULDER #1 — STRENGTH\nBar at clavicle. Press slightly back overhead. Full lockout at top. Lower over 3 sec. Keep core tight.',
            'foto': 'overhead_press.jpg',
            'opsi': [('Smith Machine Shoulder Press', 'smith_incline_press.jpg')]
        },
        {
            'nama': 'Dumbbell Shoulder Press',
            'detail': '3 sets × 8-12 reps',
            'muscle': 'All Delt Heads, Trisep',
            'tips': '🔹 SHOULDER #2\nDumbbells at ear level. Press up and slightly inward. Full lockout at top. Lower 3 sec.',
            'foto': 'dumbbell_shoulder_press.jpg',
            'opsi': [('Machine Shoulder Press', 'chest_press_machine.jpg')]
        },
        {
            'nama': 'Lateral Raise',
            'detail': '4 sets × 12-15 reps',
            'muscle': 'Deltoid Lateral (Side Delts)',
            'tips': '🔹 ISOLATION\nLead with elbows, pause 1 sec at shoulder height. Lower slowly 3 sec. No swinging.',
            'foto': 'lateral_raise.jpg',
            'opsi': [('Cable Lateral Raise', 'lateral_raise.jpg')]
        },
        {
            'nama': 'Rear Delt Fly',
            'detail': '3 sets × 12-15 reps',
            'muscle': 'Rear Delt',
            'tips': '🔹 ISOLATION\nBend forward at hips. Raise arms out to sides, squeeze shoulder blades. Pause 1 sec at top. Lower slowly.',
            'foto': 'face_pull.jpg',
            'opsi': [('Reverse Pec Deck', 'reverse_pec_deck.jpg')]
        },
        {
            'nama': 'Shrug',
            'detail': '3 sets × 12-15 reps',
            'muscle': 'Trapezius',
            'tips': '🔹 TRAP ISOLATION\nHold bar/dumbbells, shrug shoulders straight up toward ears. Hold 1 sec at top. Lower slowly — no rolling shoulders.',
            'foto': 'shrug.jpg',
            'opsi': [('Dumbbell Shrug', 'shrug.jpg')]
        },
    ],
    'Kaki + Core': [
        {
            'nama': 'Squat',
            'detail': '4 sets × 6-10 reps',
            'muscle': 'Quad, Glute, Hamstring, Core',
            'tips': '🔹 LEG #1 — STRENGTH\nFeet shoulder-width, toes slightly out. Hit parallel or below. Drive knees out. Log weight every session.',
            'foto': 'squat.jpg',
            'opsi': [('Hack Squat', 'hack_squat.jpg')]
        },
        {
            'nama': 'Leg Press',
            'detail': '4 sets × 10-12 reps',
            'muscle': 'Quad, Glute',
            'tips': '🔹 LEG #2\nFull range — do not lock knees. High wide foot = glutes. Low narrow foot = quads.',
            'foto': 'leg_press.jpg',
            'opsi': [('Bulgarian Split Squat', 'bulgarian_split_squat.jpg')]
        },
        {
            'nama': 'Romanian Deadlift',
            'detail': '3 sets × 8-12 reps',
            'muscle': 'Hamstring, Glute',
            'tips': '🔹 POSTERIOR CHAIN\nPush hips back — not down. Bar stays close to legs. Feel maximum stretch at bottom. Squeeze glutes hard at top.',
            'foto': 'romanian_deadlift.jpg',
            'opsi': [('Stiff Leg Deadlift', 'romanian_deadlift.jpg')]
        },
        {
            'nama': 'Walking Lunge',
            'detail': '3 sets × 12 reps/kaki',
            'muscle': 'Quad, Glute, Stabilizer',
            'tips': '🔹 UNILATERAL\nStep forward, drop back knee toward floor. Keep front shin vertical. Drive through front heel to stand.',
            'foto': 'walking_lunge.jpg',
            'opsi': [('Reverse Lunge', 'reverse_lunge.jpg')]
        },
        {
            'nama': 'Leg Curl',
            'detail': '3 sets × 12 reps',
            'muscle': 'Hamstring (isolasi)',
            'tips': '🔹 ISOLATION\nCurl to full contraction. Squeeze 1 sec at top. Lower slowly 3 sec. Do not let hips rise off pad.',
            'foto': 'leg_curl.jpg',
            'opsi': [('Nordic Curl', 'nordic_curl.jpg')]
        },
        {
            'nama': 'Standing Calf Raise',
            'detail': '4 sets × 15-20 reps',
            'muscle': 'Gastrocnemius',
            'tips': '🔹 CALVES\nRise on big toe. Hold 2 sec at top. Lower slowly 3 sec — full stretch at bottom. Do not bounce.',
            'foto': 'calf_raise.jpg',
            'opsi': [('Seated Calf Raise', 'calf_raise.jpg')]
        },
        {
            'nama': 'Russian Twist',
            'detail': '3 sets × 20 reps',
            'muscle': 'Oblique',
            'tips': '🔹 CORE\nLean back 45°, feet off floor. Rotate plate side to side. Touch plate to floor each rep. Control the rotation.',
            'foto': 'russian_twist.jpg',
            'opsi': [('Cable Woodchopper', 'russian_twist.jpg')]
        },
        {
            'nama': 'Bicycle Crunch',
            'detail': '3 sets × 20 reps',
            'muscle': 'Rectus Abdominis, Oblique',
            'tips': '🔹 CORE\nHands behind head, alternate bringing elbow to opposite knee. Keep core engaged throughout. Controlled pace — no rushing.',
            'foto': 'bicycle_crunch.jpg',
            'opsi': [('Mountain Climber', 'mountain_climber.jpg')]
        },
        {
            'nama': 'Plank',
            'detail': '3 sets × 60 seconds',
            'muscle': 'Core (Transverse Abdominis)',
            'tips': '🔹 STABILITY\nForearms on floor, body in straight line. Squeeze glutes and abs hard. Breathe steadily throughout.',
            'foto': 'plank.jpg',
            'opsi': [('Side Plank', 'side_plank.jpg')]
        },
    ],
    'Lengan': [
        {
            'nama': 'Barbell Curl',
            'detail': '4 sets × 8-12 reps',
            'muscle': 'Biceps',
            'tips': '🔹 BICEPS #1\nKeep elbows at sides. Full range from dead hang to full contraction. Slow 3 sec lowering.',
            'foto': 'dumbbell_curl.jpg',
            'opsi': [('EZ Bar Curl', 'dumbbell_curl.jpg')]
        },
        {
            'nama': 'Hammer Curl',
            'detail': '3 sets × 10-12 reps',
            'muscle': 'Brachialis, Biceps',
            'tips': '🔹 BICEPS #2\nPalms facing each other throughout. Full range of motion. Slow 3 sec lowering.',
            'foto': 'hammer_curl.jpg',
            'opsi': [('Rope Hammer Curl', 'rope_hammer_curl.jpg')]
        },
        {
            'nama': 'Preacher Curl',
            'detail': '3 sets × 10-12 reps',
            'muscle': 'Biceps (isolasi)',
            'tips': '🔹 BICEPS #3\nArms on preacher pad isolates biceps fully. Full stretch at bottom, full contraction at top. Slow controlled tempo.',
            'foto': 'preacher_curl.jpg',
            'opsi': [('Concentration Curl', 'preacher_curl.jpg')]
        },
        {
            'nama': 'Tricep Pushdown',
            'detail': '4 sets × 10-12 reps',
            'muscle': 'Triceps',
            'tips': '🔹 TRICEPS #1\nElbows locked at sides. Full extension at bottom. Squeeze triceps hard at lockout. Slow 3 sec return.',
            'foto': 'tricep_pushdown.jpg',
            'opsi': [('Close Grip Bench Press', 'close_grip_bench_press.jpg')]
        },
        {
            'nama': 'Overhead Tricep Extension',
            'detail': '3 sets × 10-12 reps',
            'muscle': 'Triceps Long Head',
            'tips': '🔹 TRICEPS #2\nElbows close to head. Lower behind head until full stretch. Extend fully at top. Feel the long head stretch.',
            'foto': 'tricep_pushdown.jpg',
            'opsi': [('Rope Overhead Extension', 'tricep_pushdown.jpg')]
        },
        {
            'nama': 'Dips',
            'detail': '3 sets × semampunya',
            'muscle': 'Triceps, Dada Bawah',
            'tips': '🔹 COMPOUND FINISHER\nLean forward slightly for more chest, stay upright for more triceps. Lower until shoulders below elbows. Drive up explosively.',
            'foto': 'dips.jpg',
            'opsi': [('Assisted Dip Machine', 'machine_dip.jpg')]
        },
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

def kirim_opsi(opsi_list, script_dir):
    for nama_opsi, foto_opsi in opsi_list:
        foto_path = os.path.join(script_dir, foto_opsi)
        caption = f'📌 *Opsi: {nama_opsi}*'
        kirim_foto_lokal(foto_path, caption)
        time.sleep(1.5)

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
            'Dada + Core': '🫁 *CHEST + CORE DAY*\n💡 Compound dulu (bench, incline) baru isolation (fly, push-up)\n💡 Core di akhir sesi',
            'Punggung': '🔙 *BACK DAY*\n💡 Vertical pull dulu (lat pulldown) baru horizontal (row)\n💡 Face pull untuk shoulder health',
            'Bahu': '🤷 *SHOULDER DAY*\n💡 Compound dulu (OHP) baru isolation (lateral, rear delt)\n💡 Jangan lupa shrug untuk trapezius',
            'Kaki + Core': '🦵 *LEG + CORE DAY*\n💡 Squat di awal saat tenaga penuh\n💡 Core finisher di akhir sesi',
            'Lengan': '💪 *ARM DAY*\n💡 Biceps dulu baru triceps\n💡 Dips sebagai compound finisher'
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
            time.sleep(1.5)

            if ex.get('opsi'):
                kirim_opsi(ex['opsi'], script_dir)

    print(f"✅ Morning reminder sent — {nama}")

if __name__ == '__main__':
    reminder_pagi()
    print('Done!')
