" Only do this when not done yet for this buffer
if exists("b:mypython_ftplugin")
	finish
endif
let b:mypython_ftplugin = 1

set makeprg=pylint\ --reports=n\ --include-ids=y\ --output-format=parseable\ %:p
set errorformat=%f:%l:\ %m
set expandtab
