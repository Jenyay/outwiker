from outwiker.gui.images import readImage

import outwiker.gui.iconmaker as _iconmaker

def createIcon(fname_in, fname_out) -> None:
    return _iconmaker.IconMaker().create(fname_in, fname_out)
