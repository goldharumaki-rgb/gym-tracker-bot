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
    0: ('Chest', '🔴'),
    1: ('Back', '🔵'),
    2: ('Shoulders', '🟠'),
    3: ('Legs', '🟢'),
    4: ('Biceps + Triceps', '💪'),
    5: ('Abs + Cardio', '🔥'),
    6: ('Rest Day', '😴')
}

LATIHAN = {
    'Chest': [
        {'nama': 'Barbell Bench Press', 'detail': '4 sets × 6-10 reps', 'muscle': 'Dada, Trisep, Bahu Depan', 'tips': 'Retract scapula, slight arch. Lower bar to lower chest over 3 sec. Drive explosively up. Log weight every session.', 'foto': 'bench_press.jpg'},
        {'nama': 'Incline Dumbbell Press', 'detail': '4 sets × 8-12 reps', 'muscle': 'Dada Atas, Bahu Depan', 'tips': 'Bench at 30°. Lower until elbows at shoulder height. Squeeze chest at top. Tempo 2-1-2.', 'foto': 'incline_press.jpg'},
        {'nama': 'Decline Bench Press', 'detail': '3 sets × 8-12 reps', 'muscle': 'Dada Bawah', 'tips': 'Bench angled downward. Targets lower chest fibers. Lower bar to lower chest. Drive up explosively.', 'foto': 'decline_bench_press.jpg'},
        {'nama': 'Chest Fly (Machine/Dumbbell)', 'detail': '3 sets × 12-15 reps', 'muscle': 'Dada (isolasi)', 'tips': 'Slight elbow bend, arc the weights together. Squeeze pecs hard at top. Feel the stretch at bottom.', 'foto': 'cable_fly.jpg'},
        {'nama': 'Cable Crossover', 'detail': '3 sets × 12-15 reps', 'muscle': 'Dada (isolasi, inner chest)', 'tips': 'Pulleys at chest height. Cross hands in front of body. Squeeze pecs hard at full contraction. Slow controlled return.', 'foto': 'cable_fly.jpg'},
        {'nama': 'Push-ups', 'detail': '3 sets × semampunya', 'muscle': 'Dada, Trisep, Core', 'tips': 'Hands slightly wider than shoulders. Lower chest to floor. Keep body in straight line. Push up explosively.', 'foto': 'push_up.jpg'},
    ],
    'Back': [
        {'nama': 'Lat Pulldown', 'detail': '4 sets × 8-12 reps', 'muscle': 'Lats, Bisep', 'tips': 'Wide overhand grip. Pull bar to upper chest. Lean back slightly. Squeeze lats hard at bottom. Slow 3 sec return.', 'foto': 'pull_up.jpg'},
        {'nama': 'Pull-ups', 'detail': '4 sets × 6-10 reps', 'muscle': 'Lats, Bisep', 'tips': 'Full range — dead hang to chin over bar. Pull elbows down and back. Squeeze lats hard at bottom. Control lowering 3 sec.', 'foto': 'pull_up.jpg'},
        {'nama': 'Barbell Deadlift', 'detail': '4 sets × 5-8 reps', 'muscle': 'Posterior Chain, Glute, Trap, Core', 'tips': 'Bar over mid-foot. Hinge at hips, brace core maximally. Drive floor away. Keep bar close to body. Log weight.', 'foto': 'romanian_deadlift.jpg'},
        {'nama': 'Seated Cable Row', 'detail': '3 sets × 10-12 reps', 'muscle': 'Mid-Back, Rear Delt', 'tips': 'Sit tall, chest up. Pull handle to lower chest. Squeeze shoulder blades together. Slow 3 sec return.', 'foto': 'seated_cable_row.jpg'},
        {'nama': 'T-Bar Row', 'detail': '4 sets × 8-12 reps', 'muscle': 'Mid-Back, Rhomboid, Bisep', 'tips': 'Chest on pad. Pull elbows back and up. Squeeze shoulder blades hard at top. Slow 3 sec return.', 'foto': 'bent_over_row.jpg'},
        {'nama': 'One-Arm Dumbbell Row', 'detail': '3 sets × 10 reps/sisi', 'muscle': 'Mid-Back, Lats, Bisep', 'tips': 'One arm at a time. Pull elbow back and up. Squeeze shoulder blade at top. Full stretch at bottom. No rotation.', 'foto': 'bent_over_row.jpg'},
    ],
    'Shoulders': [
        {'nama': 'Overhead Press (Barbell/Dumbbell)', 'detail': '4 sets × 6-10 reps', 'muscle': 'Deltoid, Trisep', 'tips': 'Bar at clavicle. Press slightly back overhead. Full lockout at top. Lower over 3 sec. Keep core tight.', 'foto': 'overhead_press.jpg'},
        {'nama': 'Lateral Raises', 'detail': '4 sets × 12-15 reps', 'muscle': 'Deltoid Lateral (Side Delts)', 'tips': 'Lead with elbows, pause 1 sec at shoulder height. Lower slowly 3 sec. No swinging.', 'foto': 'lateral_raise.jpg'},
        {'nama': 'Front Raises', 'detail': '3 sets × 12-15 reps', 'muscle': 'Deltoid Anterior (Front Delts)', 'tips': 'Raise dumbbell straight in front to shoulder height. Slight bend in elbow. Lower slowly 3 sec. Alternate or together.', 'foto': 'overhead_press.jpg'},
        {'nama': 'Rear Delt Fly', 'detail': '3 sets × 12-15 reps', 'muscle': 'Rear Delt', 'tips': 'Bend forward at hips. Raise arms out to sides, squeeze shoulder blades. Pause 1 sec at top. Lower slowly.', 'foto': 'reverse_pec_deck.jpg'},
        {'nama': 'Shrugs', 'detail': '3 sets × 12-15 reps', 'muscle': 'Trapezius', 'tips': 'Hold bar/dumbbells, shrug shoulders straight up toward ears. Hold 1 sec at top. Lower slowly — no rolling shoulders.', 'foto': 'shrug.jpg'},
    ],
    'Legs': [
        {'nama': 'Barbell Squats', 'detail': '4 sets × 6-10 reps', 'muscle': 'Quad, Glute, Hamstring, Core', 'tips': 'Feet shoulder-width, toes slightly out. Hit parallel or below. Drive knees out. Log weight every session.', 'foto': 'squat.jpg'},
        {'nama': 'Leg Press', 'detail': '4 sets × 10-12 reps', 'muscle': 'Quad, Glute', 'tips': 'Full range — do not lock knees. High wide foot = glutes. Low narrow foot = quads.', 'foto': 'leg_press.jpg'},
        {'nama': 'Lunges', 'detail': '3 sets × 12 reps/kaki', 'muscle': 'Quad, Glute, Stabilizer', 'tips': 'Step forward, drop back knee toward floor. Keep front shin vertical. Drive through front heel to stand.', 'foto': 'walking_lunge.jpg'},
        {'nama': 'Leg Extension', 'detail': '3 sets × 12-15 reps', 'muscle': 'Quad (isolasi)', 'tips': 'Extend fully. Squeeze quads hard 1 sec at top. Lower slowly 3 sec. Keep back against pad throughout.', 'foto': 'leg_press.jpg'},
        {'nama': 'Leg Curl', 'detail': '3 sets × 12 reps', 'muscle': 'Hamstring (isolasi)', 'tips': 'Curl to full contraction. Squeeze 1 sec at top. Lower slowly 3 sec. Do not let hips rise off pad.', 'foto': 'leg_curl.jpg'},
        {'nama': 'Calf Raises', 'detail': '4 sets × 15-20 reps', 'muscle': 'Gastrocnemius, Soleus', 'tips': 'Rise on big toe. Hold 2 sec at top. Lower slowly 3 sec — full stretch at bottom. Do not bounce.', 'foto': 'calf_raise.jpg'},
    ],
    'Biceps + Triceps': [
        {'nama': 'Barbell Curl', 'detail': '4 sets × 8-12 reps', 'muscle': 'Biceps', 'tips': 'Keep elbows at sides. Full range from dead hang to full contraction. Slow 3 sec lowering.', 'foto': 'dumbbell_curl.jpg'},
        {'nama': 'Dumbbell Curl', 'detail': '3 sets × 10-12 reps', 'muscle': 'Biceps', 'tips': 'Full range of motion. Supinate at top. Slow 3 sec lowering. Keep elbows at sides.', 'foto': 'dumbbell_curl.jpg'},
        {'nama': 'Hammer Curl', 'detail': '3 sets × 10-12 reps', 'muscle': 'Brachialis, Biceps', 'tips': 'Palms facing each other throughout. Full range of motion. Slow 3 sec lowering.', 'foto': 'hammer_curl.jpg'},
        {'nama': 'Preacher Curl', 'detail': '3 sets × 10-12 reps', 'muscle': 'Biceps (isolasi)', 'tips': 'Arms on preacher pad isolates biceps fully. Full stretch at bottom, full contraction at top. Slow controlled tempo.', 'foto': 'preacher_curl.jpg'},
        {'nama': 'Cable Curl', 'detail': '3 sets × 10-12 reps', 'muscle': 'Biceps', 'tips': 'Cable provides constant tension throughout range. Keep elbows at sides. Squeeze hard at top. Slow lowering.', 'foto': 'cable_curl.jpg'},
        {'nama': 'Triceps Pushdown', 'detail': '4 sets × 10-12 reps', 'muscle': 'Triceps', 'tips': 'Elbows locked at sides. Full extension at bottom. Squeeze triceps hard at lockout. Slow 3 sec return.', 'foto': 'tricep_pushdown.jpg'},
        {'nama': 'Skull Crushers', 'detail': '3 sets × 10-12 reps', 'muscle': 'Triceps Long Head', 'tips': 'Lower bar to forehead, elbows pointing up. Extend fully at top. Keep elbows close together.', 'foto': 'skull_crusher.jpg'},
        {'nama': 'Dips', 'detail': '3 sets × semampunya', 'muscle': 'Triceps, Dada Bawah', 'tips': 'Lean forward slightly for more chest, stay upright for more triceps. Lower until shoulders below elbows. Drive up explosively.', 'foto': 'dips.jpg'},
        {'nama': 'Overhead Triceps Extension', 'detail': '3 sets × 10-12 reps', 'muscle': 'Triceps Long Head', 'tips': 'Elbows close to head. Lower behind head until full stretch. Extend fully at top. Feel the long head stretch.', 'foto': 'skull_crusher.jpg'},
        {'nama': 'Close Grip Bench Press', 'detail': '3 sets × 8-12 reps', 'muscle': 'Triceps, Dada Dalam', 'tips': 'Hands shoulder-width apart on bar. Elbows stay close to body. Lower to lower chest. Press up focusing on triceps.', 'foto': 'close_grip_bench_press.jpg'},
    ],
    'Abs + Cardio': [
        {'nama': 'Crunches', 'detail': '3 sets × 20 reps', 'muscle': 'Rectus Abdominis', 'tips': 'Hands behind head, knees bent. Curl shoulders off floor. Squeeze abs hard at top. Slow controlled return.', 'foto': 'crunch.jpg'},
        {'nama': 'Leg Raises', 'detail': '3 sets × 15 reps', 'muscle': 'Lower Abs', 'tips': 'Lying flat, raise straight legs to 90°. Keep lower back pressed to floor. Lower with control — do not let feet drop.', 'foto': 'hanging_leg_raise.jpg'},
        {'nama': 'Hanging Leg Raises', 'detail': '3 sets × 12-15 reps', 'muscle': 'Lower Abs, Hip Flexors', 'tips': 'Hang from bar, posterior pelvic tilt. Raise legs to 90° or higher. Avoid swinging. Lower with full control.', 'foto': 'hanging_leg_raise.jpg'},
        {'nama': 'Plank', 'detail': '3 sets × 60 seconds', 'muscle': 'Core (Transverse Abdominis)', 'tips': 'Forearms on floor, body in straight line. Squeeze glutes and abs hard. Breathe steadily throughout.', 'foto': 'plank.jpg'},
        {'nama': 'Russian Twist', 'detail': '3 sets × 20 reps', 'muscle': 'Oblique', 'tips': 'Lean back 45°, feet off floor. Rotate plate side to side. Touch plate to floor each rep. Control the rotation.', 'foto': 'russian_twist.jpg'},
        {'nama': 'Cardio (Treadmill/Bike)', 'detail': '20-30 minutes', 'muscle': 'Cardiovascular System', 'tips': 'Moderate intensity — should be able to talk but slightly breathless. Burns fat, improves endurance. Great way to finish the week strong.', 'foto': 'mountain_climber.jpg'},
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
        msg = f"""🌅 *Good Morning, Ali!*

📅 {hari_str}
🧘 *Sunday — Rest Day*

Complete recovery today!
✅ Sleep 7-9 hours
✅ Eat 1.8-2.2g protein per kg bodyweight
✅ Stay hydrated — minimum 2 liters
✅ Light stretching is fine

*Discipline today • Strength tomorrow • Success forever* 💪"""
        kirim_pesan(msg)

    else:
        latihannya = LATIHAN[nama]
        daftar = '\n'.join([f'⬜ *{l["nama"]}* — {l["detail"]}' for l in latihannya])

        notes = {
            'Chest': '🔴 *CHEST DAY*\n💡 Compound dulu (bench, incline, decline) baru isolation (fly, crossover, push-up)',
            'Back': '🔵 *BACK DAY*\n💡 Vertical pull dulu (pulldown, pull-up), lalu deadlift, baru horizontal row',
            'Shoulders': '🟠 *SHOULDER DAY*\n💡 Compound dulu (OHP) baru isolation (lateral, front, rear delt, shrug)',
            'Legs': '🟢 *LEG DAY*\n💡 Squat di awal saat tenaga penuh, lalu leg press, lunges, isolasi, calf di akhir',
            'Biceps + Triceps': '💪 *ARM DAY*\n💡 Biceps dulu (curl variations) baru triceps (pushdown, skull crusher, dips)',
            'Abs + Cardio': '🔥 *ABS + CARDIO*\n💡 Core exercises dulu, cardio di akhir sesi untuk finishing'
        }

        msg = f"""🌅 *Good Morning, Ali!*

📅 {hari_str}
{emoji} *Today: {nama}*

*Single Body Part Workout:*
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
