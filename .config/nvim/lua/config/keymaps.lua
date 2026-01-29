local keymap = vim.keymap
vim.g.mapleader = " "

-- File Operations
keymap.set("n", "<C-s>", ":w<CR>")          -- Save
keymap.set("n", "<C-w>", ":bd<CR>")         -- Close Buffer (Tab)

-- Navigation (VS Code Style)
keymap.set("n", "<C-p>", ":Telescope find_files<CR>")      -- Quick Open
keymap.set("n", "<C-S-f>", ":Telescope live_grep<CR>")     -- Global Search
keymap.set("n", "<C-b>", ":NvimTreeToggle<CR>")            -- Toggle Sidebar
keymap.set("n", "<C-]>", ":ToggleTerm<CR>")                -- Toggle Terminal
vim.keymap.set("n", "<C-S-p>", ":Telescope commands<CR>")  -- Command palette

-- Quick Copilot Toggles
vim.keymap.set("n", "<leader>ce", ":Copilot enable<CR>", { desc = "Enable Copilot" })
vim.keymap.set("n", "<leader>cd", ":Copilot disable<CR>", { desc = "Disable Copilot" })

-- Editor Behavior
keymap.set("v", "<C-c>", '"+y')             -- Copy (Visual Mode)
keymap.set("n", "<C-a>", "ggVG")            -- Select All
keymap.set("n", "<C-Down>", ":m .+1<CR>==") -- Move line down (Alt + Down)
keymap.set("n", "<C-Up>", ":m .-2<CR>==")   -- Move line up (Alt + Up)

-- Multi-cursor "lite" (Add lines above/below)
keymap.set("n", "<C-d>", "yyp")             -- Duplicate line

-- Start/Stop LaTeX Live Preview with Zathura
vim.keymap.set("n", "<leader>p", "<cmd>VimtexCompile<CR>", { desc = "Toggle LaTeX Preview" })

-- Allow Shift + Arrows to start selection in all modes
vim.opt.keymodel = "startsel,stopsel"
vim.opt.selection = "exclusive"

-- Keymaps to make Shift-Selection work from Insert and Normal mode
local modes = { "n", "i", "v" }
for _, mode in ipairs(modes) do
  vim.keymap.set(mode, "<S-Up>", "<cmd>normal! v<Up><CR>")
  vim.keymap.set(mode, "<S-Down>", "<cmd>normal! v<Down><CR>")
  vim.keymap.set(mode, "<S-Left>", "<cmd>normal! v<Left><CR>")
  vim.keymap.set(mode, "<S-Right>", "<cmd>normal! v<Right><CR>")
end

-- Allow Backspace and Delete to work on the selection
vim.keymap.set("s", "<BS>", "<C-O>c", { noremap = true })
vim.keymap.set("s", "<Del>", "<C-O>c", { noremap = true })

-- Tab Navigation (Next/Prev buffer)
vim.keymap.set("n", "<S-l>", ":BufferLineCycleNext<CR>") -- Shift + l (Right)
vim.keymap.set("n", "<S-h>", ":BufferLineCyclePrev<CR>") -- Shift + h (Left)
vim.keymap.set("n", "<S-Right>", ":BufferLineCycleNext<CR>") -- Shift + l (Right)
vim.keymap.set("n", "<S-Left>", ":BufferLineCyclePrev<CR>") -- Shift + h (Left)

-- VS Code style: Close current tab
vim.keymap.set("n", "<C-w>", ":bdelete<CR>")

vim.keymap.set("n", "<C-z>", "<Nop>") -- Fix ctrl+z to suspend
keymap.set({ "n", "v" }, "<C-z>", "u", { desc = "Undo" }) -- VS Code Undo (Ctrl+z)
keymap.set({ "n", "v" }, "<C-y>", "<C-r>", { desc = "Redo" }) -- VS Code Redo (Ctrl+y)
