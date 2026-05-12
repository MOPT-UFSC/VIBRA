# -*- mode: python ; coding: utf-8 -*-

import platform
import sys

from PyInstaller.utils.hooks import collect_all, collect_data_files, copy_metadata

os = platform.system()

if os == "Windows":
    current_system_binaries = [(f"{sys.prefix}/Library/bin/*.dll", "./Library/bin/")]
elif os == "Linux":
    current_system_binaries = [(f"{sys.prefix}/lib/*.so*", "./lib/")]
else:
    current_system_binaries = []


datas = [
    ("vibra/interface/data/", "vibra/interface/data/"),
]
datas += collect_data_files("molde")
datas += copy_metadata("cad-widgets")
datas += copy_metadata('imageio')

hidden_imports = ["vtk", "cadquery-ocp-novtk", "cadquery-ocp-stubs"]

datas_ocp, binaries_ocp, hidden_ocp = collect_all("OCP")
current_system_binaries += binaries_ocp
datas += datas_ocp
hidden_imports += hidden_ocp

a = Analysis(
    ["vibra/launch.py"],
    pathex=[],
    binaries=current_system_binaries,
    datas=datas,
    hiddenimports=hidden_imports,
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
    [],
    exclude_binaries=True,
    name="vibra.exe",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=["vibra.ico"],
)


coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name="Vibra",
)
