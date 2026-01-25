local keymap = vim.keymap
keymap.set("i", "jk", "<Esc>")
keymap.set("i", "<C-z>", "<Cmd>undo<CR>")
keymap.set("i", "<C-v>", "<C-r>+")
keymap.set("i", "<C-x>", "<Esc>ddi")
keymap.set("i", "<C-a>", "<Esc>ggVG")
keymap.set("i", "<C-d>", "<Esc>yypa")
keymap.set("i", "<C-Up>", "<Esc>:m .-2<CR>==gi")
keymap.set("i", "<C-Down>", "<Esc>:m .+1<CR>==gi")