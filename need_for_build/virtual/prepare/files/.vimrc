set nocompatible
source $VIMRUNTIME/vimrc_example.vim
" source $VIMRUNTIME/mswin.vim
behave mswin

set nocompatible              " be iMproved, required
filetype off                  " required

" set the runtime path to include Vundle and initialize
set rtp+=~/.vim/bundle/Vundle.vim
call vundle#begin()
" alternatively, pass a path where Vundle should install plugins
"call vundle#begin('~/some/path/here')

" let Vundle manage Vundle, required
Plugin 'gmarik/Vundle.vim'

Plugin 'vim-misc'
Plugin 'bufexplorer.zip'
Plugin 'bufferlist.vim'
Plugin 'netrw.vim'
Plugin 'scrooloose/nerdtree'
Plugin 'MarcWeber/vim-addon-mw-utils'
Plugin 'tomtom/tlib_vim'
Plugin 'SuperTab'
Plugin 'Tagbar'
Plugin 'tComment'
Plugin 'Vimball'
" Plugin 'klen/python-mode'
" Plugin 'mitsuhiko/vim-python-combined'
Plugin 'matze/vim-move'
Plugin 'terryma/vim-multiple-cursors'
Plugin 'xolox/vim-session'
Plugin 'vim-signature'
Plugin 'tabman.vim'
Plugin 'honza/vim-snippets'
Plugin 'SirVer/ultisnips'
Plugin 'hlissner/vim-multiedit'
Plugin 'airblade/vim-gitgutter'
Plugin 'tomasr/molokai'
Plugin 'motemen/git-vim'
Plugin 'fatih/vim-go'
Plugin 'rust-lang/rust.vim'
Plugin 'cespare/vim-toml'
Plugin 'timonv/vim-cargo'
Plugin 'hdima/python-syntax'
Plugin 'scrooloose/syntastic'
" Plugin 'jiangmiao/auto-pairs'
" Plugin 'tpope/vim-fugitive'
" Plugin 'chrisbra/changesPlugin'


" All of your Plugins must be added before the following line
call vundle#end()            " required
filetype plugin indent on    " required

set diffexpr=MyDiff()
function MyDiff()
	let opt = '-a --binary '
	if &diffopt =~ 'icase' | let opt = opt . '-i ' | endif
	if &diffopt =~ 'iwhite' | let opt = opt . '-b ' | endif
	let arg1 = v:fname_in
	if arg1 =~ ' ' | let arg1 = '"' . arg1 . '"' | endif
	let arg2 = v:fname_new
	if arg2 =~ ' ' | let arg2 = '"' . arg2 . '"' | endif
	let arg3 = v:fname_out
	if arg3 =~ ' ' | let arg3 = '"' . arg3 . '"' | endif
	let eq = ''
	if $VIMRUNTIME =~ ' '
		if &sh =~ '\<cmd'
			let cmd = '""' . $VIMRUNTIME . '\diff"'
			let eq = '"'
		else
			let cmd = substitute($VIMRUNTIME, ' ', '" ', '') . '\diff"'
		endif
	else
		let cmd = $VIMRUNTIME . '\diff'
	endif
	silent execute '!' . cmd . ' ' . opt . arg1 . ' ' . arg2 . ' > ' . arg3 . eq
endfunction

" Меню выбора кодировки текста (utf8, cp1251, koi8-r, cp866)
menu Encoding.utf-8 :e ++enc=utf8 <CR>
menu Encoding.windows-1251 :e ++enc=cp1251<CR>
menu Encoding.koi8-r :e ++enc=koi8-r<CR>
menu Encoding.cp866 :e ++enc=cp866<CR>

" Список используемых кодировок для автоматического их определения
set fileencodings=utf-8,cp1251,utf-16

set iskeyword=@,a-z,A-Z,48-57,_,128-175,192-255

" Включаем нумерацию строк
set nu

" Включаем фолдинг (сворачивание участков кода)
set foldenable

" Сворачивание по синтаксису
set fdm=syntax

:let fortran_fold=1

" Автоматическое открытие сверток при заходе в них
set foldopen=all

" Разворачиваем все свертки
normal zn

" Поиск по набору текста (очень полезная функция)
set incsearch

" Не выгружать буфер, когда переключаемся на другой
" Это позволяет редактировать несколько файлов в один и тот же момент без необходимости сохранения каждый раз
" когда переключаешься между ними
set hidden

" Поддержка мыши
set mouse=a
set mousemodel=popup

" Кодировка текста по умолчанию
set termencoding=utf-8
set encoding=utf-8

" Включить автоотступы
set autoindent

" Влючить подстветку синтаксиса
syntax on

" Размер отступов
set shiftwidth=4

" Размеры табуляций
set tabstop=4
set softtabstop=4

" Более "умные" отступы при вставке их с помощью tab. 
" На самом деле заметить влияние этой опции тяжело, но хуже из-за нее не будет :)
set smarttab
set smartindent

"Автоматическое переключение рабочей папки
set autochdir

" Отключить создание файлов бекапа и свапа
set nobackup
set nowritebackup
set noswapfile

" При создании нового файла *.py и *.pyw будут сразу написаны два заголовка с
" путем до интерпретатора python и с указанием кодировки utf-8
function! BufNewFile_PY()
	0put = '#!/usr/bin/env python'
	1put = '#-*- coding: utf-8 -*-'
	$put = ''
	$put = ''
	normal G
endfunction

autocmd BufNewFile *.py call BufNewFile_PY()
autocmd BufNewFile *.pyw call BufNewFile_PY()

" Автоматическое закрытие скобок
" imap [ []<LEFT>
" imap ( ()<LEFT>
" imap { {}<LEFT>
inoremap <a-9> (

" размеры окна
set lines=100
set columns=143

let g:molokai_original = 1
" color my
color molokai

" Ctrl-пробел для автодополнения
" inoremap <C-space> <C-x><C-o>

" let Tlist_Ctags_Cmd='"C:\Program Files\Ctags\ctags.exe"'

nmap <C-t> :TagbarToggle<cr>
imap <C-t> <esc>:TagbarToggle<cr>i<right>

" Переключение языка проверки орфографии
if version >= 700
"   По умолчанию проверка орфографии выключена.
    setlocal spell spelllang=
    setlocal nospell
    function ChangeSpellLang()
        if &spelllang =~ "en_us"
            setlocal spell spelllang=ru
            echo "spelllang: ru"
        elseif &spelllang =~ "ru"
            setlocal spell spelllang=
            setlocal nospell
            echo "spelllang: off"
        else
            setlocal spell spelllang=en_us
            echo "spelllang: en"
        endif
    endfunc

    " map spell on/off for English/Russian
    map <F7> <Esc>:call ChangeSpellLang()<CR>
endif

" Игнорировать регистр букв при поиске
set ignorecase

" При поиске помечать все найденные строки
set hlsearch

" Чтобы не переносить строки в середине слов
set linebreak

" Выделять строку, на которой стоит курсор
set cursorline

" Включить подсветку невидимых символов
setlocal list
" Настройка подсветки невидимых символов
setlocal listchars=tab:\|\ ,trail:·

au BufRead,BufNewFile *.mod set filetype=vb

set virtualedit="block"

au BufRead *.session so %

set keymap=russian-jcukenwin
set iminsert=0
set imsearch=0
highlight lCursor guifg=NONE guibg=Cyan


map <silent> <F3> :call BufferList()<CR>
let g:showmarks_enable=0

filetype plugin on

" backspace in Visual mode deletes selection
vnoremap <BS> d

" CTRL-X and SHIFT-Del are Cut
vnoremap <C-X> "+x
vnoremap <S-Del> "+x

" CTRL-C and CTRL-Insert are Copy
vnoremap <C-C> "+y
vnoremap <C-Insert> "+y

" CTRL-V and SHIFT-Insert are Paste
map <C-V>	"+gP
map <S-Insert>	"+gP

cmap <C-V> <C-R>+
cmap <S-Insert> <C-R>+

" Pasting blockwise and linewise selections is not possible in Insert and
" Visual mode without the +virtualedit feature.  They are pasted as if they
" were characterwise instead.
" Uses the paste.vim autoload script.

exe 'inoremap <script> <C-V>' paste#paste_cmd['i']
exe 'vnoremap <script> <C-V>' paste#paste_cmd['v']

imap <S-Insert> <C-V>
vmap <S-Insert> <C-V>

" Use CTRL-Q to do what CTRL-V used to do
noremap <C-Q> <C-V>

" Use CTRL-S for saving, also in Insert mode
noremap <C-S>	:update<CR>
vnoremap <C-S>	<C-C>:update<CR>
inoremap <C-S>	<C-O>:update<CR>

" function! TabWrapperRope()
"   if strpart(getline('.'), 0, col('.')-1) =~ '^\s*$'
"     return "\<Tab>"
"   else
"     return "\<C-R>=RopeCodeAssistInsertMode()\<CR>"
"   endif
" endfunction
"
" imap <Tab> <C-R>=TabWrapperRope()<CR>
map <C-n> :bn<CR>
map <C-S-n> :bp<CR>
" let g:calendar_monday = 1

nmap <Home> ^
imap <Home> <Esc>^i

abbr sefl self
abbr slef self
abbr sefl. self.
abbr slef. self.
abbr sefl) self)
abbr slef) self)

nmap <C-W><C-T> :NERDTreeToggle<CR>

" Отключим автоматический перенос слов
set tw=0

nmap <C-Tab> gt
map <C-Tab> <Esc>gt
imap <C-Tab> <Esc>gt
nmap <C-S-Tab> gT
map <C-S-Tab> <Esc>gT
imap <C-S-Tab> <Esc>gT

imap <A-u> u""<LEFT>

let g:pymode_rope = 1
let g:pymode_rope_completion = 1
let g:pymode_rope_complete_on_dot = 1

" документация
let g:pymode_doc = 0
let g:pymode_doc_key = 'K'
" проверка кода
let g:pymode_lint = 1
let g:pymode_lint_checker = "pyflakes,pep8, pep257"
let g:pymode_lint_ignore="E501,W601,C0110,E211,E303,E251"
" провека кода после сохранения
let g:pymode_lint_on_write = 1
let g:pymode_lint_unmodified = 1

" поддержка virtualenv
let g:pymode_virtualenv = 1

" установка breakpoints
let g:pymode_breakpoint = 1
let g:pymode_breakpoint_key = '<leader>b'

" подстветка синтаксиса
let g:pymode_syntax = 1
let g:pymode_syntax_all = 1

" отключить autofold по коду
let g:pymode_folding = 0

" возможность запускать код
let g:pymode_run = 1

let g:pymode_trim_whitespaces = 0

let NERDTreeIgnore=['\.pyc$', '\.git$', '__pycache__']
let NERDTreeQuitOnOpen=1

let g:pymode_options_max_line_length = 80

set guitablabel=%m\ %t
set textwidth=0
set wrap
setlocal wrap
set undodir=~/.vim/tmp//
set backupdir=~/.vim/tmp//

let g:move_key_modifier = 'C'
vmap <C-Down> <Plug>MoveBlockDown
vmap <C-Up> <Plug>MoveBlockUp
nmap <C-Down> <Plug>MoveLineDown
nmap <C-Up> <Plug>MoveLineUp

let g:session_autosave = 'yes'
let g:session_default_to_last = 1
let g:session_autoload = 'yes'

hi SignColumn guibg=#000000

nmap <S-Esc> :noh<cr>

set completeopt=menu,menuone

let g:UltiSnipsExpandTrigger="<s-tab>"
let g:UltiSnipsJumpForwardTrigger="<s-tab>"
let g:UltiSnipsJumpBackwardTrigger="<c-z>"

" ChangesPlugin
let g:changes_vcs_check = 1
let g:changes_sign_text_utf8 = 0
let g:changes_vcs_system='git'
let g:changes_fast=0

let g:gitgutter_sign_added = '➕'
let g:gitgutter_sign_modified = '✔'
let g:gitgutter_sign_removed = '➖'
let g:gitgutter_sign_removed_first_line = '^'
let g:gitgutter_sign_modified_removed = '~_'

" Git
let g:git_no_map_default = 1
nnoremap <Leader>gd :GitDiff<Enter>
nnoremap <Leader>gs :GitStatus<Enter>
nnoremap <Leader>gl :GitLog<Enter>
nnoremap <Leader>ga :GitAdd<Enter>:GitStatus<Enter>
nnoremap <Leader>gc :GitCommit -a<Enter>
nnoremap <Leader>gp :GitPush<Enter>
nnoremap <Leader>gb :GitBlame<Enter>

let g:rust_recommended_style=1
let g:rustfmt_autosave = 0

let python_highlight_builtins = 1
let python_highlight_exceptions = 1
let python_highlight_string_format = 1
let python_highlight_string_templates = 1
let python_highlight_indent_errors = 1
let python_highlight_space_errors = 1
let python_highlight_doctests = 1
let b:python_version_2 = 1

set statusline+=%#warningmsg#
set statusline+=%{SyntasticStatuslineFlag()}
set statusline+=%*

let g:syntastic_always_populate_loc_list = 1
let g:syntastic_auto_loc_list = 1
let g:syntastic_check_on_open = 1
let g:syntastic_check_on_wq = 0

let g:syntastic_quiet_messages = {
        \ "regex":   ['\m\[E211\]', '\m\[E303\]']}

nmap <leader>b Ofrom pudb import set_trace; set_trace()

set sessionoptions-=blank
set colorcolumn=80
" let g:syntastic_python_checkers = ["flake8", "pep8", "pyflakes", "pylama"]
let g:syntastic_python_checkers = ["pylama"]

let g:syntastic_python_pylama_post_args = "-o ~/pylama.ini"
