import cv2
import mediapipe as mp
import random
import time
import wave
import pyaudio
import argparse
from transitions import Machine

ACTIONS = (
    "RightUp",
    "RightNotUp",
    "RightDown",
    "RightNotDown",
    "LeftUp",
    "LeftNotUp",
    "LeftDown",
    "LeftNotDown",
)

INSTRUCTIONS = {
    "en": {
        "RightUp": "Right Up",
        "RightNotUp": "Right Not Up",
        "RightDown": "Right Down",
        "RightNotDown": "Right Not Down",
        "LeftUp": "Left Up",
        "LeftNotUp": "Left Not Up",
        "LeftDown": "Left Down",
        "LeftNotDown": "Left Not Down",
    },
    "ja": {
        "RightUp": "右上げて",
        "RightNotUp": "右上げないで",
        "RightDown": "右下げて",
        "RightNotDown": "右下げないで",
        "LeftUp": "左上げて",
        "LeftNotUp": "左上げないで",
        "LeftDown": "左下げて",
        "LeftNotDown": "左下げないで",
    },
}


VOICE_FILES = {
    "RightUp": "right_up.wav",
    "RightNotUp": "right_not_up.wav",
    "RightDown": "right_down.wav",
    "RightNotDown": "right_not_down.wav",
    "LeftUp": "left_up.wav",
    "LeftNotUp": "left_not_up.wav",
    "LeftDown": "left_down.wav",
    "LeftNotDown": "left_not_down.wav",
}

STATES = ("BothDown", "BothUp", "OnlyRightUp", "OnlyLeftUp")

TRANSITIONS = {
    # when current state is BothDown
    {"trigger": "RightDown", "source": "BothDown", "dest": "BothDown"},
    {"trigger": "LeftDown", "source": "BothDown", "dest": "BothDown"},
    {"trigger": "RightNotUp", "source": "BothDown", "dest": "BothDown"},
    {"trigger": "LeftNotUp", "source": "BothDown", "dest": "BothDown"},
    {"trigger": "RightUp", "source": "BothDown", "dest": "OnlyRightUp"},
    {"trigger": "RightNotDown", "source": "BothDown", "dest": "OnlyRightUp"},
    {"trigger": "LeftUp", "source": "BothDown", "dest": "OnlyLeftUp"},
    {"trigger": "LeftNotDown", "source": "BothDown", "dest": "OnlyLeftUp"},
    # when current state is OnlyRightUp
    {"trigger": "RightDown", "source": "OnlyRightUp", "dest": "BothDown"},
    {"trigger": "RightNotUp", "source": "OnlyRightUp", "dest": "BothDown"},
    {"trigger": "LeftDown", "source": "OnlyRightUp", "dest": "OnlyRightUp"},
    {"trigger": "LeftNotUp", "source": "OnlyRightUp", "dest": "OnlyRightUp"},
    {"trigger": "RightUp", "source": "OnlyRightUp", "dest": "OnlyRightUp"},
    {"trigger": "RightNotDown", "source": "OnlyRightUp", "dest": "OnlyRightUp"},
    {"trigger": "LeftUp", "source": "OnlyRightUp", "dest": "OnlyLeftUp"},
    {"trigger": "LeftNotDown", "source": "OnlyRightUp", "dest": "OnlyLeftUp"},
    # when current state is OnlyLeftUp
    {"trigger": "LeftDown", "source": "OnlyLeftUp", "dest": "BothDown"},
    {"trigger": "LeftNotUp", "source": "OnlyLeftUp", "dest": "BothDown"},
    {"trigger": "RightUp", "source": "OnlyLeftUp", "dest": "BothUp"},
    {"trigger": "RightNotDown", "source": "OnlyLeftUp", "dest": "BothUp"},
    {"trigger": "RightDown", "source": "OnlyLeftUp", "dest": "OnlyLeftUp"},
    {"trigger": "RightNotUp", "source": "OnlyLeftUp", "dest": "OnlyLeftUp"},
    {"trigger": "LeftUp", "source": "OnlyLeftUp", "dest": "OnlyLeftUp"},
    {"trigger": "LeftNotDown", "source": "OnlyLeftUp", "dest": "OnlyLeftUp"},
    # when current state is BothUp
    {"trigger": "RightDown", "source": "BothUp", "dest": "OnlyLeftUp"},
    {"trigger": "RightNotUp", "source": "BothUp", "dest": "OnlyLeftUp"},
    {"trigger": "LeftDown", "source": "BothUp", "dest": "OnlyRightUp"},
    {"trigger": "LeftNotUp", "source": "BothUp", "dest": "OnlyRightUp"},
    {"trigger": "RightUp", "source": "BothUp", "dest": "BothUp"},
    {"trigger": "RightNotDown", "source": "BothUp", "dest": "BothUp"},
    {"trigger": "LeftUp", "source": "BothUp", "dest": "BothUp"},
    {"trigger": "LeftNotDown", "source": "BothUp", "dest": "BothUp"},
}

machine = Machine(states=STATES, transitions=TRANSITIONS, initial="BothDown")


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


def main():
    # command line args
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--lang",
        type=str,
        default="ja",
        help="Language of text and voice in the game",
    )
    args = parser.parse_args()
    lang = args.lang

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
    # TODO: コマンドライン引数で難易度指定して、ここを変える
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

        if (
            current_instruction is None
            or time.time() - instruction_start_time > instruction_duration
        ):
            current_instruction = random.choice(INSTRUCTIONS)
            instruction_start_time = time.time()
            print("New instruction:", current_instruction)
            voice_file = VOICE_FILES[current_instruction]
            play_wav(f"./voice/{lang}/{voice_file}")

        # 指示を画面に表示
        # TODO: 言語によって表示を変える
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

        # TODO: ここで状態管理と正解判定
        # 手があるとき
        hand_type = None
        if results.multi_hand_landmarks:
            for hand_landmarks, handedness in zip(
                results.multi_hand_landmarks, results.multi_handedness
            ):
                # 手のタイプ（右手 or 左手）を判断
                mp_drawing.draw_landmarks(
                    image, hand_landmarks, mp_hands.HAND_CONNECTIONS
                )
                hand_type = handedness.classification[0].label  # 'Right' or 'Left'
                pos = 1000 if hand_type == "Right" else 900
                cv2.putText(
                    image,
                    hand_type,
                    (pos, 50),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 255, 255),
                    2,
                    cv2.LINE_AA,
                )

        cv2.imshow("MediaPipe Hands", image)

        if cv2.waitKey(5) & 0xFF == 27:  # ESCキーで終了
            break

    hands.close()
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
