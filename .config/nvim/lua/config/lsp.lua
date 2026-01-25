require("mason").setup()
require("mason-lspconfig").setup({ ensure_installed = { "pyright" } })

local capabilities = require("cmp_nvim_lsp").default_capabilities()

-- Neovim 0.11+ API
vim.lsp.config("pyright", {
    cmd = { "pyright-langserver", "--stdio" },
    filetypes = { "python" },
    root_markers = { "env", ".git" },
    capabilities = capabilities,
})
vim.lsp.enable("pyright")

-- Standard Keybinds: gd (definition), K (hover)
vim.api.nvim_create_autocmd('LspAttach', {
  callback = function(args)
    local opts = { buffer = args.buf }
    vim.keymap.set('n', 'K', vim.lsp.buf.hover, opts)
    vim.keymap.set('n', 'gd', vim.lsp.buf.definition, opts)
    vim.keymap.set('n', '<leader>rn', vim.lsp.buf.rename, opts)
  end,
})
