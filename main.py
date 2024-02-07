import cv2
import mediapipe as mp
import random
import time
import wave
import pyaudio
import argparse
from statemachine import StateMachine
from logzero import logger

TRIGGERS = (
    "RaiseRight",
    "DoNotRaiseRight",
    "LowerRight",
    "DoNotLowerRight",
    "RaiseLeft",
    "DoNotRaiseLeft",
    "LowerLeft",
    "DoNotLowerLeft",
)

INSTRUCTIONS = {
    "en": {
        "RaiseRight": "Raise Right.",
        "DoNotRaiseRight": "Do not Raise Right.",
        "LowerRight": "Lower Right.",
        "DoNotLowerRight": "Do not Lower Right.",
        "RaiseLeft": "Raise Left.",
        "DoNotRaiseLeft": "Do not Raise Left.",
        "LowerLeft": "Lower Left.",
        "DoNotLowerLeft": "Do not Lower Left.",
    },
    "ja": {
        # TODO: 文字表示の日本語対応
        "RaiseRight": "Raise Right.",
        "DoNotRaiseRight": "Do not Raise Right.",
        "LowerRight": "Lower Right.",
        "DoNotLowerRight": "Do not Lower Right.",
        "RaiseLeft": "Raise Left.",
        "DoNotRaiseLeft": "Do not Raise Left.",
        "LowerLeft": "Lower Left.",
        "DoNotLowerLeft": "Do not Lower Left.",
    },
}


VOICE_FILES = {
    "RaiseRight": "right_up.wav",
    "DoNotRaiseRight": "right_not_up.wav",
    "LowerRight": "right_down.wav",
    "DoNotLowerRight": "right_not_down.wav",
    "RaiseLeft": "left_up.wav",
    "DoNotRaiseLeft": "left_not_up.wav",
    "LowerLeft": "left_down.wav",
    "DoNotLowerLeft": "left_not_down.wav",
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


def display_game_over(num_correct):
    image = cv2.imread("game_over.png")

    cv2.putText(
        image,
        "Game Over !!!",
        (50, 100),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 0, 255),
        2,
        cv2.LINE_AA,
    )
    cv2.putText(
        image,
        f"Your Score is {num_correct}.",
        (50, 300),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 0, 255),
        2,
        cv2.LINE_AA,
    )
    cv2.imshow("Game Over", image)
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
    instruction_duration = 3

    num_correct = 0
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            logger.info("Ignoring empty camera frame.")
            continue

        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
        image.flags.writeable = False

        result = hands.process(image)
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        if (
            current_instruction is None
            or time.time() - instruction_start_time > instruction_duration
        ):
            if machine.state == "BothDown" and current_instruction is not None:
                if result.multi_handedness is None:
                    num_correct += 1
                else:
                    break
            elif machine.state == "BothUp":
                if (
                    result.multi_handedness is not None
                    and len(result.multi_handedness) == 2
                ):
                    num_correct += 1
                else:
                    break
            elif machine.state == "OnlyRaiseRight":
                # TODO: ここ汚い
                hand_type = (
                    result.multi_handedness[0].classification[0].label
                    if result.multi_handedness is not None
                    else None
                )
                if hand_type == "Right":
                    num_correct += 1
                else:
                    break
            elif machine.state == "OnlyRaiseLeft":
                hand_type = (
                    result.multi_handedness[0].classification[0].label
                    if result.multi_handedness is not None
                    else None
                )
                if hand_type == "Left":
                    num_correct += 1
                else:
                    break

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
        # TODO: 日本語対応
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

        cv2.imshow("Raise Hand Game", image)

        if cv2.waitKey(5) & 0xFF == 27:
            break

    hands.close()
    cap.release()
    cv2.destroyAllWindows()

    while True:
        display_game_over(num_correct)
        if cv2.waitKey(5) & 0xFF == 27:
            break
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
