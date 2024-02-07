import cv2
import mediapipe as mp
import random
import time
import wave
import pyaudio
import argparse
from statemachine import StateMachine
from logzero import logger

# TODO: ここ汚い
# TODO: 名前変える, RaiseRightとか
TRIGGERS = (
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
        "RightUp": "Raise Right.",
        "RightNotUp": "Do not Raise Right.",
        "RightDown": "Lower Right.",
        "RightNotDown": "Do not Lower Right.",
        "LeftUp": "Raise Left.",
        "LeftNotUp": "Do not Raise Left.",
        "LeftDown": "Lower Left.",
        "LeftNotDown": "Do not Lower Left.",
    },
    "ja": {
        "RightUp": "Raise Right.",
        "RightNotUp": "Do not Raise Right.",
        "RightDown": "Lower Right.",
        "RightNotDown": "Do not Lower Right.",
        "LeftUp": "Raise Left.",
        "LeftNotUp": "Do not Raise Left.",
        "LeftDown": "Lower Left.",
        "LeftNotDown": "Do not Lower Left.",
        # "RightUp": "右上げて",
        # "RightNotUp": "右上げないで",
        # "RightDown": "右下げて",
        # "RightNotDown": "右下げないで",
        # "LeftUp": "左上げて",
        # "LeftNotUp": "左上げないで",
        # "LeftDown": "左下げて",
        # "LeftNotDown": "左下げないで",
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


def display_correct_mark(frame, center):
    logger.info("正解")
    # フレーム上にマル（円）を線で描画（円の半径を100に設定）
    cv2.circle(frame, center, 100, (0, 255, 0), thickness=3)  # 緑色の円（線で描画）
    return


def display_incorrect_mark(frame, center):
    logger.info("不正解")
    # フレーム上にバツ（2本の直線）を描画
    cv2.line(
        frame,
        (center[0] - 75, center[1] - 75),
        (center[0] + 75, center[1] + 75),
        (0, 0, 255),
        5,
    )  # 赤色の直線1
    cv2.line(
        frame,
        (center[0] + 75, center[1] - 75),
        (center[0] - 75, center[1] + 75),
        (0, 0, 255),
        5,
    )  # 赤色の直線2
    return


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--lang",
        type=str,
        default="ja",
        help="Language of text and voice in the game",
    )
    args = parser.parse_args()
    lang = args.lang

    machine = StateMachine()

    # initialize mediapipe
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=2,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5,
    )
    mp_drawing = mp.solutions.drawing_utils

    # camera capture
    cap = cv2.VideoCapture(0)

    # instruction
    current_instruction = None
    instruction_start_time = None
    instruction_duration = 3  # 指示の持続時間

    while cap.isOpened():
        success, image = cap.read()
        if not success:
            logger.info("Ignoring empty camera frame.")
            continue

        # フレームの高さと幅を取得
        height, width = image.shape[:2]

        # フレームの中心を計算
        center = (width // 2, height // 2)

        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
        image.flags.writeable = False

        result = hands.process(image)
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        if (
            current_instruction is None
            or time.time() - instruction_start_time > instruction_duration
        ):
            # TODO: ここで更新する前に正解判定をすれば良さそう
            if machine.state == "BothDown":
                display_correct_mark(
                    image, center
                ) if result.multi_handedness is None else display_incorrect_mark(
                    image, center
                )
            elif machine.state == "BothUp":
                display_correct_mark(
                    image, center
                ) if result.multi_handedness is not None and len(
                    result.multi_handedness
                ) == 2 else display_incorrect_mark(image, center)
            elif machine.state == "OnlyRightUp":
                # TODO: ここ汚い
                hand_type = (
                    result.multi_handedness[0].classification[0].label
                    if result.multi_handedness is not None
                    else None
                )
                display_correct_mark(
                    image, center
                ) if hand_type == "Right" else display_incorrect_mark(image, center)
            elif machine.state == "OnlyLeftUp":
                hand_type = (
                    result.multi_handedness[0].classification[0].label
                    if result.multi_handedness is not None
                    else None
                )
                display_correct_mark(
                    image, center
                ) if hand_type == "Left" else display_incorrect_mark(image, center)

            # get new trigger
            current_trigger = random.choice(TRIGGERS)
            # move state
            getattr(machine, current_trigger)()
            logger.info(f"Current correct state: {machine.state}.")
            current_instruction = INSTRUCTIONS[lang][current_trigger]
            instruction_start_time = time.time()
            logger.info(
                f"New instruction: {current_instruction}",
            )
            voice_file = VOICE_FILES[current_trigger]
            play_wav(f"./voice/{lang}/{voice_file}")

        # display instruction
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

        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    image, hand_landmarks, mp_hands.HAND_CONNECTIONS
                )

        cv2.imshow("MediaPipe Hands", image)

        if cv2.waitKey(5) & 0xFF == 27:
            break

    hands.close()
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
