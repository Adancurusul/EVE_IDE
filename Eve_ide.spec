# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['Eve_ide.py', 'create_sourcefile.py', 'first_test.py', 'icons_rc.py', 'make_project.py', 'new_project.py', 'select_gcc_toolchain.py', 'select_workspace.py', 'serial_show.py', 'serial_ui.py'],
             pathex=['D:\\codes\\eve_pack\\eve_idev0.0.2'],
             binaries=[],
             datas=[],
             hiddenimports=['PyQt5.QtPrintSupport'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='Eve_ide',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False , icon='main.ico')
