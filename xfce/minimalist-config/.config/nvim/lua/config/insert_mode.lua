local keymap = vim.keymap

-- The "Escape" shortcut 
keymap.set("i", "jk", "<Esc>")
keymap.set("i", "kj", "<Esc>")

-- VS Code Insert Mode muscle memory
keymap.set("i", "<C-s>", "<Esc>:w<CR>a")       -- Save while typing
keymap.set("i", "<C-v>", '<C-r>+')             -- Paste from system clipboard
-- In lua/config/insert_mode.lua
keymap.set("i", "<C-z>", "<Esc>ui", { desc = "Undo and return to insert" })keymap.set("i", "<C-Down>", "<Esc>:m .+1<CR>==gi") -- Move line down
keymap.set("i", "<C-Up>", "<Esc>:m .-2<CR>==gi")   -- Move line up

-- Deletion & Selection
keymap.set("i", "<C-BackSpace>", "<C-w>")      -- Delete word
keymap.set("i", "<C-Del>", "<Esc>ce")          -- Delete word forward
keymap.set("i", "<C-a>", "<Esc>ggVG")          -- Select All