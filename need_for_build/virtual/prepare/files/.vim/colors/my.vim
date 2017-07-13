" Vim color file
" Maintainer:	David Schweikert <dws@ee.ethz.ch>
" Last Change:	2006 Apr 30

hi clear

let colors_name = "my"

" Normal should come first
hi Normal     guifg=Black  guibg=White
hi Cursor     guifg=bg     guibg=fg
hi lCursor    guifg=NONE   guibg=Cyan

" Note: we never set 'term' because the defaults for B&W terminals are OK
hi DiffAdd    ctermbg=LightBlue    guibg=LightBlue
hi DiffChange ctermbg=LightMagenta guibg=LightMagenta
hi DiffDelete ctermfg=Blue	   ctermbg=LightCyan gui=bold guifg=Blue guibg=LightCyan
hi DiffText   ctermbg=Red	   cterm=bold gui=bold guibg=Red
hi Directory  ctermfg=DarkBlue	   guifg=Blue
hi ErrorMsg   ctermfg=White	   ctermbg=DarkRed  guibg=Red	    guifg=White
hi FoldColumn ctermfg=DarkBlue	   ctermbg=Grey     guibg=Grey	    guifg=DarkBlue
hi Folded     ctermbg=Grey	   ctermfg=DarkBlue guibg=LightGrey guifg=DarkBlue
hi IncSearch  cterm=reverse	   gui=reverse
hi LineNr     ctermfg=Brown	   guifg=Brown
hi ModeMsg    cterm=bold	   gui=bold
hi MoreMsg    ctermfg=DarkGreen    gui=bold guifg=SeaGreen
hi NonText    ctermfg=Blue	   gui=bold guifg=gray guibg=white
hi Pmenu      guibg=LightBlue
hi PmenuSel   ctermfg=White	   ctermbg=DarkBlue  guifg=White  guibg=DarkBlue
hi Question   ctermfg=DarkGreen    gui=bold guifg=SeaGreen
hi Search     ctermfg=NONE	   ctermbg=Yellow guibg=Yellow guifg=NONE
hi SpecialKey ctermfg=None	   guifg=#CCCCCC

" !!!
hi StatusLine cterm=bold	   ctermbg=blue ctermfg=white guibg=gold guifg=gray
hi StatusLineNC	cterm=bold	   ctermbg=blue ctermfg=white  guibg=white guifg=gray


hi Title      ctermfg=DarkMagenta  gui=bold guifg=Magenta
hi VertSplit  cterm=reverse	   gui=reverse
hi Visual     ctermbg=NONE	   cterm=reverse gui=reverse guifg=Grey guibg=fg
hi VisualNOS  cterm=underline,bold gui=underline,bold
hi WarningMsg ctermfg=DarkRed	   guifg=Red
hi WildMenu   ctermfg=Black	   ctermbg=Yellow    guibg=Yellow guifg=Black

" syntax highlighting
hi Comment    cterm=NONE ctermfg=DarkGreen     gui=NONE guifg=#007F00
hi Constant   cterm=NONE ctermfg=DarkGreen   gui=NONE guifg=#7F007F
hi Identifier cterm=NONE ctermfg=DarkCyan    gui=NONE guifg=cyan4
hi PreProc    cterm=NONE ctermfg=DarkMagenta gui=NONE guifg=magenta3
hi Special    cterm=NONE ctermfg=LightRed    gui=NONE guifg=deeppink
hi Statement  cterm=bold ctermfg=Blue	     gui=NONE guifg=blue
hi pythonStatement  cterm=bold ctermfg=Blue	     gui=bold guifg=blue
hi Type	      cterm=NONE ctermfg=Blue	     gui=bold guifg=blue
hi pythonPreCondit	      cterm=NONE ctermfg=Blue    gui=NONE guifg=#800000
hi pythonRawString	      cterm=NONE ctermfg=Blue    gui=NONE guifg=#7F0000
hi pythonString	      cterm=NONE ctermfg=Blue    gui=NONE guifg=#7F007F

" vim: sw=2
