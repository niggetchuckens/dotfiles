require("mason").setup()
require("mason-lspconfig").setup({ ensure_installed = { "pyright" } })

local cmp = require("cmp")
local capabilities = require("cmp_nvim_lsp").default_capabilities()

-- 1. Setup Completion Engine (CMP) with Copilot
cmp.setup({
  mapping = cmp.mapping.preset.insert({
    -- Use Enter to confirm menu items, leaving Tab for Copilot
    ['<CR>'] = cmp.mapping.confirm({ select = true }),
    -- Use Tab for normal tabbing if the menu isn't open
    ["<Tab>"] = cmp.mapping(function(fallback)
      if cmp.visible() then
        cmp.select_next_item()
      else
        fallback()
      end
    end, { "i", "s" }),
  }),
  sources = {
    { name = "nvim_lsp" },
    { name = "path" },
    { name = "buffer" },
  },
})

-- 2. Neovim 0.11+ API for Python
vim.lsp.config("pyright", {
    cmd = { "pyright-langserver", "--stdio" },
    filetypes = { "python" },
    root_markers = { "env", ".git" },
    capabilities = capabilities,
})
vim.lsp.enable("pyright")

-- 3. Standard Keybinds
vim.api.nvim_create_autocmd('LspAttach', {
  callback = function(args)
    local opts = { buffer = args.buf }
    vim.keymap.set('n', 'K', vim.lsp.buf.hover, opts)
    vim.keymap.set('n', 'gd', vim.lsp.buf.definition, opts)
    vim.keymap.set('n', '<leader>rn', vim.lsp.buf.rename, opts)
  end,
})