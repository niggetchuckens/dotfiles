vim.opt.termguicolors = true
vim.cmd("syntax on")
vim.opt.background = "dark"

-- Tab and Indentation
vim.opt.tabstop = 4      -- Number of spaces a tab counts for
vim.opt.softtabstop = 4  -- Number of spaces a tab counts for while editing
vim.opt.shiftwidth = 4   -- Size of an indent
vim.opt.expandtab = true -- Turn tabs into spaces

require("config.options")    -- Sets up basic UI/Clipboard
require("config.filetree")   -- DISBLES netrw immediately to prevent the error
require("config.lazy")       -- Loads your plugins
require("config.splash")     -- Shows the yukivim splash
require("config.keymaps")    -- Normal mode binds
require("config.insert_mode") -- VS Code insert binds
require("config.lsp")        -- LSP and Copilot
require("config.theme")
