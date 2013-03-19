# -*- mode: python -*-
a = Analysis(['tcxgen.py'],
             pathex=['/home/mcattin/Documents/endomondo'],
             hiddenimports=[],
             hookspath=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name=os.path.join('dist', 'tcxgen'),
          debug=True,
          strip=None,
          upx=True,
          console=True )
