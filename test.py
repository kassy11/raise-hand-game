import cv2

# カメラのキャプチャを開始
cap = cv2.VideoCapture(0)

# カメラが開かれているか確認
if not cap.isOpened():
    print("カメラが開けません")
    exit()

# ループ開始
while True:
    # フレームをキャプチャ
    ret, frame = cap.read()
    if not ret:
        print("フレームを取得できませんでした")
        break

    # フレームの高さと幅を取得
    height, width = frame.shape[:2]

    # フレームの中心を計算
    center = (width // 2, height // 2)

    # フレーム上にマル（円）を線で描画
    cv2.circle(frame, center, 50, (0, 255, 0), thickness=3)  # 緑色の円（線で描画）

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

    # 結果を表示
    cv2.imshow("Frame", frame)

    # Escキーでループから抜ける
    if cv2.waitKey(1) & 0xFF == 27:
        break

# キャプチャを解放し、ウィンドウを閉じる
cap.release()
cv2.destroyAllWindows()
