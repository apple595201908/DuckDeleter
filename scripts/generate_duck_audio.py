import os
import sys
import math
import wave
import subprocess
import numpy as np

sys.stdout.reconfigure(encoding='utf-8')

SAMPLE_RATE = 44100
ASSETS_DIR = r"c:\Users\user\Desktop\MonsterDeleter\assets\音频"

def save_wav(filename, samples, sample_rate=SAMPLE_RATE):
    """Save float numpy array (-1.0 to 1.0) as 16-bit PCM WAV."""
    samples = np.clip(samples, -0.99, 0.99)
    int_samples = (samples * 32767).astype(np.int16)
    
    # If mono, convert to stereo
    if len(int_samples.shape) == 1:
        stereo_samples = np.column_stack((int_samples, int_samples))
    else:
        stereo_samples = int_samples
        
    with wave.open(filename, 'w') as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(stereo_samples.tobytes())

def convert_to_mp3_and_mp4(wav_path, mp3_path, mp4_path=None):
    """Convert wav to high-quality mp3 and optional mp4 using ffmpeg."""
    cmd_mp3 = ["ffmpeg", "-y", "-i", wav_path, "-ar", "44100", "-ac", "2", "-b:a", "192k", mp3_path]
    subprocess.run(cmd_mp3, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"Created MP3: {mp3_path}")
    
    if mp4_path:
        cmd_mp4 = ["ffmpeg", "-y", "-i", wav_path, "-ar", "44100", "-ac", "2", "-c:a", "aac", "-b:a", "192k", mp4_path]
        subprocess.run(cmd_mp4, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"Created MP4: {mp4_path}")

# -------------------------------------------------------------
# 1. Cute Duck Quack Synthesizer ("呱呱！嘎嘎！")
# -------------------------------------------------------------
def synthesize_duck_quack():
    duration = 1.6
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), endpoint=False)
    audio = np.zeros_like(t)
    
    def generate_single_quack(start_time, length=0.22, base_freq=380, end_freq=240, volume=0.8):
        start_idx = int(start_time * SAMPLE_RATE)
        num_samples = int(length * SAMPLE_RATE)
        sub_t = np.linspace(0, length, num_samples, endpoint=False)
        
        # Pitch glide (starts slightly higher, glides down with expressive duck inflection)
        freq_env = base_freq + (end_freq - base_freq) * (sub_t / length) ** 0.8
        phase = 2 * np.pi * np.cumsum(freq_env) / SAMPLE_RATE
        
        # Harmonic rich pulse/saw waveform
        raw = np.sin(phase) + 0.7 * np.sin(2 * phase) + 0.5 * np.sin(3 * phase) + 0.4 * np.sin(4 * phase) + 0.3 * np.sin(5 * phase)
        
        # Add duck nasal formant resonance around 800Hz and 2200Hz
        formant1 = np.sin(2 * np.pi * 820 * sub_t) * np.exp(-sub_t * 12)
        formant2 = np.sin(2 * np.pi * 2300 * sub_t) * np.exp(-sub_t * 20)
        quack = raw * (1.0 + 0.6 * formant1 + 0.3 * formant2)
        
        # Amplitude envelope (sharp attack, nasal sustain, quick release)
        env = np.sin(np.pi * (sub_t / length) ** 0.6) ** 1.5
        quack = quack * env * volume
        
        end_idx = min(start_idx + num_samples, len(audio))
        audio[start_idx:end_idx] += quack[:end_idx - start_idx]

    # Double cute quack: "Quack! ... Quack-quack!"
    generate_single_quack(start_time=0.08, length=0.20, base_freq=420, end_freq=260, volume=0.85)
    generate_single_quack(start_time=0.35, length=0.24, base_freq=480, end_freq=290, volume=0.95)
    generate_single_quack(start_time=0.68, length=0.18, base_freq=390, end_freq=250, volume=0.70)
    
    # Add subtle cute sparkle chime
    for i, note in enumerate([1046.5, 1318.5, 1567.98]): # C6, E6, G6
        chime_t = np.linspace(0, 0.4, int(SAMPLE_RATE * 0.4))
        chime = np.sin(2 * np.pi * note * chime_t) * np.exp(-chime_t * 10) * 0.15
        s_idx = int((0.95 + i * 0.08) * SAMPLE_RATE)
        e_idx = min(s_idx + len(chime), len(audio))
        audio[s_idx:e_idx] += chime[:e_idx - s_idx]
        
    return audio

# -------------------------------------------------------------
# 2. Cute Duck Chomping & Eating Synthesizer ("大口吃掉/嚼嚼/咕嚕吞下")
# -------------------------------------------------------------
def synthesize_duck_eating():
    duration = 2.0
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), endpoint=False)
    audio = np.zeros_like(t)

    # 1. Big Cartoon CHOMP! (0.05s)
    chomp_len = 0.12
    c_t = np.linspace(0, chomp_len, int(SAMPLE_RATE * chomp_len))
    c_freq = 650 * np.exp(-c_t * 35) + 120
    c_phase = 2 * np.pi * np.cumsum(c_freq) / SAMPLE_RATE
    chomp = (np.sin(c_phase) + 0.4 * np.sin(2 * c_phase)) * np.exp(-c_t * 24) * 0.85
    # Add teeth snap click
    snap = np.random.uniform(-0.6, 0.6, len(c_t)) * np.exp(-c_t * 90) * 0.4
    s1_idx = int(0.05 * SAMPLE_RATE)
    audio[s1_idx:s1_idx + len(c_t)] += (chomp + snap)

    # 2. Chewing sounds "Nom Nom Nom!" (0.32s, 0.58s, 0.82s)
    for chew_idx, chew_time in enumerate([0.32, 0.58, 0.82]):
        n_len = 0.14
        n_t = np.linspace(0, n_len, int(SAMPLE_RATE * n_len))
        f_start = 320 + chew_idx * 30
        n_freq = f_start * np.exp(-n_t * 22) + 140
        n_phase = 2 * np.pi * np.cumsum(n_freq) / SAMPLE_RATE
        nom = np.sin(n_phase) * np.sin(np.pi * (n_t / n_len)) * 0.55
        # Soft squish
        squish = np.sin(2 * np.pi * 550 * n_t) * np.exp(-n_t * 30) * 0.25
        idx = int(chew_time * SAMPLE_RATE)
        audio[idx:idx + len(n_t)] += (nom + squish)

    # 3. Big Happy Gulp! "咕嚕~" (1.12s)
    g_len = 0.28
    g_t = np.linspace(0, g_len, int(SAMPLE_RATE * g_len))
    g_freq = 280 + 160 * np.sin(np.pi * (g_t / g_len)) - 60 * (g_t / g_len)
    g_phase = 2 * np.pi * np.cumsum(g_freq) / SAMPLE_RATE
    gulp = np.sin(g_phase) * (np.sin(np.pi * (g_t / g_len)) ** 1.3) * 0.75
    # Bubble resonance
    bubble = np.sin(2 * np.pi * 650 * g_t) * np.exp(-g_t * 16) * 0.3
    g_idx = int(1.12 * SAMPLE_RATE)
    audio[g_idx:g_idx + len(g_t)] += (gulp + bubble)

    # 4. Joyful satisfaction chime & sparkle (1.45s)
    for i, freq in enumerate([1046.5, 1318.5, 1567.98, 2093.0]): # C6, E6, G6, C7
        ch_time = 1.45 + i * 0.07
        ch_idx = int(ch_time * SAMPLE_RATE)
        c_len = 0.4
        c_t = np.linspace(0, c_len, int(SAMPLE_RATE * c_len))
        chime = np.sin(2 * np.pi * freq * c_t) * np.exp(-c_t * 9) * 0.2
        e_idx = min(ch_idx + len(chime), len(audio))
        audio[ch_idx:e_idx] += chime[:e_idx - ch_idx]

    return audio

# -------------------------------------------------------------
# 3. Cute Pop Sparkle Explosion ("啵！星星羽毛炸裂")
# -------------------------------------------------------------
def synthesize_pop_explosion():
    duration = 1.8
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), endpoint=False)
    audio = np.zeros_like(t)
    
    # 1. Cartoon Spring "POP!" (rapid frequency pitch drop)
    pop_len = 0.14
    pop_t = np.linspace(0, pop_len, int(SAMPLE_RATE * pop_len))
    pop_freq = 950 * np.exp(-pop_t * 30) + 60
    pop_phase = 2 * np.pi * np.cumsum(pop_freq) / SAMPLE_RATE
    pop_env = np.exp(-pop_t * 22)
    pop_sound = (np.sin(pop_phase) + 0.3 * np.sin(2 * pop_phase)) * pop_env * 0.9
    audio[0:len(pop_sound)] += pop_sound
    
    # 2. Soft Cloud Poof (Bandpassed filtered noise)
    noise_len = 0.6
    noise_samples = int(SAMPLE_RATE * noise_len)
    raw_noise = np.random.uniform(-1, 1, noise_samples)
    # Simple lowpass moving average
    kernel_size = 25
    filtered_noise = np.convolve(raw_noise, np.ones(kernel_size)/kernel_size, mode='same')
    noise_env = np.exp(-np.linspace(0, noise_len, noise_samples) * 8)
    audio[0:noise_samples] += filtered_noise * noise_env * 0.45
    
    # 3. Magical Star Chimes Cascade (Glissando of high crystal notes)
    scale = [783.99, 987.77, 1174.66, 1318.51, 1567.98, 1975.53, 2349.32, 2793.83] # G5 to F7
    for i, freq in enumerate(scale):
        s_time = 0.04 + i * 0.045
        s_idx = int(s_time * SAMPLE_RATE)
        c_len = 0.55
        c_t = np.linspace(0, c_len, int(SAMPLE_RATE * c_len))
        # Bell sound: fundamental + octaves with harmonic decay
        bell = (np.sin(2 * np.pi * freq * c_t) + 
                0.4 * np.sin(2 * np.pi * freq * 2 * c_t) + 
                0.2 * np.sin(2 * np.pi * freq * 3 * c_t)) * np.exp(-c_t * 8)
        e_idx = min(s_idx + len(bell), len(audio))
        audio[s_idx:e_idx] += bell[:e_idx - s_idx] * 0.22
        
    return audio

# -------------------------------------------------------------
# 3. Cheerful Duck March BGM ("歡樂小黃鴨圓舞曲")
# -------------------------------------------------------------
def synthesize_duck_bgm():
    bpm = 130
    beat_dur = 60.0 / bpm
    total_bars = 8
    total_beats = total_bars * 4
    duration = total_beats * beat_dur
    
    total_samples = int(SAMPLE_RATE * duration)
    audio = np.zeros(total_samples)
    
    # Helper note frequencies (MIDI to Hz)
    def m2f(midi_note):
        return 440.0 * (2.0 ** ((midi_note - 69) / 12.0))
    
    # Marimba mallet synthesizer
    def play_marimba(start_beat, midi_note, dur_beats=0.8, vol=0.35):
        freq = m2f(midi_note)
        s_idx = int(start_beat * beat_dur * SAMPLE_RATE)
        note_dur = dur_beats * beat_dur
        num_s = int(note_dur * SAMPLE_RATE)
        t = np.linspace(0, note_dur, num_s, endpoint=False)
        
        # Marimba timbre: woody thump + soft sine harmonics
        wood_click = np.random.uniform(-0.5, 0.5, num_s) * np.exp(-t * 80)
        sine1 = np.sin(2 * np.pi * freq * t) * np.exp(-t * 9)
        sine2 = 0.4 * np.sin(2 * np.pi * freq * 3.95 * t) * np.exp(-t * 22) # Overtones
        sine3 = 0.2 * np.sin(2 * np.pi * freq * 9.8 * t) * np.exp(-t * 45)
        
        sample = (sine1 + sine2 + sine3 + wood_click * 0.3) * vol
        e_idx = min(s_idx + num_s, len(audio))
        audio[s_idx:e_idx] += sample[:e_idx - s_idx]

    # Bouncy Bass synthesizer
    def play_bass(start_beat, midi_note, dur_beats=0.6, vol=0.45):
        freq = m2f(midi_note)
        s_idx = int(start_beat * beat_dur * SAMPLE_RATE)
        note_dur = dur_beats * beat_dur
        num_s = int(note_dur * SAMPLE_RATE)
        t = np.linspace(0, note_dur, num_s, endpoint=False)
        
        # Plucked acoustic bass
        b = (np.sin(2 * np.pi * freq * t) + 0.5 * np.sin(2 * np.pi * freq * 2 * t)) * np.exp(-t * 7)
        e_idx = min(s_idx + num_s, len(audio))
        audio[s_idx:e_idx] += b[:e_idx - s_idx] * vol

    # Upbeat percussion (cute kick & light hihat)
    for b in range(total_beats):
        s_idx = int(b * beat_dur * SAMPLE_RATE)
        # Kick on 1 and 3
        if b % 2 == 0:
            k_t = np.linspace(0, 0.12, int(SAMPLE_RATE * 0.12))
            k_freq = 150 * np.exp(-k_t * 35) + 40
            kick = np.sin(2 * np.pi * np.cumsum(k_freq) / SAMPLE_RATE) * np.exp(-k_t * 25) * 0.4
            e_idx = min(s_idx + len(kick), len(audio))
            audio[s_idx:e_idx] += kick[:e_idx - s_idx]
        # Hihat tap on every beat and offbeat
        hh_t = np.linspace(0, 0.05, int(SAMPLE_RATE * 0.05))
        hh = np.random.uniform(-1, 1, len(hh_t)) * np.exp(-hh_t * 70) * 0.08
        e_idx = min(s_idx + len(hh), len(audio))
        audio[s_idx:e_idx] += hh[:e_idx - s_idx]

    # Bassline pattern (Oom-pah)
    bass_notes = [
        36, 43, 36, 43,  # C
        36, 43, 36, 43,  # C
        41, 48, 41, 48,  # F
        36, 43, 36, 43,  # C
        43, 50, 43, 50,  # G
        41, 48, 41, 48,  # F
        36, 43, 38, 40,  # C - D - E
        36, 43, 36, 36   # C
    ]
    for i, note in enumerate(bass_notes):
        if i < total_beats:
            play_bass(i, note, dur_beats=0.45, vol=0.42)

    # Cheerful Melody (Marimba & Glockenspiel)
    # C Major happy bouncy duck melody
    melody_events = [
        # Bar 1 (C Major)
        (0.0, 72, 0.4), (0.5, 72, 0.4), (1.0, 74, 0.4), (1.5, 76, 0.4), (2.0, 72, 0.8), (3.0, 67, 0.8),
        # Bar 2
        (4.0, 69, 0.4), (4.5, 71, 0.4), (5.0, 72, 0.8), (6.0, 76, 0.4), (6.5, 77, 0.4), (7.0, 79, 0.8),
        # Bar 3 (F Major)
        (8.0, 81, 0.4), (8.5, 81, 0.4), (9.0, 79, 0.4), (9.5, 77, 0.4), (10.0, 76, 0.8), (11.0, 72, 0.8),
        # Bar 4 (C Major)
        (12.0, 74, 0.4), (12.5, 72, 0.4), (13.0, 74, 0.8), (14.0, 76, 0.8), (15.0, 79, 0.8),
        # Bar 5 (G Major)
        (16.0, 81, 0.4), (16.5, 81, 0.4), (17.0, 79, 0.4), (17.5, 77, 0.4), (18.0, 79, 0.8), (19.0, 76, 0.8),
        # Bar 6 (F Major)
        (20.0, 77, 0.4), (20.5, 76, 0.4), (21.0, 74, 0.4), (21.5, 72, 0.4), (22.0, 71, 0.8), (23.0, 67, 0.8),
        # Bar 7 & 8 (Resolution cadence)
        (24.0, 72, 0.4), (24.5, 74, 0.4), (25.0, 76, 0.4), (25.5, 79, 0.4), (26.0, 81, 0.8), (27.0, 84, 0.8),
        (28.0, 84, 0.4), (28.5, 83, 0.4), (29.0, 81, 0.4), (29.5, 79, 0.4), (30.0, 72, 1.5)
    ]

    for start_b, note, dur_b in melody_events:
        play_marimba(start_b, note, dur_b, vol=0.38)
        # Double with a soft upper glockenspiel octave for extra sweetness
        if note >= 72:
            play_marimba(start_b, note + 12, dur_b * 0.6, vol=0.15)

    return audio

def main():
    os.makedirs(ASSETS_DIR, exist_ok=True)
    temp_dir = os.path.join(ASSETS_DIR, "_temp_wav")
    os.makedirs(temp_dir, exist_ok=True)
    
    print("Generating Duck Audio assets...")
    
    # 1. Duck Quack Voice
    quack_audio = synthesize_duck_quack()
    quack_wav = os.path.join(temp_dir, "quack.wav")
    save_wav(quack_wav, quack_audio)
    convert_to_mp3_and_mp4(quack_wav, os.path.join(ASSETS_DIR, "duck_quack.mp3"))
    convert_to_mp3_and_mp4(quack_wav, os.path.join(ASSETS_DIR, "怪兽说话.mp3"))

    # 2. Duck Chomping & Eating SFX
    eat_audio = synthesize_duck_eating()
    eat_wav = os.path.join(temp_dir, "eat.wav")
    save_wav(eat_wav, eat_audio)
    convert_to_mp3_and_mp4(eat_wav, os.path.join(ASSETS_DIR, "duck_eat.mp3"))

    # 3. Pop Sparkle Explosion
    pop_audio = synthesize_pop_explosion()
    pop_wav = os.path.join(temp_dir, "pop.wav")
    save_wav(pop_wav, pop_audio)
    convert_to_mp3_and_mp4(pop_wav, os.path.join(ASSETS_DIR, "duck_pop.mp3"))
    convert_to_mp3_and_mp4(pop_wav, os.path.join(ASSETS_DIR, "爆炸.mp3"), os.path.join(ASSETS_DIR, "爆炸.MP4"))

    # 4. Cheerful Duck BGM
    bgm_audio = synthesize_duck_bgm()
    bgm_wav = os.path.join(temp_dir, "bgm.wav")
    save_wav(bgm_wav, bgm_audio)
    convert_to_mp3_and_mp4(bgm_wav, os.path.join(ASSETS_DIR, "duck_bgm.mp3"))
    convert_to_mp3_and_mp4(bgm_wav, os.path.join(ASSETS_DIR, "bgm(1).mp3"))
    
    # Clean temp directory
    try:
        import shutil
        shutil.rmtree(temp_dir)
    except Exception:
        pass
        
    print("All Duck Audio assets generated successfully!")

if __name__ == "__main__":
    main()
