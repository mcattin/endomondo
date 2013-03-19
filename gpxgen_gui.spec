# -*- mode: python -*-
a = Analysis(['gpxgen_gui.py'],
             pathex=['/home/mcattin/Documents/endomondo'],
             hiddenimports=[],
             hookspath=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name=os.path.join('dist', 'gpxgen_gui'),
          debug=True,
          strip=None,
          upx=True,
          console=True )
