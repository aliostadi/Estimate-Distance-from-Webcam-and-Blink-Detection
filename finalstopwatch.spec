# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['finalstopwatch.py'],
    pathex=[],
    binaries=[],
    datas=[("C:\\Users\\msi\\PycharmProjects\\bina_fina_stopwatch\\venv\\Lib\\site-packages\\mediapipe\\modules","mediapipe\\modules"),
    ("C:\\Users\\msi\\PycharmProjects\\bina_fina_stopwatch\\venv\\Lib\\site-packages\\cvzone","site-packages\\cvzone")],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='finalstopwatch',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
