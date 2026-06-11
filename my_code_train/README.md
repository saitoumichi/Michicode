# my_code_train

このリポジトリは、VoxelMorph 系の3D医用画像位置合わせモデルを手元環境で動かすための最小検証用コード群です。

## 目的

- `debug_registration_local.py`  : 形状やエラー箇所の調査用
- `local_vxm_test.py`         : 本番に近い流れでモデル生成→warpまでテスト
- `test_jupyter_local.py`     : Jupyter向け最小検証（ダミー入力でforward確認）

## 動作環境

- Python 3.8+
- PyTorch (cuda/ cpu)
- `vxm_torch` など、手元の研究コード（`C:\Users\ri0151fv\Yamacode` に存在）

## 使い方

1. 必要に応じて仮想環境を作成・有効化

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt   # あれば
```

2. `test_jupyter_local.py` を実行（最小動作確認）

```powershell
python test_jupyter_local.py
```

3. `local_vxm_test.py` でも同様に動作確認

```powershell
python local_vxm_test.py
```

4. `debug_registration_local.py` はエラー調査・shape確認用途

```powershell
python debug_registration_local.py
```

## 注意点

- いずれのスクリプトも学習済み重みや実データを含みません。まずは最小構成で forward が通ることを確認することが目的です。
- `vxm_torch` のパスが通っていない場合、`sys.path.append` で手動追加してください。

## 今後追加するなら

- 依存関係を `requirements.txt` に明記
- VoxelMorph モデルの学習用 /評価用スクリプト
- 実データ読み込みパイプライン
- READMEに結果キャプチャ・コマンド例
