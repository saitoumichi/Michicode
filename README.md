# Michicode

![Research](https://img.shields.io/badge/Research-Wavelet%20VoxelMorph-blue)
![Framework](https://img.shields.io/badge/Framework-PyTorch-red)
![Status](https://img.shields.io/badge/Status-Under%20Development-orange)

## 研究進捗サマリー

| 項目 | 状態 |
|------|------|
| Haar Wavelet実装 | ✅ |
| 3D Wavelet実装 | ✅ |
| 完全再構成確認 | ✅ |
| DWT実装 | ✅ |
| VoxelMorph動作確認 | ✅ |
| DWT学習実験 | ⏳ |
| SWT比較実験 | ⏳ |
| 101症例評価 | ⏳ |
| 卒業論文執筆 | ⏳ |

## 目次

- 概要
- 研究背景
- ディレクトリ構成
- 研究目的
- 研究の新規性
- Wavelet成分
- 先行研究と提案手法
- 完全再構成条件
- 実験結果
- 実験環境
- ネットワーク設定
- 損失関数
- 現在の進捗
- 現在の課題
- 今後の方針
- 実験ログ
- 更新履歴
- Git運用
- 参考文献

---

## 概要

本リポジトリは、卒業研究で取り組んでいる医用画像レジストレーションに関するコードを管理するためのリポジトリです。

研究テーマは、胸部CT画像を対象とした非剛体レジストレーションであり、VoxelMorphをベースとした深層学習モデルにWavelet変換を組み合わせることで、より高精度な位置合わせを実現することを目的としています。

現在は、先行研究で提案されたWavelet-VoxelMorphの実装を解析し、自身の実装との違いを比較しながら、完全再構成（Perfect Reconstruction : PR）が成立するWavelet変換の導入方法を検証しています。

また、本リポジトリは単なるコード保管場所ではなく、先行研究との比較、変更履歴、実験結果、発生した問題点を整理する研究ログとしても利用しています。

---

## 研究背景

### 研究全体のイメージ図

以下に研究全体の流れを示す図を追加予定である。

```markdown
![Research Flow](images/research_flow.png)
```

※ `images/research_flow.png` に研究全体のフローチャートを配置する予定。

---

医用画像レジストレーションは、異なる時期に撮影された画像や異なる患者画像を空間的に対応付ける技術です。

胸部CT画像では、呼吸状態や撮影条件の違いによって肺の形状が大きく変化するため、単純な位置合わせでは十分な精度を得ることができません。そのため、画像全体を柔軟に変形させる非剛体レジストレーションが必要となります。

近年では深層学習を利用したレジストレーション手法としてVoxelMorphが広く利用されています。VoxelMorphはMoving画像とFixed画像を入力として変形ベクトル場（DVF : Deformation Vector Field）を推定し、そのDVFを用いてMoving画像を変形することで画像位置合わせを実現します。

先行研究では、VoxelMorphにWavelet変換を導入し、低周波成分と高周波成分を分離して特徴抽出を行うことでレジストレーション性能の向上を図っています。しかし、実装を調査した結果、Wavelet変換とダウンサンプリングの処理順序が理論的な完全再構成条件と一致していない可能性が確認されました。

そこで本研究では、Analysisフィルタによる周波数分解、Downsampling、Upsampling、Synthesisフィルタによる再構成というWavelet理論に基づく処理順序へ修正し、その影響を評価しています。

---

### 本研究で扱う処理の流れ

```text
Moving CT        Fixed CT
     │              │
     └──────┬───────┘
            ↓
      Wavelet Analysis
            ↓
     周波数成分へ分解
            ↓
         Encoder
            ↓
       Bottleneck
            ↓
         Decoder
            ↓
      DVF Prediction
            ↓
  Spatial Transformer
            ↓
     Registered Image
```

### Wavelet変換の目的

Wavelet変換を利用することで、画像を低周波成分と高周波成分へ分解することができる。

- 低周波成分 : 臓器全体の形状情報
- 高周波成分 : 輪郭や境界などの詳細情報

本研究では、これらを分離して学習させることで特徴抽出能力の向上を目指している。

## ディレクトリ構成

```
Michicode/
├── code_in_school/
│   └── jupyter.py
│
├── my_code_train/
│   ├── debug_registration_local.py
│   ├── local_vxm_test.py
│   └── test_jupyter_local.py
│
├── vxm_torch/
│   ├── __init__.py
│   ├── layers.py
│   ├── losses.py
│   ├── modelio.py
│   ├── networks.py
│   └── utils.py
│
└── torch_local_backup/
    ├── __init__.py
    ├── layers.py
    ├── losses.py
    ├── modelio.py
    ├── networks.py
    └── utils.py
```

---

## フォルダ説明

### code_in_school/

大学の授業や演習で使用したコードを格納しています。主に基礎的な実験やノートブック形式の資料が含まれます。

### my_code_train/

研究用の実験コードや検証用スクリプトを管理しています。VoxelMorphの動作確認、Wavelet変換の検証、デバッグ用スクリプトなどが含まれます。

- `debug_registration_local.py`: レジストレーション処理のデバッグ用。
- `local_vxm_test.py`: VoxelMorphの学習済みモデルを用いた推論・評価。
- `test_jupyter_local.py`: ローカル環境での試験的コード実行。

### vxm_torch/

現在研究で使用しているVoxelMorphのPyTorch実装です。

主な役割:
- ネットワーク構造の定義
- DVF生成
- Spatial Transformerによる画像変形
- 損失関数計算
- 学習および推論処理

主要ファイル:
- networks.py : U-NetおよびVoxelMorph本体
- layers.py : Spatial Transformerなどのレイヤ実装
- losses.py : MSE、NCC、LNCC、Gradient Loss
- modelio.py : モデル保存・読込
- utils.py : 補助関数群

### torch_local_backup/

先行研究で使用されていたコードおよび修正前のバックアップを保存しています。

主な用途:
- 先行研究との比較
- 修正前後の差分確認
- 問題発生時の復元
- 処理順序の確認
- 実験結果の再現

---

## 研究目的

1. **先行研究の理解と再現**  
   既存のVoxelMorphベースのレジストレーションコードの構造と動作を理解し、問題点や改善点を明確にする。

2. **Wavelet変換の導入と検証**  
   Haar Waveletを中心に、3次元画像への適用方法を検討し、Analysisフィルタ・Synthesisフィルタの設計と完全再構成条件の成立を評価する。

3. **完全再構成の評価**  
   再構成誤差を定量的に測定し、理論的なPerfect Reconstructionが実際の実装で成立しているかを確認する。

4. **レジストレーション性能の向上**  
   Wavelet変換を組み込んだネットワーク構造の効果をRMSE、MS-SSIM、Dice係数などの指標で評価し、性能向上を目指す。

5. **研究記録の体系的管理**  
   実験結果、エラー解析、コード変更履歴を一元管理し、研究の継続的発展を支援する。

---


## 研究の新規性

先行研究では、画像をダウンサンプリングした後にWavelet変換を適用していた。

```text
Input
↓
Downsample
↓
Wavelet
```

本研究では、Wavelet理論に基づきAnalysis Filterを先に適用し、その後にダウンサンプリングを行う構成を検証している。

```text
Input
↓
Analysis Filter
↓
Downsample
```

主な変更点

- Wavelet処理順序の見直し
- 3次元Haar Waveletの実装
- 完全再構成誤差の定量評価
- DWTとSWTの比較検証
- Wavelet理論との整合性確認

## 比較対象

本リポジトリでは、以下の観点から先行研究コードと自身の改良コードを比較・分析しています。

- 入力画像サイズ（128×256×256、256×256×256）
- Wavelet変換の有無および種類（DWT、SWT）
- ダウンサンプリングとアップサンプリングのタイミング
- Analysis→Downsample→Upsample→Synthesis の処理順序の違い
- エンコーダおよびデコーダへの入力形式の違い
- DVF（変形ベクトル場）生成方法の差異
- 完全再構成条件の成立状況
- 損失関数の構成および重み付け
- 評価指標の違いと結果の比較
- 学習時間およびGPUリソースの使用状況


---

## Wavelet成分

3次元Haar Wavelet変換では、入力画像を8個の周波数成分へ分解する。

| 成分 | 内容 |
|--------|--------|
| LLL | 低周波成分（形状情報） |
| LLH | 一部高周波成分 |
| LHL | 一部高周波成分 |
| LHH | 高周波成分 |
| HLL | 高周波成分 |
| HLH | 高周波成分 |
| HHL | 高周波成分 |
| HHH | 最も高い周波数成分 |

LLLは肺全体の形状や大まかな構造を保持し、HHHは輪郭や微細な変化を保持する。

本研究では、これらの周波数成分を利用して特徴抽出を行う。

### 3次元Haar Waveletの構造

```text
入力画像
    ↓
2×2×2ブロック
    ↓
8成分へ分解

LLL  LLH
LHL  LHH
HLL  HLH
HHL  HHH
```

各成分は異なる周波数情報を保持しており、LLLは全体構造、HHHは微細構造を表現する。

### Wavelet分解図

以下に3次元Haar Wavelet分解の模式図を追加予定である。

```markdown
![Wavelet Decomposition](images/wavelet_decomposition.png)
```

※ `images/wavelet_decomposition.png` にLLL〜HHHの8成分を示す図を配置する予定。

## 先行研究と提案手法

### ネットワーク構造図

以下にVoxelMorphおよびWavelet-VoxelMorphのネットワーク構造図を追加予定である。

```markdown
![Network Architecture](images/network_architecture.png)
```

※ `images/network_architecture.png` にネットワーク構造図を配置する予定。

### 先行研究の処理順序

```text
入力画像
↓
Downsample
↓
Wavelet変換
↓
Encoder
↓
Decoder
↓
Wavelet加算
↓
Upsample
```

### 本研究で検証している処理順序

```text
入力画像
↓
Analysis Filter
↓
Downsample
↓
Encoder
↓
Decoder
↓
Upsample
↓
Synthesis Filter
```

本研究では、Wavelet理論に基づいた処理順序へ修正することで完全再構成条件との整合性を向上させることを目的としている。

---

## 完全再構成条件

本研究ではWavelet変換における完全再構成（Perfect Reconstruction）条件を確認している。

確認対象:

1. エイリアシングキャンセル条件
2. 振幅歪み補償条件
3. AnalysisフィルタとSynthesisフィルタの整合性

これらの条件を満たすことで、理論上は入力画像を完全に再構成することができる。

---

## DWTとSWTの比較

| 項目 | DWT | SWT |
|--------|--------|--------|
| ダウンサンプリング | ○ | × |
| アップサンプリング | ○ | × |
| 完全再構成 | ○ | ○ |
| 計算量 | 小 | 大 |
| メモリ使用量 | 小 | 大 |
| 平行移動不変性 | × | ○ |

本研究ではDWTとSWTの両方について比較実験を行う予定である。

---

## 実験結果

### 完全再構成誤差グラフ

以下に完全再構成誤差の比較グラフを追加予定である。

```markdown
![Reconstruction Error](images/reconstruction_error.png)
```

※ `images/reconstruction_error.png` に画像サイズごとの再構成誤差を示すグラフを配置する予定。

### 完全再構成誤差

128×256×256 CT画像

- Mean Error : 1.37e-08
- Max Error : 2.38e-07

256×256×256 CT画像

- Mean Error : 5.37e-08
- Max Error : 9.54e-07


上記結果より、実装したHaar Wavelet変換および逆変換において、ほぼ完全再構成が達成できていることを確認した。

### 完全再構成の確認状況

完全再構成条件の確認として、以下を検証している。

- AnalysisフィルタとSynthesisフィルタの整合性
- エイリアシングキャンセル条件
- 振幅歪みの有無
- 入力画像と再構成画像の誤差測定

現在の結果では、誤差は10^-7オーダーであり、実用上ほぼ完全再構成が成立していると考えられる。

---

## 先行研究結果

先行研究（Wavelet-VoxelMorph）の評価結果

| 評価指標 | 結果 |
|----------|----------|
| RMSE | 126.37 ± 82.03 HU |
| MS-SSIM | 0.990 |
| Dice | 0.974 |
| Folding Rate | 9.12 % |

---

## 現在の結果

現在確認できている評価結果

### pair101

| 評価指標 | 結果 |
|----------|----------|
| RMSE | 151.218 |
| MS-SSIM | 0.9671 |
| Dice | 0.9605 |


※ 現時点では1ペアによる評価結果であり、今後101症例全体で評価を行う予定である。

### 学習Loss推移グラフ

以下に学習時のLoss推移グラフを追加予定である。

```markdown
![Loss Curve](images/loss_curve.png)
```

※ `images/loss_curve.png` に学習エポックごとのLoss推移を示すグラフを配置する予定。

---

## 結果比較

| 評価指標 | 先行研究 | 現在 |
|----------|----------|----------|
| RMSE | 126.37 | 151.218 |
| MS-SSIM | 0.990 | 0.9671 |
| Dice | 0.974 | 0.9605 |

現時点では単一ペア評価のため単純比較はできないが、今後101症例全体で評価を行い比較する予定である。

---

## 実験環境

本研究の実験はローカルGPU環境で実施している。

### ハードウェア

- GPU : NVIDIA GeForce RTX 3060 Ti
- VRAM : 8GB
- CPU : Local PC Environment

### ソフトウェア

- Python 3.10
- PyTorch
- NumPy
- Matplotlib
- Jupyter Notebook

### データセット

- 胸部CT画像 : 501症例
- 学習用データ : 400症例
- 評価用データ : 101症例
- スキャナ : GE Discovery CT750 HD
- 前処理 : ベッド除去済み胸部CT

### 入力画像サイズ

- 128×256×256
- 256×256×256

---

## ネットワーク設定

### VoxelMorph

Encoder Features

```text
[32, 64, 64, 64, 64]
```

Decoder Features

```text
[64, 64, 64, 64, 64, 32, 16, 16]
```

Output

```text
DVF (3 Channels)
```

### モデル概要

本研究ではVoxelMorphをベースとしたEncoder-Decoder構造を利用する。

処理の流れ

```text
Moving Image
      +
Fixed Image
      ↓
    Encoder
      ↓
   Bottleneck
      ↓
    Decoder
      ↓
      DVF
      ↓
Spatial Transformer
      ↓
Registered Image
```

出力されるDVFは3チャネル（x, y, z方向）で構成される。

### 入力サイズ

- 128×256×256
- 256×256×256

---

## 評価指標

本研究では以下の評価指標を使用している。

### RMSE

画像間の画素値誤差を評価する指標。

### MS-SSIM

構造的類似度を評価する指標。

### Dice係数

肺領域の重なり具合を評価する指標。

### Folding Rate

DVFの物理的妥当性を評価する指標。

---

## 損失関数

本研究では画像類似度と変形場の滑らかさを考慮した損失関数を使用する。

### Pre-training

```text
L = αLsim + βLdef
```

```text
α = 100
β = 0.01
```

### 類似度損失

- MSE
- NCC
- LNCC

### 正則化項

- Gradient Loss

目的:

- レジストレーション精度向上
- Folding抑制
- 滑らかなDVF生成

## 再現方法

### 学習

```bash
python train.py
```

### 評価

```bash
python evaluate.py
```

### 動作確認

```bash
python my_code_train/local_vxm_test.py
```

※ 実際の実験コードに応じて実行ファイル名は変更される場合がある。

---

## 現在の進捗

### Wavelet実装

- [x] Haar Wavelet実装
- [x] 3次元Wavelet実装
- [x] 逆変換実装
- [x] 完全再構成確認
- [x] Haar Analysis Filter実装
- [x] Haar Synthesis Filter実装
- [x] 完全再構成誤差測定

### ネットワーク検証

- [x] VoxelMorph動作確認
- [x] Wavelet組込み確認
- [x] DVF出力確認
- [ ] DWT学習実験
- [ ] SWT比較実験
- [ ] 400症例学習
- [ ] 101症例評価

### 今後の検証

- [ ] 256×256×256学習
- [ ] 完全再構成条件の検証
- [ ] RMSE比較
- [ ] MS-SSIM比較
- [ ] Dice比較
- [ ] Folding比較

---

## 現在の課題

- 先行研究の処理順序とWavelet理論の不一致
- Analysis → Downsample → Upsample → Synthesis への修正
- 完全再構成条件（3条件）の数式レベルでの確認
- DWTとSWTの性能比較
- 256×256×256入力への対応
- 学習時間およびGPUメモリ消費量の増加
- Folding Rateの低減
- RMSE・MS-SSIM・Diceの改善
- 101症例による定量評価

---

## 今後の方針

- Analysis → Downsample → Upsample → Synthesis の処理順序へ修正
- 完全再構成条件（3条件）の確認
- DWTとSWTの比較実験
- 400症例による学習
- 101症例による評価
- RMSE・MS-SSIM・Diceによる定量評価
- Folding Rateの改善
- 卒業論文への反映


## 実験ログ

### 2025/05

- Haar Wavelet実装
- 逆Wavelet変換実装
- 3D Wavelet実装

### 2025/06

- 完全再構成確認
- Mean Error : 1.37e-08
- Max Error : 2.38e-07
- DWT実装
- 先行研究コード解析
- README作成

### 今後

- DWT学習
- SWT比較
- 400症例学習
- 101症例評価

---

## 更新履歴

### 2025年

#### 5月

- Haar Wavelet実装
- 3次元Wavelet実装
- 逆Wavelet変換実装
- 完全再構成確認

#### 6月

- 先行研究コード解析
- README整備
- Wavelet処理順序の検証
- 完全再構成誤差測定
- DWT実装

### 今後の予定

- DWT学習実験
- SWT比較実験
- 400症例学習
- 101症例評価
- 卒業論文執筆

---

## Git運用

### Branch

```text
main        : 安定版
experiment  : 実験用
backup      : バックアップ用
```

### Commit Rule

変更内容が分かるコミットメッセージを記録する。

例:

```text
Wavelet処理順序修正
DWT実装
完全再構成確認
README更新
```

---

## 研究メモ

### Wavelet導入の目的

- 周波数ごとの特徴抽出
- 微細構造の保持
- 肺境界の位置合わせ精度向上

### 検証中の内容

- DWTとSWTの比較
- 完全再構成条件の確認
- Wavelet処理順序の影響
- Folding抑制効果
- DVF品質の向上

### 最終目標

先行研究と同等以上の精度を達成し、Wavelet理論に基づく実装の有効性を示すこと。

---

## 参考文献

[1] Balakrishnan G, Zhao A, Sabuncu MR, Guttag J, Dalca AV.
VoxelMorph: A Learning Framework for Deformable Medical Image Registration.
IEEE Transactions on Medical Imaging, 2019.

[2] Mallat S.
A Wavelet Tour of Signal Processing.
Academic Press, 2008.

[3] Daubechies I.
Ten Lectures on Wavelets.
SIAM, 1992.

[4] Unser M.
Ten Good Reasons for Using Spline Wavelets.
Proceedings of SPIE, 1997.

[5] 先行研究で使用しているWavelet-VoxelMorph関連論文.

---

## License

本リポジトリは個人学習および研究目的で作成されています。必要に応じて自由に編集・利用してください。
