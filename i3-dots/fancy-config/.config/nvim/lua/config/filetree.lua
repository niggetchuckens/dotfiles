-- 1. Completely disable netrw to stop the E117 error
vim.g.loaded_netrw = 1
vim.g.loaded_netrwPlugin = 1

local setup, nvimtree = pcall(require, "nvim-tree")
if not setup then return end

nvimtree.setup({
  -- VS Code Style: Close tree when opening a file
  actions = {
    open_file = {
      quit_on_open = true, -- Set to true/false if you want it to hide or not after picking a file
    },
  },
  view = {
    width = 30,
    side = "left",
  },
  renderer = {
    icons = {
      show = {
        file = true,
        folder = true,
        folder_arrow = true,
        git = true,
      },
    },
  },
  filters = {
    dotfiles = false,
  },
})

-- 2. VS Code "Auto-Close" Logic
-- If the only window left open is NvimTree, close it automatically.
vim.api.nvim_create_autocmd("QuitPre", {
  callback = function()
    local invalid_win = {}
    local wins = vim.api.nvim_list_wins()
    for _, w in ipairs(wins) do
      local bufname = vim.api.nvim_buf_get_name(vim.api.nvim_win_get_buf(w))
      if bufname:match("NvimTree_") ~= nil then
        table.insert(invalid_win, w)
      end
    end
    if #invalid_win == #wins - 1 then
      for _, w in ipairs(invalid_win) do vim.api.nvim_win_close(w, true) end
    end
  end
})

-- 3. Keybinds
vim.keymap.set("n", "<C-b>", ":NvimTreeToggle<CR>", { desc = "Toggle File Explorer" })
vim.keymap.set("n", "<leader>e", ":NvimTreeToggle<CR>", { desc = "Toggle File Explorer" })