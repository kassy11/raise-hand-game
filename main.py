import cv2
import mediapipe as mp
import random
import time
import wave
import pyaudio


INSTRUCTIONS = (
    "Right Up",
    "Right Not Up",
    "Right Down",
    "Right Not Down",
    "Left Up",
    "Left Not Up",
    "Left Down",
    "Left Not Down",
)

VOICE_FILES = {
    "Right Up": "right_up.wav",
    "Right Not Up": "right_not_up.wav",
    "Right Down": "right_down.wav",
    "Right Not Down": "right_not_down.wav",
    "Left Up": "left_up.wav",
    "Left Not Up": "left_not_up.wav",
    "Left Down": "left_down.wav",
    "Left Not Down": "left_not_down.wav",
}


def play_wav(filename):
    wav_file = wave.open(filename, "rb")
    p = pyaudio.PyAudio()
    stream = p.open(
        format=p.get_format_from_width(wav_file.getsampwidth()),
        channels=wav_file.getnchannels(),
        rate=wav_file.getframerate(),
        output=True,
    )

    data = wav_file.readframes(1024)
    while data:
        stream.write(data)
        data = wav_file.readframes(1024)

    stream.stop_stream()
    stream.close()
    p.terminate()


# MediaPipeの初期化
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5,
)
mp_drawing = mp.solutions.drawing_utils

# カメラキャプチャの開始
cap = cv2.VideoCapture(0)

# ゲーム状態管理用
current_instruction = None
instruction_start_time = None
instruction_duration = 5  # 指示の持続時間

while cap.isOpened():
    success, image = cap.read()
    if not success:
        print("Ignoring empty camera frame.")
        continue

    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
    image.flags.writeable = False

    results = hands.process(image)

    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    # 新しい指示の生成と表示
    if (
        current_instruction is None
        or time.time() - instruction_start_time > instruction_duration
    ):
        current_instruction = random.choice(INSTRUCTIONS)
        instruction_start_time = time.time()
        print("New instruction:", current_instruction)
        # 音声の再生
        voice_file = VOICE_FILES[current_instruction]
        play_wav("./voice/" + voice_file)

    # 指示を画面に表示
    # TODO: 日本語表示に変更する
    cv2.putText(
        image,
        current_instruction,
        (10, 50),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 0, 255),
        2,
        cv2.LINE_AA,
    )

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    cv2.imshow("MediaPipe Hands", image)

    if cv2.waitKey(5) & 0xFF == 27:  # ESCキーで終了
        break

hands.close()
cap.release()
cv2.destroyAllWindows()
