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
    0: ('Upper Body Strength', '💪🔵'),
    1: ('Lower Body Strength', '🦵🔵'),
    2: ('Rest Day', '😴'),
    3: ('Upper Body Hypertrophy', '💪🟣'),
    4: ('Lower Body Hypertrophy', '🦵🟣'),
    5: ('Full Body Pump', '🔥'),
    6: ('Rest Day', '😴')
}

LATIHAN = {
    'Upper Body Strength': [
        {'nama': 'Barbell Bench Press', 'detail': '4 sets × 5-8 reps', 'muscle': 'Chest, Triceps, Front Delts', 'tips': '🔹 STRENGTH #1\nRetract scapula, slight arch. Lower bar to lower chest over 3 sec. Drive explosively up. Log weight every session — aim for PR.', 'foto': 'bench_press.jpg'},
        {'nama': 'Weighted Pull Up / Lat Pulldown', 'detail': '4 sets × 5-8 reps', 'muscle': 'Lats, Biceps', 'tips': '🔹 STRENGTH #2\nAdd weight via belt if bodyweight is easy. Full range — dead hang to chin over bar. Pull elbows down and back. Control lowering 3 sec.', 'foto': 'pull_up.jpg'},
        {'nama': 'Incline Dumbbell Press', 'detail': '3 sets × 8-10 reps', 'muscle': 'Upper Chest, Front Delts', 'tips': '🔹 HYPERTROPHY\nBench at 30°. Lower until elbows at shoulder height. Squeeze chest at top. Tempo 2-1-2.', 'foto': 'incline_press.jpg'},
        {'nama': 'Barbell Row', 'detail': '3 sets × 6-8 reps', 'muscle': 'Mid-Back, Rhomboid, Biceps', 'tips': '🔹 STRENGTH\nHinge 45°, brace core hard. Pull bar to belly button. Squeeze lats 1 sec at top. Lower slowly 3 sec.', 'foto': 'bent_over_row.jpg'},
        {'nama': 'Overhead Press', 'detail': '3 sets × 6-8 reps', 'muscle': 'Deltoid, Triceps', 'tips': '🔹 STRENGTH\nBar at clavicle. Press slightly back overhead. Full lockout at top. Lower over 3 sec. Keep core tight.', 'foto': 'overhead_press.jpg'},
        {'nama': 'Barbell Curl', 'detail': '3 sets × 8-10 reps', 'muscle': 'Biceps', 'tips': '🔹 ISOLATION\nKeep elbows at sides. Full range from dead hang to full contraction. Supinate at top. Slow 3 sec lowering.', 'foto': 'dumbbell_curl.jpg'},
        {'nama': 'Skull Crusher', 'detail': '3 sets × 8-10 reps', 'muscle': 'Triceps Long Head', 'tips': '🔹 ISOLATION\nLower bar to forehead, elbows pointing up. Extend fully at top. Keep elbows close together. Control every rep.', 'foto': 'tricep_pushdown.jpg'},
    ],
    'Lower Body Strength': [
        {'nama': 'Back Squat', 'detail': '4 sets × 5-8 reps', 'muscle': 'Quads, Glutes, Hamstrings, Core', 'tips': '🔹 STRENGTH #1\nFeet shoulder-width, toes slightly out. Break hips and knees simultaneously. Hit parallel or below. Drive knees out. Log weight every session.', 'foto': 'squat.jpg'},
        {'nama': 'Romanian Deadlift', 'detail': '4 sets × 6-8 reps', 'muscle': 'Hamstrings, Glutes, Lower Back', 'tips': '🔹 STRENGTH #2\nPush hips back — not down. Bar stays close to legs. Feel maximum stretch at bottom. Squeeze glutes hard at top. Lower 3 sec.', 'foto': 'romanian_deadlift.jpg'},
        {'nama': 'Leg Press', 'detail': '3 sets × 8-10 reps', 'muscle': 'Quads, Glutes', 'tips': '🔹 COMPOUND\nFull range — do not lock knees. High wide foot = glutes. Low narrow foot = quads. Control lowering 3 sec.', 'foto': 'leg_press.jpg'},
        {'nama': 'Walking Lunge', 'detail': '3 sets × 10 steps/leg', 'muscle': 'Quads, Glutes, Stabilizers', 'tips': '🔹 UNILATERAL\nStep forward, drop back knee toward floor. Keep front shin vertical. Drive through front heel to stand. Stay controlled — no wobbling.', 'foto': 'walking_lunge.jpg'},
        {'nama': 'Standing Calf Raise', 'detail': '4 sets × 12-15 reps', 'muscle': 'Gastrocnemius', 'tips': '🔹 ISOLATION\nRise on big toe. Hold 2 sec at top. Lower slowly 3 sec — full stretch at bottom. Do not bounce.', 'foto': 'calf_raise.jpg'},
        {'nama': 'Hanging Leg Raise', 'detail': '3 sets × 12-15 reps', 'muscle': 'Lower Abs, Hip Flexors', 'tips': '🔹 CORE\nHang from bar, posterior pelvic tilt. Raise legs to 90° or higher. Avoid swinging. Lower with full control 3 sec.', 'foto': 'hanging_leg_raise.jpg'},
    ],
    'Upper Body Hypertrophy': [
        {'nama': 'Incline Bench Press', 'detail': '4 sets × 8-12 reps', 'muscle': 'Upper Chest, Triceps', 'tips': '🔹 HYPERTROPHY #1 — Tempo 2-1-2\nFocus on mind-muscle connection. Feel the upper chest stretch at bottom. Squeeze hard at top.', 'foto': 'incline_press.jpg'},
        {'nama': 'Chest Supported Row', 'detail': '4 sets × 8-12 reps', 'muscle': 'Mid-Back, Rhomboid, Rear Delt', 'tips': '🔹 HYPERTROPHY #2 — Tempo 2-1-2\nChest on pad removes lower back fatigue. Pull elbows back and up. Squeeze shoulder blades hard at top.', 'foto': 'seated_cable_row.jpg'},
        {'nama': 'Dumbbell Shoulder Press', 'detail': '3 sets × 10-12 reps', 'muscle': 'All Delt Heads, Triceps', 'tips': '🔹 HYPERTROPHY\nDumbbells at ear level. Press up and slightly inward. Full lockout at top. Lower 3 sec. Control throughout.', 'foto': 'overhead_press.jpg'},
        {'nama': 'Lat Pulldown', 'detail': '3 sets × 10-12 reps', 'muscle': 'Lats, Teres Major', 'tips': '🔹 HYPERTROPHY\nWide overhand grip. Pull bar to upper chest. Lean back slightly. Squeeze lats hard at bottom. Slow 3 sec return.', 'foto': 'pull_up.jpg'},
        {'nama': 'Cable Fly', 'detail': '3 sets × 12-15 reps', 'muscle': 'Chest, Pec Minor', 'tips': '🔹 ISOLATION\nPulleys at chest height. Arc inward and together. Squeeze pecs hard at top. Keep slight elbow bend. Slow controlled movement.', 'foto': 'cable_fly.jpg'},
        {'nama': 'Lateral Raise', 'detail': '4 sets × 12-15 reps', 'muscle': 'Side Delts', 'tips': '🔹 ISOLATION\nLead with elbows. Raise to shoulder height. Pause 1 sec at top. Lower slowly 3 sec. No swinging.', 'foto': 'lateral_raise.jpg'},
        {'nama': 'Hammer Curl', 'detail': '3 sets × 10-12 reps', 'muscle': 'Brachialis, Biceps', 'tips': '🔹 ISOLATION\nPalms facing each other throughout. Full range of motion. Slow 3 sec lowering. Alternate or together.', 'foto': 'hammer_curl.jpg'},
        {'nama': 'Rope Pushdown', 'detail': '3 sets × 10-12 reps', 'muscle': 'Triceps', 'tips': '🔹 ISOLATION\nUse rope attachment. Spread rope apart at bottom for full contraction. Elbows locked at sides. Slow 3 sec return.', 'foto': 'tricep_pushdown.jpg'},
    ],
    'Lower Body Hypertrophy': [
        {'nama': 'Front Squat / Hack Squat', 'detail': '4 sets × 8-12 reps', 'muscle': 'Quads, VMO', 'tips': '🔹 HYPERTROPHY #1\n• Front Squat: bar on front delts, elbows high. More upright torso = more quad focus.\n• Hack Squat: full depth, knees tracking over toes. Feet low for max quad stretch.', 'foto': 'hack_squat.jpg'},
        {'nama': 'Bulgarian Split Squat', 'detail': '3 sets × 10-12 reps/leg', 'muscle': 'Quads, Glutes (unilateral)', 'tips': '🔹 UNILATERAL\nRear foot elevated on bench. Front foot far enough to keep shin vertical. Drop straight down. Lean slightly forward for more glute activation.', 'foto': 'bulgarian_split_squat.jpg'},
        {'nama': 'Leg Curl', 'detail': '4 sets × 10-12 reps', 'muscle': 'Hamstrings', 'tips': '🔹 ISOLATION\nCurl to full contraction. Squeeze 1 sec at top. Lower slowly 3 sec. Do not let hips rise off pad.', 'foto': 'leg_curl.jpg'},
        {'nama': 'Leg Extension', 'detail': '3 sets × 12-15 reps', 'muscle': 'Quads', 'tips': '🔹 ISOLATION\nExtend fully. Squeeze quads hard 1 sec at top. Lower slowly 3 sec. Keep back against pad throughout.', 'foto': 'leg_press.jpg'},
        {'nama': 'Seated Calf Raise', 'detail': '4 sets × 15-20 reps', 'muscle': 'Soleus', 'tips': '🔹 ISOLATION\nTargets soleus (deep calf muscle). Full stretch at bottom. Rise as high as possible. Hold 2 sec at top. Slow 3 sec lowering.', 'foto': 'calf_raise.jpg'},
        {'nama': 'Cable Crunch', 'detail': '3 sets × 15-20 reps', 'muscle': 'Rectus Abdominis', 'tips': '🔹 CORE\nKneel facing cable. Round your spine — not hip flex. Crunch elbows toward knees. Squeeze abs hard at bottom. Slow 3 sec return.', 'foto': 'cable_crunch.jpg'},
    ],
    'Full Body Pump': [
        {'nama': 'Dumbbell Bench Press', 'detail': '3 sets × 10-12 reps', 'muscle': 'Chest, Triceps', 'tips': '🔹 PUMP\nFeel the stretch at bottom. Squeeze chest hard at top. Moderate weight — focus on contraction not load.', 'foto': 'bench_press.jpg'},
        {'nama': 'Pull Up / Lat Pulldown', 'detail': '3 sets × 10-12 reps', 'muscle': 'Lats, Biceps', 'tips': '🔹 PUMP\nFull range of motion. Squeeze lats hard at bottom. Slow controlled lowering. Focus on mind-muscle connection.', 'foto': 'pull_up.jpg'},
        {'nama': 'Leg Press', 'detail': '3 sets × 15 reps', 'muscle': 'Quads, Glutes', 'tips': '🔹 PUMP\nHigh reps, moderate weight. Full range — do not lock knees. Feel the quad burn. Rest 60 sec between sets.', 'foto': 'leg_press.jpg'},
        {'nama': 'Dumbbell Row', 'detail': '3 sets × 10-12 reps', 'muscle': 'Mid-Back, Biceps', 'tips': '🔹 PUMP\nOne arm at a time. Pull elbow back and up. Squeeze shoulder blade at top. Full stretch at bottom. No rotation.', 'foto': 'bent_over_row.jpg'},
        {'nama': 'Lateral Raise', 'detail': '4 sets × 15-20 reps', 'muscle': 'Side Delts', 'tips': '🔹 PUMP — WEAK POINT\nLight weight, high reps. Lead with elbows. Pause 1 sec at shoulder height. Slow 3 sec lowering. Feel the burn!', 'foto': 'lateral_raise.jpg'},
        {'nama': 'Face Pull', 'detail': '3 sets × 15-20 reps', 'muscle': 'Rear Delt, Rotator Cuff', 'tips': '🔹 PUMP + SHOULDER HEALTH\nPull toward face, elbows at shoulder height. Rotate hands outward at end. Essential for posture and shoulder health.', 'foto': 'face_pull.jpg'},
        {'nama': 'Biceps Curl', 'detail': '3 sets × 12-15 reps', 'muscle': 'Biceps', 'tips': '🔹 PUMP\nFull range of motion. Supinate at top. Slow 3 sec lowering. Keep elbows at sides. Feel the stretch at bottom.', 'foto': 'dumbbell_curl.jpg'},
        {'nama': 'Triceps Pushdown', 'detail': '3 sets × 12-15 reps', 'muscle': 'Triceps', 'tips': '🔹 PUMP\nElbows locked at sides. Full extension at bottom. Squeeze triceps hard at lockout. Slow 3 sec return. Light to moderate weight.', 'foto': 'tricep_pushdown.jpg'},
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
😴 *Sunday — Full Rest Day*

Complete recovery today!
✅ Sleep 7-9 hours
✅ Eat 1.8-2.2g protein per kg bodyweight
✅ Stay hydrated — minimum 2 liters
✅ No training — let your body fully recover

*Weekly reminder:*
• Add 2.5-5kg on strength lifts when all reps done with good form
• Deload every 4-6 weeks: reduce volume 40-50% for 1 week 💪"""
        else:
            msg = f"""🌅 *Good Morning, Ali!*

📅 {hari_str}
😴 *Wednesday — Active Rest Day*

Light activity only today!
🚶 Walk 30-45 minutes at easy pace
🧘 Light stretching — focus on tight areas
✅ Eat enough protein to support recovery
✅ Sleep 7-9 hours tonight

Come back stronger tomorrow! 💪"""
        kirim_pesan(msg)

    else:
        latihannya = LATIHAN[nama]
        daftar = '\n'.join([f'⬜ *{l["nama"]}* — {l["detail"]}' for l in latihannya])

        notes = {
            'Upper Body Strength': '🔵 *STRENGTH FOCUS*\nBeban berat, rep rendah, rest 2-3 menit\n💡 Track PR on bench press, pull-up, OHP, and row',
            'Lower Body Strength': '🔵 *STRENGTH FOCUS*\nSquat & deadlift heavy — log every session\n💡 Rest 3-4 min on squat and RDL',
            'Upper Body Hypertrophy': '🟣 *HYPERTROPHY FOCUS*\nTempo 2-1-2, rest 60-90 detik\n💡 Mind-muscle connection — feel every rep',
            'Lower Body Hypertrophy': '🟣 *HYPERTROPHY FOCUS*\nVolume tinggi, rest 60-90 detik\n💡 Feel the quad & hamstring pump',
            'Full Body Pump': '🔥 *PUMP & WEAK POINT*\nModerate weight, high reps, short rest\n💡 Focus on lagging muscles — lateral raise & face pull priority'
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
