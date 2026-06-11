# Michicode

このリポジトリは、個人学習用のコード収集と実験用スクリプトをまとめたものです。

## 📁 ディレクトリ構成

- `code_in_school/`
  - 学校や講義で使うコード例や練習問題。`jupyter.py`などを含む。
- `my_code_train/`
  - 自身のコーディングトレーニング用プロジェクト。
  - `debug_registration_local.py`
  - `local_vxm_test.py`
  - `test_jupyter_local.py`

## 🚀 使い方

1. このリポジトリをクローン

   ```powershell
   git clone <リポジトリURL>
   cd Michicode
   ```

2. Pythonスクリプトを実行

   ```powershell
   python code_in_school/jupyter.py
   python my_code_train/local_vxm_test.py
   ```

3. Jupyterを使って対話形式で確認したい場合

   ```powershell
   python -m notebook
   ```

## 🛠️ 依存関係

このリポジトリには明示的な`requirements.txt`がありません。各スクリプトに必要な外部ライブラリがあれば、実行前に`pip install`で追加してください。

## ✨ 提案

- `requirements.txt`を追加し、依存パッケージを固定すると再現性が高まります。
- 各フォルダに`README.md`を置き、目的と実行手順を明示しておくと便利です。

## 📬 連絡

このリポジトリは個人用途向けのメモリポジトリです。修正や機能追加は自由に行ってください。
