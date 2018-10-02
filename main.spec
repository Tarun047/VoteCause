# -*- mode: python -*-

block_cipher = None


a = Analysis(['main.py'],
             pathex=['/home/tarun/VoteCause'],
             binaries=[],
             datas=[('/home/tarun/VoteCause/PollCreator.ui',''),('/home/tarun/VoteCause/PollManager.ui',''),('/home/tarun/VoteCause/Stats.ui',''),('/home/tarun/VoteCause/main.ui','')],
             hiddenimports=['PyQt5.sip'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='main',
          debug=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=True )
