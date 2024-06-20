# -*- mode: python ; coding: utf-8 -*-

import sys
import platform

os = platform.system()

if os == "Windows":
    current_system_binaries = [
        (f"{sys.prefix}/Library/bin/mkl_rt.2.dll", "./Library/bin/")
    ]
elif os == "Linux":
    current_system_binaries = [
        (f"{sys.prefix}/lib/libmkl_rt.so.2", "./lib/")
    ]
else:
    current_system_binaries = []


a = Analysis(
    ['vibra/launch.py'],
    pathex=[],
    binaries=current_system_binaries,
    datas=[
        ("vibra/interface/data/", "vibra/interface/data/")
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='Vibra',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
