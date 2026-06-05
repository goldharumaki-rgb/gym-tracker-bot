import urllib.request
import json
import datetime
import os
import time
import uuid

TOKEN = os.environ.get('TELEGRAM_TOKEN', '')
CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID', '')

JADWAL = {
    0: ('Upper A', '💪🔵'),
    1: ('Lower A', '🦵🔵'),
    2: ('Rest Day', '😴'),
    3: ('Upper B', '💪🟣'),
    4: ('Lower B', '🦵🟣'),
    5: ('Rest Day', '😴'),
    6: ('Rest Day', '😴')
}

LATIHAN = {
    'Upper A': [
        {'nama': 'Barbell Bench Press', 'detail': '5 sets × 5 reps | Rest 3 min', 'muscle': 'Dada, Trisep, Bahu Depan', 'tips': '🔹 STRENGTH #1\nRetract scapula, slight arch. Lower bar to lower chest over 3 sec. Drive explosively up. Priority lift — log weight every session.', 'foto': 'bench_press.jpg'},
        {'nama': 'Bent-over Barbell Row', 'detail': '5 sets × 5 reps | Rest 3 min', 'muscle': 'Lats, Rhomboid, Bisep', 'tips': '🔹 STRENGTH #2\nHinge 45°, brace core hard. Pull bar to belly button. Squeeze lats 1 sec at top. Lower slowly 3 sec. Log weight every session.', 'foto': 'bent_over_row.jpg'},
        {'nama': 'Overhead Press (OHP)', 'detail': '4 sets × 6 reps | Rest 2-3 min', 'muscle': 'Deltoid, Trisep', 'tips': '🔹 STRENGTH #3\nBar at clavicle. Press slightly back overhead. Full lockout at top. Lower over 3 sec. Keep core tight.', 'foto': 'overhead_press.jpg'},
        {'nama': 'Weighted Pull-up', 'detail': '4 sets × 6 reps | Rest 2-3 min', 'muscle': 'Lats, Bisep', 'tips': '🔹 STRENGTH #4\nAdd weight via belt. Full range — dead hang to chin over bar. Pull elbows down and back. Control lowering 3 sec.', 'foto': 'pull_up.jpg'},
        {'nama': 'Incline Dumbbell Press', 'detail': '3 sets × 10-12 reps | Rest 90 sec', 'muscle': 'Dada Atas, Bahu Depan', 'tips': '🔹 HYPERTROPHY\nBench at 30°. Lower until elbows at shoulder height. Squeeze chest at top. Tempo 2-1-2.', 'foto': 'incline_press.jpg'},
        {'nama': 'Seated Cable Row', 'detail': '3 sets × 12 reps | Rest 90 sec', 'muscle': 'Mid-Back, Rear Delt', 'tips': '🔹 HYPERTROPHY\nSit tall, chest up. Pull handle to lower chest. Squeeze shoulder blades together. Slow 3 sec return.', 'foto': 'seated_cable_row.jpg'},
        {'nama': 'Lateral Raise + Face Pull', 'detail': '3 sets × 15 reps | Rest 60 sec', 'muscle': 'Deltoid Lateral, Rear Delt', 'tips': '🔹 SUPERSET\n• Lateral Raise: lead with elbows, pause 1 sec at shoulder height, lower 3 sec.\n• Face Pull: pull to face, elbows at shoulder height, rotate hands outward at end.', 'foto': 'lateral_raise.jpg'},
        {'nama': 'EZ-bar Curl + Skull Crusher', 'detail': '3 sets × 12 reps | Rest 90 sec', 'muscle': 'Bisep, Trisep (superset)', 'tips': '🔹 SUPERSET FINISHER\n• EZ Curl: supinate at top, slow 3 sec lowering. Keep elbows at sides.\n• Skull Crusher: lower bar to forehead, elbows pointing up. Extend fully at top.', 'foto': 'dumbbell_curl.jpg'},
    ],
    'Lower A': [
        {'nama': 'Barbell Back Squat', 'detail': '5 sets × 5 reps | Rest 3-4 min', 'muscle': 'Quad, Glute, Hamstring, Core', 'tips': '🔹 STRENGTH #1\nFeet shoulder-width, toes slightly out. Break hips and knees simultaneously. Hit parallel or below. Drive knees out. Log weight every session.', 'foto': 'squat.jpg'},
        {'nama': 'Romanian Deadlift (RDL)', 'detail': '4 sets × 6-8 reps | Rest 2-3 min', 'muscle': 'Hamstring, Glute, Lower Back', 'tips': '🔹 STRENGTH #2\nPush hips back — not down. Bar stays close to legs. Feel maximum stretch at bottom. Squeeze glutes hard at top. Lower 3 sec.', 'foto': 'romanian_deadlift.jpg'},
        {'nama': 'Leg Press', 'detail': '4 sets × 10-12 reps | Rest 90 sec', 'muscle': 'Quad, Glute', 'tips': '🔹 HYPERTROPHY\nFull range — do not lock knees. High wide foot = glutes. Low narrow foot = quads. Control lowering 3 sec.', 'foto': 'leg_press.jpg'},
        {'nama': 'Walking Lunge (Dumbbell)', 'detail': '3 sets × 12 reps/leg | Rest 90 sec', 'muscle': 'Quad, Glute, Stabilizer', 'tips': '🔹 UNILATERAL\nStep forward, drop back knee toward floor. Keep front shin vertical. Drive through front heel to stand. Stay controlled — no wobbling.', 'foto': 'walking_lunge.jpg'},
        {'nama': 'Leg Curl + Leg Extension', 'detail': '3 sets × 15 reps | Rest 60 sec', 'muscle': 'Hamstring, Quad (isolasi)', 'tips': '🔹 SUPERSET ISOLATION\n• Leg Curl: curl to full contraction, squeeze 1 sec, lower 3 sec.\n• Leg Extension: extend fully, squeeze quads 1 sec at top, lower 3 sec.', 'foto': 'leg_curl.jpg'},
        {'nama': 'Standing + Seated Calf Raise', 'detail': '4 sets × 15-20 reps | Rest 60 sec', 'muscle': 'Gastrocnemius, Soleus', 'tips': '🔹 SUPERSET\n• Standing: targets gastrocnemius. Rise on big toe, hold 2 sec at top, lower 3 sec.\n• Seated: targets soleus. Same tempo. Full stretch at bottom.', 'foto': 'calf_raise.jpg'},
        {'nama': 'Plank + Hanging Leg Raise', 'detail': '3 sets × 45 sec / 12 reps | Rest 60 sec', 'muscle': 'Core, Lower Abs', 'tips': '🔹 SUPERSET CORE\n• Plank: squeeze glutes and abs hard. Body in straight line. Breathe steadily.\n• Hanging Leg Raise: posterior pelvic tilt, raise legs to 90°+. Avoid swinging.', 'foto': 'hanging_leg_raise.jpg'},
    ],
    'Upper B': [
        {'nama': 'Dumbbell Flat Press', 'detail': '4 sets × 10-12 reps | Rest 90 sec', 'muscle': 'Dada, Trisep', 'tips': '🔹 HYPERTROPHY #1 — Tempo 2-1-2\nFocus on mind-muscle connection. Feel the chest stretch at bottom. Squeeze hard at top. Do not use momentum.', 'foto': 'bench_press.jpg'},
        {'nama': 'Chest-supported T-bar Row', 'detail': '4 sets × 10-12 reps | Rest 90 sec', 'muscle': 'Mid-Back, Rhomboid, Rear Delt', 'tips': '🔹 HYPERTROPHY #2 — Tempo 2-1-2\nChest on pad removes lower back fatigue. Pull elbows back and up. Squeeze shoulder blades hard at top.', 'foto': 'seated_cable_row.jpg'},
        {'nama': 'Cable Fly (Low to High)', 'detail': '3 sets × 15 reps | Rest 60 sec', 'muscle': 'Dada Atas, Pec Minor', 'tips': '🔹 ISOLATION\nPulleys at lowest position. Arc upward and inward. Squeeze pecs at top. Keep slight elbow bend. Slow controlled movement.', 'foto': 'cable_fly.jpg'},
        {'nama': 'Lat Pulldown (Wide Grip)', 'detail': '4 sets × 12 reps | Rest 90 sec', 'muscle': 'Lats, Teres Major', 'tips': '🔹 HYPERTROPHY\nWide overhand grip. Pull bar to upper chest. Lean back slightly. Squeeze lats hard at bottom. Slow 3 sec return to full stretch.', 'foto': 'pull_up.jpg'},
        {'nama': 'Arnold Press', 'detail': '3 sets × 12 reps | Rest 90 sec', 'muscle': 'Semua Kepala Deltoid', 'tips': '🔹 HYPERTROPHY\nStart with palms facing you, rotate outward as you press up. Full lockout at top. Reverse rotation on way down. Hits all three delt heads.', 'foto': 'arnold_press.jpg'},
        {'nama': 'Face Pull (Cable)', 'detail': '4 sets × 15 reps | Rest 60 sec', 'muscle': 'Rear Delt, Rotator Cuff, Trap', 'tips': '🔹 ISOLATION\nPull toward face, elbows at shoulder height. Rotate hands outward at the end. Essential for shoulder health and posture.', 'foto': 'face_pull.jpg'},
        {'nama': 'Hammer Curl + Overhead Extension', 'detail': '3 sets × 12-15 reps | Rest 60 sec', 'muscle': 'Brachialis, Trisep Long Head', 'tips': '🔹 SUPERSET\n• Hammer Curl: palms facing each other, full range, slow 3 sec lowering.\n• Overhead Extension: elbows close to head, lower behind head until full stretch, extend fully.', 'foto': 'hammer_curl.jpg'},
        {'nama': 'Cable Curl + Pushdown (Finisher)', 'detail': '2 sets × 20 reps | Rest 45 sec', 'muscle': 'Bisep, Trisep', 'tips': '🔹 SUPERSET FINISHER\nLight weight, high reps, pump-focused. No rest between exercises. Full range of motion on both. Feel the burn!', 'foto': 'tricep_pushdown.jpg'},
    ],
    'Lower B': [
        {'nama': 'Conventional Deadlift', 'detail': '4 sets × 5 reps | Rest 3-4 min', 'muscle': 'Posterior Chain, Glute, Trap, Core', 'tips': '🔹 STRENGTH #1\nBar over mid-foot. Hinge at hips, brace core maximally. Drive floor away. Keep bar close to body. Lock out hips and knees simultaneously. LOG WEIGHT.', 'foto': 'romanian_deadlift.jpg'},
        {'nama': 'Bulgarian Split Squat', 'detail': '4 sets × 10 reps/leg | Rest 2 min', 'muscle': 'Quad, Glute (unilateral)', 'tips': '🔹 UNILATERAL\nRear foot elevated on bench. Front foot far enough to keep shin vertical. Drop straight down. Lean slightly forward for more glute activation.', 'foto': 'bulgarian_split_squat.jpg'},
        {'nama': 'Barbell Hip Thrust', 'detail': '4 sets × 12 reps | Rest 90 sec', 'muscle': 'Glute Max, Hamstring', 'tips': '🔹 GLUTE ISOLATION\nUpper back on bench, bar on hips with pad. Drive hips up until body parallel. Squeeze glutes HARD at top — hold 2 sec. Chin tucked. Lower 3 sec.', 'foto': 'hip_thrust.jpg'},
        {'nama': 'Hack Squat / Sissy Squat', 'detail': '3 sets × 12 reps | Rest 90 sec', 'muscle': 'Quad Sweep, VMO', 'tips': '🔹 QUAD ISOLATION\n• Hack Squat: full depth, knees tracking over toes.\n• Sissy Squat: lean back, knees forward past toes for maximum quad stretch.', 'foto': 'hack_squat.jpg'},
        {'nama': 'Good Morning / Back Extension', 'detail': '3 sets × 12-15 reps | Rest 90 sec', 'muscle': 'Hamstring, Erector Spinae', 'tips': '🔹 POSTERIOR CHAIN\nHinge at hips with soft knees. Feel stretch in hamstrings at bottom. Rise until body is straight. Keep back neutral throughout.', 'foto': 'good_morning.jpg'},
        {'nama': 'Cable Kickback + Abductor', 'detail': '3 sets × 15 reps | Rest 60 sec', 'muscle': 'Glute Med, Glute Max (isolasi)', 'tips': '🔹 SUPERSET ISOLATION\n• Cable Kickback: hinge forward, squeeze glute hard at top, control lowering.\n• Abductor machine: push knees outward, squeeze glutes at full abduction, slow return.', 'foto': 'cable_kickback.jpg'},
        {'nama': 'Cable Crunch + Russian Twist', 'detail': '3 sets × 15 reps | Rest 60 sec', 'muscle': 'Rectus Abdominis, Oblique', 'tips': '🔹 SUPERSET CORE FINISHER\n• Cable Crunch: round spine — not hip flex. Squeeze abs hard at bottom.\n• Russian Twist: lean back 45°, feet off floor. Rotate side to side, touch floor each rep.', 'foto': 'cable_crunch.jpg'},
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
😴 *Rest Day*

Your body grows during rest — not just during training!
✅ Sleep 7-8 hours
✅ Eat 1.8-2.2g protein per kg bodyweight
✅ Stay hydrated — minimum 2 liters
✅ Light walk or dynamic stretching is fine

*Progression reminder:*
• Strength (5×5, 4×5-6): add 2.5-5kg when all reps done with good form
• Hypertrophy: add weight when you hit top rep range on all sets
• Deload every 4-6 weeks: reduce volume 40-50% for 1 week 💪"""
        kirim_pesan(msg)
    else:
        latihannya = LATIHAN[nama]
        daftar = '\n'.join([f'⬜ *{l["nama"]}* — {l["detail"]}' for l in latihannya])
        notes = {
            'Upper A': '🔵 *STRENGTH FOCUS* — Beban berat, rep rendah, rest panjang\n💡 Prioritize first 4 compounds — track PR every session',
            'Lower A': '🔵 *STRENGTH + QUAD DOMINANT* — Squat focus\n💡 Log squat weight every session — aim for progressive overload',
            'Upper B': '🟣 *HYPERTROPHY FOCUS* — Volume tinggi, tempo 2-1-2\n💡 Focus on mind-muscle connection — not just moving weight',
            'Lower B': '🟣 *HYPERTROPHY + POSTERIOR DOMINANT* — Deadlift + glute focus\n💡 Deadlift di awal saat tenaga penuh — hip thrust salah satu latihan terbaik untuk glute'
        }
        msg = f"""🌅 *Good Morning, Ali!*

📅 {hari_str}
{emoji} *Today: {nama} — Upper/Lower 4-Day Split*

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
