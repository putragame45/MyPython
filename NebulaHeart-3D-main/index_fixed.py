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

WIDTH, HEIGHT = 1000, 700
NUM_PARTICLES = 800
BURST_HOLD_RATE = 8
RAINBOW_CHANGE_RATE = 60
GRAVITY = np.array([0.0, -0.01, 0.0], dtype=np.float32)

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

particle_velocity = np.zeros((NUM_PARTICLES, 3), dtype=np.float32)
particle_lifetime = np.ones(NUM_PARTICLES, dtype=np.float32) * 255.0
particle_hue = np.random.uniform(0, 360, NUM_PARTICLES).astype(np.float32)
particle_size = np.random.uniform(2.5, 5.0, NUM_PARTICLES).astype(np.float32)
hsv_color_cache = np.zeros((NUM_PARTICLES, 3), dtype=np.float32)
rainbow_mode = False
rainbow_cycle_offset = 0

def init_sounds():
    try:
        pygame.mixer.init()
        return True
    except Exception:
        return False

sound_enabled = init_sounds()

def hsv_to_rgb(hue: float):
    hue = hue % 360.0
    c = 1.0
    x = c * (1.0 - abs((hue / 60.0) % 2 - 1.0))
    if hue < 60:
        r, g, b = c, x, 0.0
    elif hue < 120:
        r, g, b = x, c, 0.0
    elif hue < 180:
        r, g, b = 0.0, c, x
    elif hue < 240:
        r, g, b = 0.0, x, c
    elif hue < 300:
        r, g, b = x, 0.0, c
    else:
        r, g, b = c, 0.0, x
    return r, g, b

# ==========================================
# Particle layout definitions
# ==========================================
pos_space = np.random.uniform(-4.0, 4.0, (NUM_PARTICLES, 3)).astype(np.float32)

pos_blackhole = np.zeros((NUM_PARTICLES, 3), dtype=np.float32)
NUM_HOLE_DISK = 420
for i in range(NUM_PARTICLES):
    angle = np.random.uniform(0, 2 * np.pi)
    if i < NUM_HOLE_DISK:
        radius = np.random.uniform(0.15, 1.4)
        height = np.random.normal(0.0, 0.05)
    else:
        radius = np.random.uniform(1.8, 3.3)
        height = np.random.normal(0.0, 0.22)
    pos_blackhole[i, 0] = radius * np.cos(angle)
    pos_blackhole[i, 1] = height
    pos_blackhole[i, 2] = radius * np.sin(angle)

text_img = np.zeros((200, 800), dtype=np.uint8)
cv2.putText(text_img, "I LOVE YOU", (20, 130), cv2.FONT_HERSHEY_SIMPLEX, 3.5, 255, 12, cv2.LINE_AA)
y_indices, x_indices = np.where(text_img > 0)
x_text = (x_indices - 400) / 70.0
y_text = -(y_indices - 100) / 70.0
z_text = np.random.uniform(-0.1, 0.1, len(x_text))
text_points = np.stack((x_text, y_text, z_text), axis=-1)
chosen_indices = np.random.choice(len(text_points), NUM_PARTICLES)
pos_text = text_points[chosen_indices].astype(np.float32)

pos_heart = np.zeros((NUM_PARTICLES, 3), dtype=np.float32)
for i in range(NUM_PARTICLES):
    t_val = np.random.uniform(-np.pi, np.pi)
    p_val = np.random.uniform(-np.pi, np.pi)
    x = 2.0 * (math.sin(t_val) ** 3)
    y = 2.0 * math.cos(t_val) - 0.7 * math.cos(2 * t_val) - 0.3 * math.cos(3 * t_val) - 0.1 * math.cos(4 * t_val)
    z = math.sin(p_val) * 0.4
    pos_heart[i, 0] = x * 0.85
    pos_heart[i, 1] = (y * 0.85) + 0.5
    pos_heart[i, 2] = z

current_pos = np.copy(pos_space)
target_pos = np.copy(pos_space)

def hitung_mode_gestur(hand_landmarks):
    tips = [8, 12, 16, 20]
    pips = [6, 10, 14, 18]
    jari_berdiri = [
        hand_landmarks.landmark[t].y < hand_landmarks.landmark[p]
        for t, p in zip(tips, pips)
    ]
    if sum(jari_berdiri) == 0:
        return 4
    if jari_berdiri[0] and jari_berdiri[1] and not any(jari_berdiri[2:]):
        return 3
    if jari_berdiri[0] and not any(jari_berdiri[1:]):
        return 2
    return 1


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
                distance = math.sqrt((wrist.x - pinky_mcp.x) ** 2 + (wrist.y - pinky_mcp.y) ** 2)
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

        cv2.putText(frame, "Tahan E untuk particle burst", (10, 340),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.4, (200, 200, 200), 1)

        with lock:
            shared_data["mode"] = local_mode
            shared_data["target_x"] = local_x
            shared_data["target_y"] = local_y
            shared_data["target_z"] = local_z
            shared_data["frame"] = frame.copy()
            shared_data["frame_ready"] = True

    cap.release()


def spawn_particles_at_hand(hand_x, hand_y, hand_z, count=10):
    dead_indices = np.where(particle_lifetime < 50)[0]
    if len(dead_indices) == 0:
        return
    spawn_count = min(count, len(dead_indices))
    for idx in dead_indices[:spawn_count]:
        current_pos[idx] = np.array([hand_x, hand_y, hand_z], dtype=np.float32)
        angle = np.random.uniform(0, 2 * np.pi)
        elevation = np.random.uniform(-np.pi / 6, np.pi / 6)
        speed = np.random.uniform(0.18, 0.35)
        particle_velocity[idx] = np.array(
            [
                speed * np.cos(angle) * np.cos(elevation),
                speed * np.sin(elevation) * 0.8,
                speed * np.sin(angle) * np.cos(elevation)
            ],
            dtype=np.float32
        )
        particle_lifetime[idx] = 255.0


def update_particles(frame_count):
    global particle_lifetime, particle_velocity, current_pos
    active_mask = particle_lifetime > 0
    particle_lifetime[active_mask] -= 1.0
    particle_lifetime = np.clip(particle_lifetime, 0.0, 255.0)

    fading_mask = particle_lifetime < 100
    particle_velocity[fading_mask, 1] -= 0.0008
    particle_velocity[active_mask] *= 0.985

    current_pos[active_mask] += particle_velocity[active_mask]
    far_mask = np.linalg.norm(current_pos, axis=1) > 12.0
    current_pos[far_mask] *= 0.96


def render_particles(current_mode, frame_count):
    global rainbow_cycle_offset
    if rainbow_mode and frame_count % RAINBOW_CHANGE_RATE == 0:
        rainbow_cycle_offset = (rainbow_cycle_offset + 18) % 360

    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE)
    glPointSize(5.0)
    glBegin(GL_POINTS)
    for i in range(NUM_PARTICLES):
        alpha = (particle_lifetime[i] / 255.0) ** 1.2
        if rainbow_mode:
            hue = (particle_hue[i] + rainbow_cycle_offset) % 360
            r, g, b = hsv_to_rgb(hue)
            color = (r, g, b)
        else:
            if current_mode == 2:
                color = (0.05 + 0.95 * (i / NUM_PARTICLES), 0.02, 0.15)
            elif current_mode == 3:
                color = (0.0, 0.75, 1.0)
            elif current_mode == 4:
                color = (1.0, 0.18, 0.5)
            else:
                color = (0.12, 0.55, 1.0)
        glColor4f(color[0], color[1], color[2], max(alpha * 0.75, 0.05))
        glVertex3f(current_pos[i, 0], current_pos[i, 1], current_pos[i, 2])
    glEnd()

    glPointSize(8.0)
    glBegin(GL_POINTS)
    for i in range(NUM_PARTICLES):
        alpha = (particle_lifetime[i] / 255.0) ** 1.5
        if alpha <= 0.0:
            continue
        if rainbow_mode:
            hue = (particle_hue[i] + rainbow_cycle_offset) % 360
            r, g, b = hsv_to_rgb(hue)
        else:
            if current_mode == 2:
                r, g, b = 0.15, 0.06, 0.2
            elif current_mode == 3:
                r, g, b = 0.1, 0.85, 1.0
            elif current_mode == 4:
                r, g, b = 1.0, 0.18, 0.55
            else:
                r, g, b = 0.2, 0.65, 1.0
        glow_alpha = alpha * 0.12
        glColor4f(r, g, b, glow_alpha)
        glVertex3f(current_pos[i, 0], current_pos[i, 1], current_pos[i, 2])
    glEnd()
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)


def play_mode_change_sound():
    if not sound_enabled:
        return
    try:
        sample_rate = 22050
        duration = 0.08
        freq = 900
        samples = int(sample_rate * duration)
        t = np.linspace(0, duration, samples, False)
        wave = np.sin(2 * np.pi * freq * t) * 0.2
        wave = (wave * np.linspace(1, 0, samples)).astype(np.float32)
        sound = pygame.sndarray.make_sound((wave * 32767).astype(np.int16))
        sound.play()
    except Exception:
        pass

camera_thread = threading.Thread(target=camera_thread_func, daemon=True)
camera_thread.start()
time.sleep(0.5)

cv2.namedWindow("Hand Sensor Monitor", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Hand Sensor Monitor", 480, 360)

pygame.init()
pygame.display.set_mode((WIDTH, HEIGHT), DOUBLEBUF | OPENGL)
pygame.display.set_caption("Space Gesture Controller")

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

print("\n" + "=" * 60)
print("🚀 SPACE GESTURE CONTROLLER REVISED")
print("=" * 60)
print(f"Particles: {NUM_PARTICLES}")
print("Keyboard:")
print("  R - Toggle Rainbow Mode")
print("  E - Hold for Particle Burst")
print("  ESC - Exit")
print("=" * 60 + "\n")

pingame_e_held = False

while shared_data["running"]:
    pygame.event.pump()
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            shared_data["running"] = False
        elif event.type == KEYDOWN:
            if event.key == K_r:
                rainbow_mode = not rainbow_mode
                play_mode_change_sound()
            elif event.key == K_e:
                pingame_e_held = True
                spawn_particles_at_hand(hand_x, hand_y, hand_z, count=15)
        elif event.type == KEYUP:
            if event.key == K_e:
                pingame_e_held = False

    if pingame_e_held and frame_count % BURST_HOLD_RATE == 0:
        spawn_particles_at_hand(hand_x, hand_y, hand_z, count=12)

    with lock:
        current_mode = shared_data["mode"]
        target_hand_x = shared_data["target_x"]
        target_hand_y = shared_data["target_y"]
        target_hand_z = shared_data["target_z"]
        frame_ready = shared_data["frame_ready"]
        frame = shared_data["frame"]
        if frame_ready:
            shared_data["frame_ready"] = False

    if frame is not None and frame_ready:
        try:
            _, _, win_w, win_h = cv2.getWindowImageRect("Hand Sensor Monitor")
            if win_w <= 0 or win_h <= 0:
                win_w, win_h = 480, 360
        except Exception:
            win_w, win_h = 480, 360
        h, w = frame.shape[:2]
        scale = min(win_w / w, win_h / h)
        new_w = max(1, int(w * scale))
        new_h = max(1, int(h * scale))
        canvas = np.zeros((win_h, win_w, 3), dtype=np.uint8)
        resized = cv2.resize(frame, (new_w, new_h), interpolation=cv2.INTER_AREA)
        x_off = (win_w - new_w) // 2
        y_off = (win_h - new_h) // 2
        canvas[y_off:y_off + new_h, x_off:x_off + new_w] = resized
        cv2.imshow("Hand Sensor Monitor", canvas)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            shared_data["running"] = False

    hand_x += (target_hand_x - hand_x) * 0.25
    hand_y += (target_hand_y - hand_y) * 0.25
    hand_z += (target_hand_z - hand_z) * 0.25

    if current_mode == 1:
        target_pos = pos_space
        rotation_angle += 0.5
    elif current_mode == 2:
        target_pos = pos_blackhole
        rotation_angle += 1.2
    elif current_mode == 3:
        target_pos = pos_text
        rotation_angle = 0.0
    elif current_mode == 4:
        target_pos = pos_heart
        rotation_angle += 0.9
    else:
        target_pos = pos_space
        rotation_angle += 0.5

    current_pos += (target_pos - current_pos) * 0.08
    update_particles(frame_count)

    glClearColor(0.0, 0.0, 0.0, 1.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glTranslatef(0.0, 0.0, -12.0)
    glRotatef(rotation_angle, 0.0, 1.0, 0.0)

    render_particles(current_mode, frame_count)

    pygame.display.flip()
    clock.tick(60)
    frame_count += 1

shared_data["running"] = False
cv2.destroyAllWindows()
pygame.quit()
