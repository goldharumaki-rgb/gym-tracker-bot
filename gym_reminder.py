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
    5: ('Full Body Pump', '🔥'),
    6: ('Rest Day', '😴')
}

LATIHAN = {
    'Upper A': [
        {
            'nama': 'Incline Barbell Bench Press',
            'detail': '4 sets × 6-8 reps',
            'muscle': 'Upper Chest, Triceps, Front Delts',
            'tips': '🔹 CHEST #1\nRetract scapula, slight arch. Lower bar to upper chest over 3 sec. Drive explosively up. Log weight every session.',
            'foto': 'incline_press.jpg',
            'opsi': [
                ('Incline Dumbbell Press', 'incline_press.jpg'),
                ('Smith Machine Incline Press', 'smith_incline_press.jpg'),
                ('Machine Incline Press', 'chest_press_machine.jpg'),
            ]
        },
        {
            'nama': 'Pull Up',
            'detail': '4 sets × 6-8 reps',
            'muscle': 'Lats, Biceps',
            'tips': '🔹 BACK VERTICAL #1\nFull range — dead hang to chin over bar. Pull elbows down and back. Squeeze lats hard at bottom. Control lowering 3 sec.',
            'foto': 'pull_up.jpg',
            'opsi': [
                ('Lat Pulldown', 'pull_up.jpg'),
                ('Assisted Pull Up', 'assisted_pull_up.jpg'),
                ('Neutral Grip Pulldown', 'neutral_grip_pulldown.jpg'),
            ]
        },
        {
            'nama': 'Flat Dumbbell Press',
            'detail': '3 sets × 8-10 reps',
            'muscle': 'Chest, Triceps',
            'tips': '🔹 CHEST #2\nFeel the chest stretch at bottom. Squeeze hard at top. Tempo 2-1-2. Focus on mind-muscle connection.',
            'foto': 'bench_press.jpg',
            'opsi': [
                ('Barbell Bench Press', 'bench_press.jpg'),
                ('Chest Press Machine', 'chest_press_machine.jpg'),
                ('Push Up Berbeban', 'bench_press.jpg'),
            ]
        },
        {
            'nama': 'T-Bar Row',
            'detail': '3 sets × 8-10 reps',
            'muscle': 'Mid-Back, Rhomboid, Biceps',
            'tips': '🔹 BACK HORIZONTAL #1\nChest on pad. Pull elbows back and up. Squeeze shoulder blades hard at top. Slow 3 sec return.',
            'foto': 'bent_over_row.jpg',
            'opsi': [
                ('Barbell Row', 'bent_over_row.jpg'),
                ('Chest Supported Row', 'seated_cable_row.jpg'),
                ('Seated Cable Row', 'seated_cable_row.jpg'),
            ]
        },
        {
            'nama': 'Seated Dumbbell Shoulder Press',
            'detail': '3 sets × 8-10 reps',
            'muscle': 'All Delt Heads, Triceps',
            'tips': '🔹 SHOULDERS\nDumbbells at ear level. Press up and slightly inward. Full lockout at top. Lower 3 sec.',
            'foto': 'overhead_press.jpg',
            'opsi': [
                ('Arnold Press', 'arnold_press.jpg'),
                ('Smith Shoulder Press', 'smith_incline_press.jpg'),
                ('Machine Shoulder Press', 'chest_press_machine.jpg'),
            ]
        },
        {
            'nama': 'EZ Bar Curl',
            'detail': '3 sets × 10-12 reps',
            'muscle': 'Biceps',
            'tips': '🔹 BICEPS ISOLATION\nKeep elbows at sides. Full range from dead hang to full contraction. Slow 3 sec lowering.',
            'foto': 'dumbbell_curl.jpg',
            'opsi': [
                ('Barbell Curl', 'dumbbell_curl.jpg'),
                ('Dumbbell Curl', 'dumbbell_curl.jpg'),
                ('Cable Curl', 'cable_curl.jpg'),
            ]
        },
        {
            'nama': 'Overhead Cable Extension',
            'detail': '3 sets × 10-12 reps',
            'muscle': 'Triceps Long Head',
            'tips': '🔹 TRICEPS ISOLATION\nElbows close to head. Lower behind head until full stretch. Extend fully at top. Feel the long head stretch.',
            'foto': 'tricep_pushdown.jpg',
            'opsi': [
                ('Skull Crusher', 'skull_crusher.jpg'),
                ('Dumbbell Overhead Extension', 'tricep_pushdown.jpg'),
                ('Machine Tricep Extension', 'tricep_pushdown.jpg'),
            ]
        },
    ],
    'Lower A': [
        {
            'nama': 'Back Squat',
            'detail': '4 sets × 6-8 reps',
            'muscle': 'Quads, Glutes, Hamstrings, Core',
            'tips': '🔹 QUAD #1 — STRENGTH\nFeet shoulder-width, toes slightly out. Hit parallel or below. Drive knees out. Log weight every session.',
            'foto': 'squat.jpg',
            'opsi': [
                ('Front Squat', 'front_squat.jpg'),
                ('Hack Squat', 'hack_squat.jpg'),
                ('Pendulum Squat', 'pendulum_squat.jpg'),
            ]
        },
        {
            'nama': 'Romanian Deadlift',
            'detail': '4 sets × 8-10 reps',
            'muscle': 'Hamstrings, Glutes, Lower Back',
            'tips': '🔹 HAMSTRING #1 — STRENGTH\nPush hips back — not down. Feel maximum stretch at bottom. Squeeze glutes hard at top. Lower 3 sec.',
            'foto': 'romanian_deadlift.jpg',
            'opsi': [
                ('Dumbbell RDL', 'romanian_deadlift.jpg'),
                ('Stiff Leg Deadlift', 'romanian_deadlift.jpg'),
                ('Good Morning', 'good_morning.jpg'),
            ]
        },
        {
            'nama': 'Leg Press',
            'detail': '3 sets × 10-12 reps',
            'muscle': 'Quads, Glutes',
            'tips': '🔹 QUAD #2\nFull range — do not lock knees. High wide foot = glutes. Low narrow foot = quads.',
            'foto': 'leg_press.jpg',
            'opsi': [
                ('Hack Squat', 'hack_squat.jpg'),
                ('Pendulum Squat', 'pendulum_squat.jpg'),
                ('Belt Squat', 'squat.jpg'),
            ]
        },
        {
            'nama': 'Walking Lunge',
            'detail': '3 sets × 12 steps/leg',
            'muscle': 'Quads, Glutes, Stabilizers',
            'tips': '🔹 UNILATERAL\nStep forward, drop back knee toward floor. Keep front shin vertical. Drive through front heel. Stay controlled.',
            'foto': 'walking_lunge.jpg',
            'opsi': [
                ('Reverse Lunge', 'reverse_lunge.jpg'),
                ('Step Up', 'step_up.jpg'),
                ('Smith Split Squat', 'bulgarian_split_squat.jpg'),
            ]
        },
        {
            'nama': 'Standing Calf Raise',
            'detail': '4 sets × 12-15 reps',
            'muscle': 'Gastrocnemius',
            'tips': '🔹 CALVES\nRise on big toe. Hold 2 sec at top. Lower slowly 3 sec — full stretch at bottom. Do not bounce.',
            'foto': 'calf_raise.jpg',
            'opsi': [
                ('Donkey Calf Raise', 'donkey_calf_raise.jpg'),
                ('Leg Press Calf Raise', 'leg_press.jpg'),
            ]
        },
        {
            'nama': 'Cable Crunch',
            'detail': '3 sets × 15-20 reps',
            'muscle': 'Rectus Abdominis',
            'tips': '🔹 CORE\nKneel facing cable. Round your spine — not hip flex. Squeeze abs hard at bottom. Slow 3 sec return.',
            'foto': 'cable_crunch.jpg',
            'opsi': [
                ('Machine Crunch', 'cable_crunch.jpg'),
                ('Decline Sit Up', 'decline_sit_up.jpg'),
            ]
        },
    ],
    'Upper B': [
        {
            'nama': 'Chest Dip',
            'detail': '4 sets × 8-10 reps',
            'muscle': 'Lower Chest, Triceps',
            'tips': '🔹 CHEST #1 — HYPERTROPHY\nLean forward for more chest activation. Lower until shoulders below elbows. Drive up explosively.',
            'foto': 'bench_press.jpg',
            'opsi': [
                ('Decline Bench Press', 'decline_bench_press.jpg'),
                ('Machine Dip', 'machine_dip.jpg'),
                ('Cable Press', 'cable_fly.jpg'),
            ]
        },
        {
            'nama': 'Wide Grip Lat Pulldown',
            'detail': '4 sets × 8-12 reps',
            'muscle': 'Lats, Teres Major',
            'tips': '🔹 BACK VERTICAL — HYPERTROPHY\nWide overhand grip. Pull bar to upper chest. Lean back slightly. Squeeze lats hard at bottom.',
            'foto': 'pull_up.jpg',
            'opsi': [
                ('Pull Up', 'pull_up.jpg'),
                ('Close Grip Pulldown', 'neutral_grip_pulldown.jpg'),
                ('Machine Pulldown', 'neutral_grip_pulldown.jpg'),
            ]
        },
        {
            'nama': 'Machine Chest Press',
            'detail': '3 sets × 10-12 reps',
            'muscle': 'Chest, Triceps',
            'tips': '🔹 CHEST #2 — HYPERTROPHY\nFocus on mind-muscle connection. Feel the stretch at bottom. Squeeze chest hard at top. Tempo 2-1-2.',
            'foto': 'chest_press_machine.jpg',
            'opsi': [
                ('Dumbbell Bench Press', 'bench_press.jpg'),
                ('Smith Press', 'smith_incline_press.jpg'),
                ('Flat Barbell Press', 'bench_press.jpg'),
            ]
        },
        {
            'nama': 'Single Arm Dumbbell Row',
            'detail': '3 sets × 10-12 reps',
            'muscle': 'Mid-Back, Lats, Biceps',
            'tips': '🔹 BACK HORIZONTAL — HYPERTROPHY\nOne arm at a time. Pull elbow back and up. Squeeze shoulder blade at top. Full stretch at bottom.',
            'foto': 'bent_over_row.jpg',
            'opsi': [
                ('Machine Row', 'seated_cable_row.jpg'),
                ('Meadows Row', 'bent_over_row.jpg'),
                ('Seated Cable Row', 'seated_cable_row.jpg'),
            ]
        },
        {
            'nama': 'Cable Lateral Raise',
            'detail': '4 sets × 12-15 reps',
            'muscle': 'Side Delts',
            'tips': '🔹 SHOULDERS — HYPERTROPHY\nCable keeps tension throughout full range. Lead with elbow. Pause 1 sec at shoulder height. Lower slowly 3 sec.',
            'foto': 'lateral_raise.jpg',
            'opsi': [
                ('Dumbbell Lateral Raise', 'lateral_raise.jpg'),
                ('Machine Lateral Raise', 'lateral_raise.jpg'),
            ]
        },
        {
            'nama': 'Incline Dumbbell Curl',
            'detail': '3 sets × 10-12 reps',
            'muscle': 'Biceps Long Head',
            'tips': '🔹 BICEPS — HYPERTROPHY\nIncline position stretches long head maximally. Let arms hang fully. Curl to full contraction. Slow 3 sec lowering.',
            'foto': 'dumbbell_curl.jpg',
            'opsi': [
                ('Preacher Curl', 'preacher_curl.jpg'),
                ('Spider Curl', 'preacher_curl.jpg'),
                ('Bayesian Curl', 'cable_curl.jpg'),
            ]
        },
        {
            'nama': 'Rope Pushdown',
            'detail': '3 sets × 10-12 reps',
            'muscle': 'Triceps',
            'tips': '🔹 TRICEPS — HYPERTROPHY\nUse rope attachment. Spread rope apart at bottom for full contraction. Elbows locked at sides. Slow 3 sec return.',
            'foto': 'tricep_pushdown.jpg',
            'opsi': [
                ('Straight Bar Pushdown', 'tricep_pushdown.jpg'),
                ('V-Bar Pushdown', 'tricep_pushdown.jpg'),
            ]
        },
    ],
    'Lower B': [
        {
            'nama': 'Hack Squat',
            'detail': '4 sets × 8-12 reps',
            'muscle': 'Quads, VMO',
            'tips': '🔹 QUAD #1 — HYPERTROPHY\nFull depth, knees tracking over toes. Feet low and narrow for max quad stretch. Control the eccentric 3 sec.',
            'foto': 'hack_squat.jpg',
            'opsi': [
                ('Front Squat', 'front_squat.jpg'),
                ('Leg Press', 'leg_press.jpg'),
                ('Pendulum Squat', 'pendulum_squat.jpg'),
            ]
        },
        {
            'nama': 'Hip Thrust',
            'detail': '4 sets × 8-12 reps',
            'muscle': 'Glute Max, Hamstrings',
            'tips': '🔹 GLUTES — HYPERTROPHY\nUpper back on bench, bar on hips with pad. Drive hips up until body parallel. Squeeze glutes HARD at top — hold 2 sec.',
            'foto': 'hip_thrust.jpg',
            'opsi': [
                ('Glute Bridge', 'glute_bridge.jpg'),
                ('Smith Hip Thrust', 'hip_thrust.jpg'),
            ]
        },
        {
            'nama': 'Bulgarian Split Squat',
            'detail': '3 sets × 10-12 reps/leg',
            'muscle': 'Quads, Glutes (unilateral)',
            'tips': '🔹 UNILATERAL\nRear foot elevated on bench. Drop straight down. Lean slightly forward for more glute activation. Control every rep.',
            'foto': 'bulgarian_split_squat.jpg',
            'opsi': [
                ('Reverse Lunge', 'reverse_lunge.jpg'),
                ('Step Up', 'step_up.jpg'),
                ('Smith Split Squat', 'bulgarian_split_squat.jpg'),
            ]
        },
        {
            'nama': 'Seated Leg Curl',
            'detail': '3 sets × 10-12 reps',
            'muscle': 'Hamstrings',
            'tips': '🔹 HAMSTRINGS — HYPERTROPHY\nSeated position provides better hamstring stretch. Curl to full contraction. Squeeze 1 sec at top. Lower slowly 3 sec.',
            'foto': 'leg_curl.jpg',
            'opsi': [
                ('Lying Leg Curl', 'leg_curl.jpg'),
                ('Nordic Curl', 'nordic_curl.jpg'),
            ]
        },
        {
            'nama': 'Leg Extension',
            'detail': '3 sets × 12-15 reps',
            'muscle': 'Quads, VMO',
            'tips': '🔹 QUAD FINISHER\nExtend fully. Squeeze quads hard 1 sec at top. Lower slowly 3 sec. Keep back against pad throughout.',
            'foto': 'leg_press.jpg',
            'opsi': [
                ('Single Leg Extension', 'leg_press.jpg'),
                ('Sissy Squat', 'sissy_squat.jpg'),
            ]
        },
        {
            'nama': 'Seated Calf Raise',
            'detail': '4 sets × 15-20 reps',
            'muscle': 'Soleus',
            'tips': '🔹 CALVES — HYPERTROPHY\nTargets soleus. Full stretch at bottom. Rise as high as possible. Hold 2 sec at top. Slow 3 sec lowering.',
            'foto': 'calf_raise.jpg',
            'opsi': [
                ('Single Leg Calf Raise', 'calf_raise.jpg'),
                ('Smith Calf Raise', 'calf_raise.jpg'),
            ]
        },
        {
            'nama': 'Hanging Leg Raise',
            'detail': '3 sets × 15 reps',
            'muscle': 'Lower Abs, Hip Flexors',
            'tips': '🔹 CORE\nHang from bar, posterior pelvic tilt. Raise legs to 90° or higher. Avoid swinging. Lower with full control 3 sec.',
            'foto': 'hanging_leg_raise.jpg',
            'opsi': [
                ('Reverse Crunch', 'cable_crunch.jpg'),
                ('Captain Chair Raise', 'hanging_leg_raise.jpg'),
            ]
        },
    ],
    'Full Body Pump': [
        {
            'nama': 'Smith Incline Press',
            'detail': '3 sets × 10-12 reps',
            'muscle': 'Upper Chest, Triceps',
            'tips': '🔹 CHEST PUMP\nSmith machine allows constant tension. Lower slowly 3 sec. Squeeze upper chest at top.',
            'foto': 'smith_incline_press.jpg',
            'opsi': [
                ('Incline Dumbbell Press', 'incline_press.jpg'),
                ('Machine Incline Press', 'chest_press_machine.jpg'),
            ]
        },
        {
            'nama': 'Chest Supported Row',
            'detail': '3 sets × 10-12 reps',
            'muscle': 'Mid-Back, Rhomboid',
            'tips': '🔹 BACK PUMP\nChest on pad removes lower back fatigue. Pull elbows back and up. Squeeze shoulder blades hard at top.',
            'foto': 'seated_cable_row.jpg',
            'opsi': [
                ('T-Bar Row', 'bent_over_row.jpg'),
                ('Seated Cable Row', 'seated_cable_row.jpg'),
            ]
        },
        {
            'nama': 'Dumbbell Romanian Deadlift',
            'detail': '3 sets × 10-12 reps',
            'muscle': 'Hamstrings, Glutes',
            'tips': '🔹 HAMSTRING PUMP\nDumbbells allow more range of motion. Push hips back. Feel maximum stretch at bottom. Squeeze glutes at top.',
            'foto': 'romanian_deadlift.jpg',
            'opsi': [
                ('Stiff Leg Deadlift', 'romanian_deadlift.jpg'),
                ('Good Morning', 'good_morning.jpg'),
            ]
        },
        {
            'nama': 'Neutral Grip Pulldown',
            'detail': '3 sets × 10-12 reps',
            'muscle': 'Lats, Biceps',
            'tips': '🔹 LAT PUMP\nNeutral grip reduces bicep dominance. Pull bar to upper chest. Squeeze lats hard at bottom. Slow 3 sec return.',
            'foto': 'neutral_grip_pulldown.jpg',
            'opsi': [
                ('Pull Up', 'pull_up.jpg'),
                ('Close Grip Pulldown', 'neutral_grip_pulldown.jpg'),
            ]
        },
        {
            'nama': 'Dumbbell Lateral Raise',
            'detail': '4 sets × 15-20 reps',
            'muscle': 'Side Delts',
            'tips': '🔹 DELT PUMP — WEAK POINT\nLight weight, high reps. Lead with elbows. Pause 1 sec at shoulder height. Slow 3 sec lowering.',
            'foto': 'lateral_raise.jpg',
            'opsi': [
                ('Cable Lateral Raise', 'lateral_raise.jpg'),
                ('Machine Lateral Raise', 'lateral_raise.jpg'),
            ]
        },
        {
            'nama': 'Face Pull',
            'detail': '3 sets × 15-20 reps',
            'muscle': 'Rear Delt, Rotator Cuff, Trap',
            'tips': '🔹 REAR DELT + SHOULDER HEALTH\nPull toward face, elbows at shoulder height. Rotate hands outward at end. Essential for posture and shoulder health.',
            'foto': 'face_pull.jpg',
            'opsi': [
                ('Reverse Pec Deck', 'reverse_pec_deck.jpg'),
                ('Bent Over Lateral Raise', 'lateral_raise.jpg'),
            ]
        },
        {
            'nama': 'Hammer Curl',
            'detail': '3 sets × 12-15 reps',
            'muscle': 'Brachialis, Biceps',
            'tips': '🔹 BICEPS PUMP\nPalms facing each other throughout. Full range of motion. Slow 3 sec lowering.',
            'foto': 'hammer_curl.jpg',
            'opsi': [
                ('Rope Hammer Curl', 'rope_hammer_curl.jpg'),
                ('Cross Body Hammer Curl', 'hammer_curl.jpg'),
            ]
        },
        {
            'nama': 'Cable Pushdown',
            'detail': '3 sets × 12-15 reps',
            'muscle': 'Triceps',
            'tips': '🔹 TRICEPS PUMP\nElbows locked at sides. Full extension at bottom. Squeeze triceps hard at lockout. Slow 3 sec return.',
            'foto': 'tricep_pushdown.jpg',
            'opsi': [
                ('Rope Pushdown', 'tricep_pushdown.jpg'),
                ('V-Bar Pushdown', 'tricep_pushdown.jpg'),
            ]
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
    """Kirim foto opsi gerakan alternatif"""
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
😴 *Sunday — Full Rest Day*

Complete recovery today!
✅ Sleep 7-9 hours
✅ Eat 1.8-2.2g protein per kg bodyweight
✅ Stay hydrated — minimum 2 liters
✅ No training needed today

*Progression reminder:*
• Strength lifts: add 2.5-5kg when all reps done with good form
• Hypertrophy: add weight when you hit top rep range on all sets
• Deload every 4-6 weeks: reduce volume 40-50% for 1 week 💪"""
        else:
            msg = f"""🌅 *Good Morning, Ali!*

📅 {hari_str}
😴 *Wednesday — Active Rest Day*

Light activity only today!
🚶 Walk 30 minutes at easy pace
🧘 Stretching — focus on tight areas
🫧 Foam rolling for recovery
✅ Eat enough protein
✅ Sleep 7-9 hours tonight

Come back stronger tomorrow! 💪"""
        kirim_pesan(msg)

    else:
        latihannya = LATIHAN[nama]
        daftar = '\n'.join([f'⬜ *{l["nama"]}* — {l["detail"]}' for l in latihannya])

        notes = {
            'Upper A': '🔵 *STRENGTH FOCUS*\nBeban berat, rep rendah, rest 2-3 menit\n💡 Track PR on every compound lift',
            'Lower A': '🔵 *STRENGTH FOCUS*\nSquat & RDL heavy — log every session\n💡 Rest 3-4 min on squat and RDL',
            'Upper B': '🟣 *HYPERTROPHY FOCUS*\nTempo 2-1-2, rest 60-90 detik\n💡 Mind-muscle connection — feel every rep',
            'Lower B': '🟣 *HYPERTROPHY FOCUS*\nVolume tinggi, rest 60-90 detik\n💡 Feel the quad & glute pump',
            'Full Body Pump': '🔥 *PUMP & WEAK POINT*\nModerate weight, high reps, short rest\n💡 Lateral raise & face pull are priority today'
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

            # Kirim foto opsi alternatif
            if ex.get('opsi'):
                kirim_opsi(ex['opsi'], script_dir)

    print(f"✅ Morning reminder sent — {nama}")

if __name__ == '__main__':
    reminder_pagi()
    print('Done!')
