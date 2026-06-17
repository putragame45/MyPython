import cv2
import mediapipe as mp
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import math
import threading
import time

# ==========================================
# KONFIGURASI & INISIALISASI
# ==========================================
WIDTH, HEIGHT = 1000, 700
NUM_PARTICLES = 800  # Reduced from 1500 untuk performa lebih baik

# ==========================================
# PERFORMANCE FLAGS
# ==========================================
ENABLE_PHYSICS_SIMULATION = False  # Physics disabled for simplified visual style
BURST_HOLD_RATE = 8  # Spawn burst while E is held, every N frames
HSV_CACHE_UPDATE_RATE = 1  # Update HSV color cache setiap N frame
RAINBOW_CHANGE_RATE = 60  # Change rainbow hue offset every second

lock = threading.Lock()
shared_data = {
    "mode": 1,
    "target_x": 0.0,
    "target_y": 0.0,
    "target_z": -12.0,
    "frame": None,
    "frame_ready": False,
    "running": True,
}

# Missing runtime constants (previously referenced elsewhere)
PHYSICS_UPDATE_RATE = 8
TRAIL_UPDATE_RATE = 6
MAX_LASER_PAIRS = 6
MAX_NEIGHBOR_CHECK = 12
NUM_SPHERE = max(1, NUM_PARTICLES // 3)

# Toggles untuk fitur yang bisa diaktifkan lewat keyboard
show_laser = False
show_trails = False

# Trail storage (list of recent positions per particle)
TRAIL_LENGTH = 12
particle_trails = [[] for _ in range(NUM_PARTICLES)]

# ==========================================
# FITUR 1: SOUND EFFECTS SYSTEM
# ==========================================
def init_sounds():
    """Initialize sound effects (jika pygame.mixer tersedia)."""
    try:
        pygame.mixer.init()
        # Buat sound placeholder - akan di-generate secara procedural
        sounds = {
            "mode_change": None,
            "spawn": None,
            "collision": None
        }
        return sounds
    except Exception as e:
        print(f"[WARNING] Sound initialization gagal: {e}")
        return None

# ==========================================
# FITUR 2: PARTICLE SPAWNER - VELOCITY & LIFESPAN
# ==========================================
particle_velocity = np.zeros((NUM_PARTICLES, 3))  # kecepatan setiap partikel
particle_lifetime = np.ones(NUM_PARTICLES) * 255  # lifespan untuk fade effect
GRAVITY = np.array([0.0, -0.02, 0.0])  # gravitasi ringan untuk efek jatuh

# ==========================================
# FITUR 3 & 6: COLOR SHIFTING & SIZE VARIATION
# ==========================================
particle_hue = np.random.uniform(0, 360, NUM_PARTICLES)  # hue untuk rainbow mode
particle_size = np.random.uniform(2.0, 4.5, NUM_PARTICLES)  # ukuran partikel variasi (reduced range)
rainbow_mode = False  # toggle dengan tombol 'R'
hsv_color_cache = np.zeros((NUM_PARTICLES, 3))  # Cache RGB dari HSV untuk performa
rainbow_cycle_offset = 0
burst_hold = False
burst_hold_frame = 0
RAINBOW_CHANGE_RATE = 60  # frame per detik untuk color change setiap detik

# Physics simulation removed from effects.

# ==========================================
# GENERASI DATA BENTUK (PARTIKEL 3D)
# ==========================================
pos_space = np.random.uniform(-4.0, 4.0, (NUM_PARTICLES, 3))

# Mode 2: Black Hole visualization (satu jari telunjuk)
pos_blackhole = np.zeros((NUM_PARTICLES, 3))
NUM_HOLE_DISK = 420
for i in range(NUM_PARTICLES):
    angle = np.random.uniform(0, 2 * np.pi)
    if i < NUM_HOLE_DISK:
        radius = np.random.uniform(0.2, 1.6)
        height = np.random.normal(0.0, 0.06)
    else:
        radius = np.random.uniform(1.8, 3.5)
        height = np.random.normal(0.0, 0.2)
    pos_blackhole[i, 0] = radius * np.cos(angle)
    pos_blackhole[i, 1] = height
    pos_blackhole[i, 2] = radius * np.sin(angle)

# Mode 3: Teks "I LOVE YOU"
text_img = np.zeros((200, 800), dtype=np.uint8)
cv2.putText(text_img, "I LOVE YOU", (20, 130), cv2.FONT_HERSHEY_SIMPLEX, 3.5, 255, 12, cv2.LINE_AA)
y_indices, x_indices = np.where(text_img > 0)
x_text = (x_indices - 400) / 70.0
y_text = -(y_indices - 100) / 70.0
z_text = np.random.uniform(-0.1, 0.1, len(x_text))
text_points = np.stack((x_text, y_text, z_text), axis=-1)
chosen_indices = np.random.choice(len(text_points), NUM_PARTICLES)
pos_text = text_points[chosen_indices]

# Mode 4: Hati
pos_heart = np.zeros((NUM_PARTICLES, 3))
for i in range(NUM_PARTICLES):
    t_val = np.random.uniform(-np.pi, np.pi)
    p_val = np.random.uniform(-np.pi, np.pi)
    x = 2.0 * (np.sin(t_val) ** 3)
    y = 2.0 * np.cos(t_val) - 0.7 * np.cos(2*t_val) - 0.3 * np.cos(3*t_val) - 0.1 * np.cos(4*t_val)
    z = np.sin(p_val) * 0.4
    pos_heart[i, 0] = x * 0.85
    pos_heart[i, 1] = (y * 0.85) + 0.5
    pos_heart[i, 2] = z

# Mode 5 dihapus: tidak ada lagi domain expansion
current_pos = np.copy(pos_space)
target_pos  = np.copy(pos_space)

# ==========================================
# DETEKSI GESTURE
# ==========================================
def hitung_mode_gestur(hand_landmarks):
    """
    Mode 1 - Tangan terbuka (semua jari berdiri)      : Kosmos
    Mode 2 - Satu jari (telunjuk)                     : Black Hole
    Mode 3 - Peace (telunjuk + tengah)                : I LOVE YOU
    Mode 4 - Genggam (semua jari turun)               : Hati
    """
    tips = [8, 12, 16, 20]
    pips = [6, 10, 14, 18]
    jari_berdiri = [
        hand_landmarks.landmark[t].y < hand_landmarks.landmark[p].y
        for t, p in zip(tips, pips)
    ]

    # ---- Mode lain ----
    if sum(jari_berdiri) == 0:
        return 4  # Genggam -> Hati
    if jari_berdiri[0] and jari_berdiri[1] and not any(jari_berdiri[2:]):
        return 3  # Peace -> I LOVE YOU
    if jari_berdiri[0] and not any(jari_berdiri[1:]):
        return 2  # Telunjuk -> Black Hole
    return 1      # Default -> Kosmos

# ==========================================
# THREAD KAMERA (Windows-safe)
# ==========================================
def camera_thread_func():
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    if not cap.isOpened():
        print("[ERROR] Webcam tidak bisa dibuka!")
        shared_data["running"] = False
        return

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 480)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 360)
    cap.set(cv2.CAP_PROP_FPS, 30)

    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(
        max_num_hands=1,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    )

    mode_labels = {
        1: "COSMOS (Terbuka)",
        2: "BLACK HOLE (Satu Jari)",
        3: "I LOVE YOU (Peace)",
        4: "HATI / LOVE (Kepal)"
    }

    while shared_data["running"]:
        ret, frame = cap.read()
        if not ret:
            time.sleep(0.01)
            continue

        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb_frame)

        local_mode = 1
        local_x, local_y, local_z = 0.0, 0.0, -12.0
        finger_positions = {}

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp.solutions.drawing_utils.draw_landmarks(
                    frame, hand_landmarks, mp_hands.HAND_CONNECTIONS
                )
                local_mode = hitung_mode_gestur(hand_landmarks)

                wrist = hand_landmarks.landmark[0]
                local_x = (wrist.x - 0.5) * 10.0
                local_y = -(wrist.y - 0.5) * 7.0

                pinky_mcp = hand_landmarks.landmark[17]
                distance = math.sqrt(
                    (wrist.x - pinky_mcp.x)**2 + (wrist.y - pinky_mcp.y)**2
                )
                local_z = -10.0 - (1.0 / (distance + 0.01)) * 0.2
                

        label_color = (255, 255, 255)
        cv2.putText(
            frame,
            f"MODE: {mode_labels[local_mode]}",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.52,
            label_color,
            2
        )

        cv2.putText(frame, "E - Particle Burst ", (10, 340),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.4, (200, 200, 200), 1)
        
        cv2.putText(frame,"R - Rainbow Mode ", (10, 340),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.4, (200, 200, 200), 1)
        
        cv2.putText(frame, "ESC - Exit", (10, 340),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.4, (200, 200, 200), 1)

        with lock:
            shared_data["mode"]        = local_mode
            shared_data["target_x"]    = local_x
            shared_data["target_y"]    = local_y
            shared_data["target_z"]    = local_z
            shared_data["frame"]       = frame.copy()
            shared_data["frame_ready"] = True

    cap.release()

# ==========================================
# FUNGSI RENDER DOMAIN EXPANSION (OpenGL)
# Dipanggil dari main loop saat current_mode == 5
# ==========================================
def render_domain_expansion(current_pos_arr, phase, expand_t, frame_count):
    """
    Render efek Domain Expansion Gojo:
    1. Shockwave ring saat expand/collapse
    2. Partikel void (warna biru-cyan-putih)
    3. Spiral partikel menuju pusat (Six Eyes)
    4. Cincin konsentris berputar
    5. Inti 'Six Eyes' bercahaya di tengah
    """
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE)  # Additive blending untuk efek cahaya

    t = frame_count

    # ---- 1. PARTIKEL VOID (bola luar) ----
    glPointSize(2.5)
    glBegin(GL_POINTS)
    for i in range(VOID_SPHERE):
        # Warna variasi biru-cyan-putih sesuai kedalaman domain
        depth_factor = (pos_domain[i, 2] + 5.0) / 10.0  # normalize z
        r_col = 0.1 + depth_factor * 0.3
        g_col = 0.4 + depth_factor * 0.4
        b_col = 0.8 + depth_factor * 0.2
        alpha = 0.4 * expand_t
        glColor4f(r_col, g_col, min(b_col, 1.0), alpha)
        glVertex3f(
            current_pos_arr[i, 0],
            current_pos_arr[i, 1],
            current_pos_arr[i, 2]
        )
    glEnd()

    # ---- 2. CINCIN ORBIT (berputar) ----
    glPointSize(3.0)
    glBegin(GL_POINTS)
    for i in range(RING_START, RING_END):
        # Partikel cincin: warna lebih terang, biru muda
        pulse = 0.5 + 0.5 * math.sin(t * 0.04 + i * 0.01)
        alpha = (0.5 + 0.3 * pulse) * expand_t
        glColor4f(0.2, 0.7 + pulse * 0.3, 1.0, alpha)
        glVertex3f(
            current_pos_arr[i, 0],
            current_pos_arr[i, 1],
            current_pos_arr[i, 2]
        )
    glEnd()

    # ---- 3. SPIRAL MENUJU PUSAT ----
    glPointSize(4.0)
    glBegin(GL_POINTS)
    for i in range(RING_END, NUM_DOMAIN):
        # Spiral: makin dekat pusat makin terang/putih
        dist = math.sqrt(
            current_pos_arr[i, 0]**2 +
            current_pos_arr[i, 1]**2 +
            current_pos_arr[i, 2]**2
        )
        brightness = max(0.0, 1.0 - dist / 3.0)
        pulse = 0.5 + 0.5 * math.sin(t * 0.06 + i * 0.05)
        alpha = (0.6 + 0.4 * brightness) * expand_t * pulse
        glColor4f(
            0.5 + brightness * 0.5,   # R: putih di dekat pusat
            0.7 + brightness * 0.3,   # G
            1.0,                       # B: selalu biru
            alpha
        )
        glVertex3f(
            current_pos_arr[i, 0],
            current_pos_arr[i, 1],
            current_pos_arr[i, 2]
        )
    glEnd()

    # ---- 4. INTI SIX EYES (bola kecil bercahaya di pusat) ----
    if expand_t > 0.3:
        eye_alpha = (expand_t - 0.3) / 0.7  # muncul bertahap
        pulse_eye = 0.7 + 0.3 * math.sin(t * 0.1)

        # Lapisan glow luar
        glPointSize(18.0)
        glBegin(GL_POINTS)
        glColor4f(0.3, 0.7, 1.0, 0.15 * eye_alpha * pulse_eye)
        glVertex3f(0.0, 0.0, 0.0)
        glEnd()

        # Lapisan glow tengah
        glPointSize(10.0)
        glBegin(GL_POINTS)
        glColor4f(0.5, 0.85, 1.0, 0.35 * eye_alpha * pulse_eye)
        glVertex3f(0.0, 0.0, 0.0)
        glEnd()

        # Inti putih
        glPointSize(5.0)
        glBegin(GL_POINTS)
        glColor4f(0.9, 0.97, 1.0, 0.95 * eye_alpha)
        glVertex3f(0.0, 0.0, 0.0)
        glEnd()

    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)  # reset blend



# ==========================================
# UPDATE DAN RENDER PARTICLE TRAILS
# ==========================================
def update_particle_trails(current_pos_arr):
    """Update trail positions untuk setiap partikel."""
    for i in range(len(current_pos_arr)):
        if len(particle_trails[i]) >= TRAIL_LENGTH:
            particle_trails[i].pop(0)
        particle_trails[i].append(current_pos_arr[i].copy())

def render_particle_trails(mode):
    """Render garis trail dari partikel - OPTIMIZED."""
    if not show_trails:
        return
        
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE)
    glLineWidth(1.0)
    
    trail_colors = {
        1: (0.1, 0.5, 1.0),
        2: (1.0, 0.6, 0.2),
        3: (0.0, 0.8, 1.0),
        4: (1.0, 0.2, 0.6),
        5: (0.3, 0.9, 1.0)
    }
    
    color = trail_colors.get(mode, trail_colors[1])
    
    glBegin(GL_LINE_STRIP)
    # Render hanya 15 trails (reduced)
    for i in range(0, min(15, NUM_PARTICLES), max(1, NUM_PARTICLES // 10)):
        trail = particle_trails[i]
        if len(trail) > 1:
            for j, pos in enumerate(trail):
                alpha = (j / len(trail)) * 0.3
                glColor4f(color[0], color[1], color[2], alpha)
                glVertex3f(pos[0], pos[1], pos[2])
    glEnd()
    
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

# ==========================================
# RENDER SHOCKWAVE EFFECT
# ==========================================
def render_shockwave(frame_count, strength=1.0):
    """Render gelombang shockwave saat transisi mode - OPTIMIZED."""
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE)
    
    # Gelombang berkembang
    wave_radius = (frame_count % 60) / 60.0 * 8.0
    
    glBegin(GL_LINE_LOOP)
    segments = 32  # reduced dari 64
    for i in range(segments):
        angle = (i / segments) * 2 * np.pi
        oscillate = math.sin(frame_count * 0.1) * 0.2
        r = wave_radius + oscillate
        x = r * math.cos(angle)
        z = r * math.sin(angle)
        
        alpha = max(0, 1.0 - (frame_count % 60) / 60.0) * strength
        glColor4f(0.5, 0.9, 1.0, alpha * 0.5)
        glVertex3f(x, 0.0, z)
    glEnd()
    
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

# ==========================================
# FITUR 2: PARTICLE SPAWNER SYSTEM
# ==========================================
def spawn_particles_at_hand(hand_x, hand_y, hand_z, count=10):
    """
    Spawn partikel baru dari posisi tangan dengan random velocity.
    Fitur: Ledakkan partikel ke segala arah saat tangan bergerak.
    """
    global particle_velocity, particle_lifetime
    # Cari partikel yang sudah "mati" (lifetime rendah) untuk di-spawn ulang
    dead_indices = np.where(particle_lifetime < 50)[0]
    spawn_count = min(count, len(dead_indices))
    
    for i in range(spawn_count):
        idx = dead_indices[i]
        current_pos[idx] = np.array([hand_x, hand_y, hand_z])
        # Random velocity ke segala arah
        angle = np.random.uniform(0, 2*np.pi)
        elevation = np.random.uniform(-np.pi/4, np.pi/4)
        speed = np.random.uniform(0.05, 0.2)
        particle_velocity[idx] = np.array([
            speed * np.cos(angle) * np.cos(elevation),
            speed * np.sin(elevation),
            speed * np.sin(angle) * np.cos(elevation)
        ])
        particle_lifetime[idx] = 255

# ==========================================
# FITUR 3 & 4: UPDATE PARTICLE PHYSICS
# ==========================================
def update_particle_physics(frame_count):
    """
    Update physics: gravitasi dan interaksi partikel dengan integrasi posisi lebih halus.
    """
    global current_pos, particle_velocity, particle_lifetime
    
    if not ENABLE_PHYSICS_SIMULATION:
        return
    
    # Apply gravitasi ringan setiap frame
    particle_velocity += GRAVITY * 0.02
    
    # Hanya lakukan perhitungan tetangga full setiap beberapa frame
    if frame_count % PHYSICS_UPDATE_RATE == 0:
        check_indices = np.arange(0, NUM_PARTICLES, 3)

        for i in check_indices:
            distances = np.linalg.norm(current_pos - current_pos[i], axis=1)
            closest_indices = np.argsort(distances)[1:MAX_NEIGHBOR_CHECK]

            for j in closest_indices:
                diff = current_pos[j] - current_pos[i]
                dist = np.linalg.norm(diff) + 0.001

                if dist < 0.01:
                    continue

                # Attraction jika berada di kisaran radius tarikan
                if REPULSION_RADIUS < dist < ATTRACTION_RADIUS:
                    force = (diff / dist) * ATTRACTION_STRENGTH * 0.35
                    particle_velocity[i] += force

                # Repulsion bila terlalu dekat
                elif dist < REPULSION_RADIUS:
                    force = (diff / dist) * REPULSION_STRENGTH * (1 - dist / REPULSION_RADIUS) * 0.3
                    particle_velocity[i] -= force

        # Hanya turunkan lifetime secara berkala agar tidak menimbulkan loncatan setiap frame
        particle_lifetime -= 1
        particle_lifetime = np.clip(particle_lifetime, 0, 255)

    # Dampening / friction setiap frame untuk menghindari loncatan kecepatan
    particle_velocity *= 0.96

    # Integrasi posisi dengan faktor kecil agar gerakan halus setiap frame
    current_pos += particle_velocity * 0.04

# ==========================================
# FITUR 5: LASER BEAMS RENDERING
# ==========================================
def render_laser_beams(hand_positions):
    """
    Render laser beams dari jari ke partikel utama.
    hand_positions: dict {"thumb": [...], "index": [...], etc}
    """
    if not hand_positions:
        return
    
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE)  # Additive
    glLineWidth(2.5)
    glBegin(GL_LINES)
    
    # Cari partikel terdekat dan hubungkan dengan laser
    finger_positions = list(hand_positions.values())
    
    for pos in finger_positions:
        # Cari partikel terdekat
        distances = np.linalg.norm(current_pos - np.array(pos), axis=1)
        closest_idx = np.argmin(distances)
        closest_dist = distances[closest_idx]
        
        if closest_dist < 15.0:  # hanya jika dekat
            laser_intensity = max(0, 1.0 - closest_dist / 15.0)
            
            # Warna laser: biru ke putih
            glColor4f(0.3 + laser_intensity * 0.7, 0.6 + laser_intensity * 0.4, 1.0, laser_intensity * 0.7)
            glVertex3f(pos[0], pos[1], pos[2])
            glVertex3f(current_pos[closest_idx, 0], current_pos[closest_idx, 1], current_pos[closest_idx, 2])
    
    glEnd()
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

# ==========================================
# FITUR 1: GENERATE SOUND EFFECTS (PROCEDURAL)
# ==========================================
def play_mode_change_sound():
    """Buat dan mainkan sound saat mode berubah."""
    try:
        # Generate simple beep sound procedurally
        sample_rate = 22050
        duration = 0.1  # 100ms
        freq = 800  # Hz
        samples = int(sample_rate * duration)
        
        # Sine wave
        t = np.linspace(0, duration, samples)
        wave = np.sin(2 * np.pi * freq * t) * 0.3
        
        # Fade out
        fade = np.linspace(1, 0, samples)
        wave = wave * fade
        
        # Convert to pygame Sound
        wave = (wave * 32767).astype(np.int16)
        sound = pygame.sndarray.make_sound(wave)
        sound.play()
    except Exception:
        pass  # Silent fail jika audio tidak tersedia

# ==========================================
# JALANKAN THREAD KAMERA
# ==========================================
camera_thread = threading.Thread(target=camera_thread_func, daemon=True)
camera_thread.start()
time.sleep(0.5)

# ==========================================
# INISIALISASI JENDELA cv2 (main thread)
# ==========================================
cv2.namedWindow("Hand Sensor Monitor", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Hand Sensor Monitor", 480, 360)

# ==========================================
# MAIN LOOP: PYGAME + OPENGL
# ==========================================
pygame.init()
pygame.display.set_mode((WIDTH, HEIGHT), DOUBLEBUF | OPENGL)
pygame.display.set_caption("Space Gesture Controller — Domain Expansion Edition")

glMatrixMode(GL_PROJECTION)
glLoadIdentity()
gluPerspective(45, (WIDTH / HEIGHT), 0.1, 50.0)
glMatrixMode(GL_MODELVIEW)
glEnable(GL_DEPTH_TEST)

clock = pygame.time.Clock()
rotation_angle = 0.0
hand_x, hand_y, hand_z = 0.0, 0.0, -12.0
frame_count = 0
prev_hand_x, prev_hand_y, prev_hand_z = 0.0, 0.0, -12.0

# Print optimization info
print("\n" + "="*60)
print("🚀 PERFORMANCE OPTIMIZATION ACTIVE")
print("="*60)
print(f"Particles: {NUM_PARTICLES} (reduced from 1500)")
print(f"Physics Update: Every {PHYSICS_UPDATE_RATE} frames")
print(f"Trail Update: Every {TRAIL_UPDATE_RATE} frames")
print(f"Max Laser Pairs: {MAX_LASER_PAIRS}")
print(f"Neighbors per particle: {MAX_NEIGHBOR_CHECK}")
print("="*60)
print("📱 KEYBOARD CONTROLS:")
print("  R - Rainbow Mode")
print("  E - Hold for Particle Burst")
print("  ESC - Exit")
print("="*60 + "\n")

# Burst hold state
burst_hold = False

prev_mode       = 1    # deteksi transisi masuk mode
prev_mode_for_sound = 1  # Untuk sound effect pada mode change

while shared_data["running"]:
    pygame.event.pump()
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            shared_data["running"] = False
        elif event.type == KEYDOWN:
            if event.key == K_r:
                rainbow_mode = not rainbow_mode  # Toggle rainbow
                if rainbow_mode:
                    play_mode_change_sound()
            elif event.key == K_e:
                burst_hold = True
                spawn_particles_at_hand(hand_x, hand_y, hand_z, count=15)
        elif event.type == KEYUP:
            if event.key == K_e:
                burst_hold = False

    with lock:
        current_mode  = shared_data["mode"]
        target_hand_x = shared_data["target_x"]
        target_hand_y = shared_data["target_y"]
        target_hand_z = shared_data["target_z"]
        frame_ready   = shared_data["frame_ready"]
        frame         = shared_data["frame"]
        hand_fingers  = shared_data.get("hand_fingers", {})
        if frame_ready:
            shared_data["frame_ready"] = False

    # Tampilkan webcam (jaga rasio aspek saat jendela di-resize)
    if frame is not None and frame_ready:
        try:
            _, _, win_w, win_h = cv2.getWindowImageRect("Hand Sensor Monitor")
            if win_w <= 0 or win_h <= 0:
                win_w, win_h = 480, 360
        except Exception:
            win_w, win_h = 480, 360

        # ukuran asli frame
        h, w = frame.shape[:2]
        # skala agar muat ke dalam jendela tanpa mengubah rasio
        scale = min(win_w / w, win_h / h)
        new_w = max(1, int(w * scale))
        new_h = max(1, int(h * scale))

        # canvas hitam ukuran jendela, lalu center frame yang di-resize
        canvas = np.zeros((win_h, win_w, 3), dtype=np.uint8)
        resized = cv2.resize(frame, (new_w, new_h), interpolation=cv2.INTER_AREA)
        x_off = (win_w - new_w) // 2
        y_off = (win_h - new_h) // 2
        canvas[y_off:y_off+new_h, x_off:x_off+new_w] = resized

        cv2.imshow("Hand Sensor Monitor", canvas)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            shared_data["running"] = False

    # Handle E key hold for continuous burst
    if burst_hold and frame_count % BURST_HOLD_RATE == 0:
        spawn_particles_at_hand(hand_x, hand_y, hand_z, count=12)

    # Sound effect saat mode berubah
    if current_mode != prev_mode_for_sound:
        play_mode_change_sound()
        prev_mode_for_sound = current_mode

    prev_mode = current_mode

    # ==========================================
    # RENDER
    # ==========================================
    glClearColor(0.0, 0.0, 0.0, 1.0)

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    # Smooth kamera
    hand_x += (target_hand_x - hand_x) * 0.25
    hand_y += (target_hand_y - hand_y) * 0.25
    hand_z += (target_hand_z - hand_z) * 0.25
    
    # Fitur 2: Spawn particles saat tangan bergerak cepat
    hand_move_dist = math.sqrt(
        (target_hand_x - prev_hand_x)**2 + 
        (target_hand_y - prev_hand_y)**2 + 
        (target_hand_z - prev_hand_z)**2
    )
    if hand_move_dist > 0.4:
        spawn_particles_at_hand(hand_x, hand_y, hand_z, count=5)
    
    prev_hand_x, prev_hand_y, prev_hand_z = target_hand_x, target_hand_y, target_hand_z

    # Pilih target posisi partikel
    if current_mode == 1:
        target_pos = pos_space
        rotation_angle += 0.5
    elif current_mode == 2:
        target_pos = pos_blackhole
        rotation_angle += 2.0
    elif current_mode == 3:
        target_pos = pos_text
        rotation_angle = 0.0
    elif current_mode == 4:
        target_pos = pos_heart
        rotation_angle += 1.5

    # Interpolasi posisi partikel
    lerp_speed = 0.15
    current_pos += (target_pos - current_pos) * lerp_speed
    
    # Update trail particles dengan frequency yang lebih rendah
    if frame_count % TRAIL_UPDATE_RATE == 0:
        update_particle_trails(current_pos)
    
    # ==========================================
    # FITUR 3,4,6: UPDATE PARTICLE PHYSICS
    # ==========================================
    # Physics update setiap frame; perhitungan tetangga berat hanya dilakukan secara berkala
    update_particle_physics(frame_count)

    # Kamera
    if current_mode in [2, 3, 4]:
        glTranslatef(hand_x, hand_y, hand_z)
        if current_mode == 2:
            glRotatef(25, 1.0, 0.0, 0.5)
    else:
        glTranslatef(0.0, 0.0, -12.0)

    glRotatef(rotation_angle, 0.0, 1.0, 0.0)

    # ==========================================
    # RENDER PARTIKEL
    # ==========================================
    # Render mode normal - OPTIMIZED
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glPointSize(3.0)
    
    # Update HSV cache setiap N frame (expensive computation)
    if rainbow_mode and frame_count % HSV_CACHE_UPDATE_RATE == 0:
        for i in range(NUM_PARTICLES):
            hue = (particle_hue[i] + frame_count * 1.5) % 360
            sat = 1.0
            val = 0.8
            c = val * sat
            x = c * (1 - abs((hue / 60) % 2 - 1))
            m = val - c
            
            if 0 <= hue < 60:
                hsv_color_cache[i] = [c+m, x+m, 0+m]
            elif 60 <= hue < 120:
                hsv_color_cache[i] = [x+m, c+m, 0+m]
            elif 120 <= hue < 180:
                hsv_color_cache[i] = [0+m, c+m, x+m]
            elif 180 <= hue < 240:
                hsv_color_cache[i] = [0+m, x+m, c+m]
            elif 240 <= hue < 300:
                hsv_color_cache[i] = [x+m, 0+m, c+m]
            else:
                hsv_color_cache[i] = [c+m, 0+m, x+m]
    
    glBegin(GL_POINTS)
    for i in range(NUM_PARTICLES):
        alpha = particle_lifetime[i] / 255.0
        
        if rainbow_mode:
            glColor4f(hsv_color_cache[i, 0], hsv_color_cache[i, 1], hsv_color_cache[i, 2], alpha * 0.8)
        else:
            if current_mode == 3:
                glColor4f(0.0, 0.8, 1.0, alpha)
            elif current_mode == 4:
                glColor4f(1.0, 0.1, 0.4, alpha)
            elif current_mode == 2 and i >= NUM_SPHERE:
                glColor4f(1.0, 0.7, 0.3, alpha * 0.6)
            elif current_mode == 2 and i < NUM_SPHERE:
                glColor4f(1.0, 0.5, 0.0, alpha)
            else:
                glColor4f(0.1, 0.5, 1.0, alpha * 0.8)
        
        glVertex3f(current_pos[i, 0], current_pos[i, 1], current_pos[i, 2])
    
    glEnd()
    
    # Render particle trails (cahaya mengikuti partikel) - CONDITIONAL
    if show_trails and frame_count % TRAIL_UPDATE_RATE == 0:
        render_particle_trails(current_mode)
    
    # FITUR 5: Render laser beams dari jari ke partikel - CONDITIONAL
    if show_laser and hand_fingers and frame_count % 2 == 0:
        render_laser_beams(hand_fingers)
    
    # Shockwave rendering removed

    pygame.display.flip()
    clock.tick(60)
    frame_count += 1

# ==========================================
# CLEANUP
# ==========================================
shared_data["running"] = False
cv2.destroyAllWindows()
pygame.quit()