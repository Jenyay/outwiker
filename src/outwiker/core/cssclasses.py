# -*- coding=utf-8 -*-

CSS_ERROR = 'ow-error'
CSS_IMAGE = 'ow-image'
CSS_LINK = 'ow-link'
CSS_LINK_PAGE = 'ow-link-page'
CSS_ATTACH = 'ow-attach'
CSS_ATTACH_FILE = 'ow-attach-file'
CSS_ATTACH_IMAGE = 'ow-attach-image'
CSS_ATTACH_DIR = 'ow-attach-dir'
CSS_ATTACH_LIST = 'ow-attach-list'
CSS_IMAGE = 'ow-image'
CSS_QUOTE = 'ow-quote'


def getDefaultStyles() -> str:
    return '''
		img{border:none}

		/* Attachment link */
		a.ow-attach {
		  border-bottom: 1px solid transparent;
		  text-decoration: none;
		  font-style: italic;
		}

		a.ow-attach:hover {
		  border-color: #eee;
		  color: #000;
		}

		a.ow-link-page:before {
		  margin-right: 0px;
		  content: "";
		  height: 20px;
		  vertical-align: middle;
		  width: 20px;
		  background-repeat: no-repeat;
		  display: inline-block;
		  background-image: url("data:image/svg+xml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiA/PjxzdmcgaWQ9IklDT04iIHZpZXdCb3g9IjAgMCA1MTIgNTEyIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciPjxkZWZzPjxzdHlsZT4uY2xzLTF7ZmlsbDojYjBjYmUwO30uY2xzLTEsLmNscy0ye3N0cm9rZTojNjY2NjdlO3N0cm9rZS1saW5lY2FwOnJvdW5kO3N0cm9rZS1saW5lam9pbjpyb3VuZDtzdHJva2Utd2lkdGg6MTVweDt9LmNscy0ye2ZpbGw6IzVmOWNjYjt9PC9zdHlsZT48L2RlZnM+PHRpdGxlLz48cGF0aCBjbGFzcz0iY2xzLTEiIGQ9Ik0zOTEsMTU4LjV2MjY1YTI1LDI1LDAsMCwxLTI1LDI1SDE0NmEyNSwyNSwwLDAsMS0yNS0yNVY4OC41YTI1LDI1LDAsMCwxLDI1LTI1SDI5NloiLz48cGF0aCBjbGFzcz0iY2xzLTIiIGQ9Ik0zOTEsMTU4LjVIMzIxYTI1LDI1LDAsMCwxLTI1LTI1di03MFoiLz48L3N2Zz4=");
		  background-position: center 2px;
		  background-size: 75% auto;
		}

		a.ow-attach:before {
		  margin-right: 0px;
		  content: "";
		  height: 20px;
		  vertical-align: middle;
		  width: 20px;
		  background-repeat: no-repeat;
		  display: inline-block;
		  /* file icon by default */
		  background-image: url("data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSI0MDAiIGhlaWdodD0iNDAwIj48cGF0aCBmaWxsPSIjMkE5NEY0IiBkPSJNMTM1LjYyNiAzNDYuMWMtMjAuMjAxIDAtMzkuMTQ2LTcuODItNTMuMzQ3LTIyLjAyLTE0LjE5OS0xNC4yLTIyLjAyLTMzLjE0Ni0yMi4wMi01My4zNDYgMC0yMC4yMDEgNy44Mi0zOS4xNDYgMjIuMDItNTMuMzQ3TDIyOS40MTQgNzAuMjUzYzExLjI2My0xMS4yNTkgMjYuMDc2LTE3LjAyNyA0MS42ODEtMTYuMjkxIDE0Ljg4My43MTggMjkuMjYyIDcuMjk2IDQwLjQ4OSAxOC41MjNzMTcuODA3IDI1LjYwNSAxOC41MjQgNDAuNDg3Yy43NTQgMTUuNjE5LTUuMDMxIDMwLjQyMi0xNi4yOTMgNDEuNjgybC0xMzguMjE4IDEzOC4yMmMtMTQuNjY2IDE0LjY2My0zOC41MjUgMTQuNjYzLTUzLjE4OSAwLTcuMDg1LTcuMDg2LTEwLjk4Ni0xNi41My0xMC45ODYtMjYuNTk1IDAtMTAuMDY2IDMuOTAxLTE5LjUxMSAxMC45ODctMjYuNTk2bDkzLjYzMS05My42MzdjNC44MzctNC44MzYgMTIuNjgtNC44MzYgMTcuNTE4IDAgNC44MzggNC44MzggNC44MzggMTIuNjgyLjAwMiAxNy41MmwtOTMuNjMzIDkzLjYzN2MtMi40MDUgMi40MDQtMy43MyA1LjYyOC0zLjczIDkuMDc2IDAgMy40NDcgMS4zMjUgNi42NzEgMy43MyA5LjA3NiA1LjAwNSA1LjAwMyAxMy4xNDYgNS4wMDYgMTguMTUyIDBsMTM4LjIxOC0xMzguMjJjNi4zNS02LjM0OSA5LjQ4My0xNC4yOTIgOS4wNjUtMjIuOTY5LS40Mi04LjcxOC00LjQzMy0xNy4yOTktMTEuMjk2LTI0LjE2My0xNC4zMDEtMTQuMzAxLTM0LjEyMi0xNS4yMzgtNDcuMTM1LTIuMjMxTDk5Ljc5OCAyMzQuOTA3Yy05LjUyIDkuNTIxLTE0Ljc2NCAyMi4yNDUtMTQuNzY0IDM1LjgyOCAwIDEzLjU4MiA1LjI0NCAyNi4zMDcgMTQuNzY0IDM1LjgyNiA5LjUyMSA5LjUyMSAyMi4yNDUgMTQuNzY1IDM1LjgyOCAxNC43NjVzMjYuMzA3LTUuMjQ0IDM1LjgyNy0xNC43NjVsMTQ3LjE0MS0xNDcuMTRjNC44MzgtNC44MzggMTIuNjgtNC44MzkgMTcuNTE5IDAgNC44MzggNC44MzggNC44MzggMTIuNjgxIDAgMTcuNTE5TDE4OC45NzIgMzI0LjA4MWMtMTQuMiAxNC4xOTktMzMuMTQ2IDIyLjAxOS01My4zNDYgMjIuMDE5eiIvPjwvc3ZnPg==");
		  background-position: center 2px;
		  background-size: 75% auto;
		}

		a.ow-attach-dir:before {
		  margin-right: 5px;
		  content: "";
		  height: 20px;
		  vertical-align: middle;
		  width: 20px;
		  background-repeat: no-repeat;
		  display: inline-block;
		  /* folder icon if folder class is specified */
		  background-image: url("data:image/svg+xml;base64,PHN2ZyB4bWxucz0naHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmcnIHZpZXdCb3g9JzAgMCAxMDAgMTAwJz48cGF0aCBmaWxsPSdsaWdodGJsdWUnIGQ9J005Ni40MjksMzcuNXYzOS4yODZjMCwzLjQyMy0xLjIyOCw2LjM2MS0zLjY4NCw4LjgxN2MtMi40NTUsMi40NTUtNS4zOTUsMy42ODMtOC44MTYsMy42ODNIMTYuMDcxIGMtMy40MjMsMC02LjM2Mi0xLjIyOC04LjgxNy0zLjY4M2MtMi40NTYtMi40NTYtMy42ODMtNS4zOTUtMy42ODMtOC44MTdWMjMuMjE0YzAtMy40MjIsMS4yMjgtNi4zNjIsMy42ODMtOC44MTcgYzIuNDU1LTIuNDU2LDUuMzk0LTMuNjgzLDguODE3LTMuNjgzaDE3Ljg1N2MzLjQyMiwwLDYuMzYyLDEuMjI4LDguODE3LDMuNjgzYzIuNDU1LDIuNDU1LDMuNjgzLDUuMzk1LDMuNjgzLDguODE3VjI1aDM3LjUgYzMuNDIyLDAsNi4zNjEsMS4yMjgsOC44MTYsMy42ODNDOTUuMjAxLDMxLjEzOCw5Ni40MjksMzQuMDc4LDk2LjQyOSwzNy41eicgLz48L3N2Zz4K");
		  background-position: center top;
		  background-size: 75% auto;
		}

		/* Attachments list - (:attachlist:) wiki command */
		.ow-attach-list ul {
		  margin-left: 15px;
		  padding-left: 10px;
		  border-left: 1px dashed #ddd;
		}

		.ow-attach-list li {
		  list-style: none;
		  font-weight: normal;
		}

		.ow-attach-list a.ow-attach-dir {
		  font-weight: bold;
		  font-style: normal;
		  transition: all 0.2s ease;
		}
    '''
