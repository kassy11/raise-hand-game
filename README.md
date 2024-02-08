# raise-hand-game
OpenCVとMediaPipeを使った旗揚げ（手上げ）ゲーム

## 概要
- OpenCVでカメラキャプチャ
- MediaPipeで手検出（右 or 左）
- 指示の声はVOICEVOXで生成（ずんだもん）
- 以下のようなステートマシンを作成し正解状態を判定
![image](./assets/state_machine.png)

## デモ

## ToDo
- 日英対応