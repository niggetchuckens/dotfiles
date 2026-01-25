-- Apply Catppuccin Mocha for that high-end look
require("catppuccin").setup({ flavour = "mocha" })
vim.cmd.colorscheme "catppuccin"

local set_hl = vim.api.nvim_set_hl
set_hl(0, "YukiPurple", { fg = "#8d00ff", bold = true })
set_hl(0, "YukiCyan", { fg = "#43CCEA" })

-- Statusline setup
require('lualine').setup { options = { theme = 'catppuccin' } }