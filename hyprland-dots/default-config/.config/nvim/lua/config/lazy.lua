local lazypath = vim.fn.stdpath("data") .. "/lazy/lazy.nvim"
if not vim.loop.fs_stat(lazypath) then
  vim.fn.system({ "git", "clone", "--filter=blob:none", "https://github.com/folke/lazy.nvim.git", "--branch=stable", lazypath })
end
vim.opt.rtp:prepend(lazypath)

require("lazy").setup({
  -- =========================
  -- [ 1. UI & COSMETICS ]
  -- =========================
  { 
    "goolord/alpha-nvim", 
    dependencies = { "nvim-tree/nvim-web-devicons" },
    config = function()
      local dashboard = require("alpha.themes.dashboard")
      -- [ YUKIVIM SPLASH SCREEN ]
      dashboard.section.header.val = {
        "██╗   ██╗██╗   ██╗██╗  ██╗██╗██╗   ██╗██╗███╗   ███╗",
        "╚██╗ ██╔╝██║   ██║██║ ██╔╝██║██║   ██║██║████╗ ████║",
        " ╚████╔╝ ██║   ██║█████╔╝ ██║██║   ██║██║██╔████╔██║",
        "  ╚██╔╝  ██║   ██║██╔═██╗ ██║╚██╗ ██╔╝██║██║╚██╔╝██║",
        "   ██║   ╚██████╔╝██║  ██╗██║ ╚████╔╝ ██║██║ ╚═╝ ██║",
        "   ╚═╝    ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝  ╚═╝╚═╝     ╚═╝",
      }
      dashboard.section.buttons.val = {
        dashboard.button("f", "  Find File", ":Telescope find_files <CR>"),
        dashboard.button("n", "  New File", ":ene <BAR> startinsert <CR>"),
        dashboard.button("r", "  Recent Files", ":Telescope oldfiles <CR>"),
        dashboard.button("u", "󰚰  Update Plugins", ":Lazy sync<CR>"),
        dashboard.button("q", "󰩈  Quit", ":qa<CR>"),
      }
      require("alpha").setup(dashboard.config)
    end
  },
  { 
    "nvim-lualine/lualine.nvim", 
    dependencies = { "nvim-tree/nvim-web-devicons" },
    opts = { options = { theme = 'dracula' } } 
  },
  { 
    "akinsho/bufferline.nvim", 
    version = "*", 
    dependencies = 'nvim-tree/nvim-web-devicons',
    config = function()
      require("bufferline").setup({
        options = {
          mode = "buffers",
          offsets = { { filetype = "NvimTree", text = "File Explorer", text_align = "left", separator = true } },
        }
      })
    end
  },
  { 
    "nvim-tree/nvim-tree.lua", 
    dependencies = { "nvim-tree/nvim-web-devicons" },
    config = function()
      require("nvim-tree").setup({
        view = { width = 30, side = "left" },
        filters = { dotfiles = false },
      })
    end
  },
  { "akinsho/toggleterm.nvim", version = "*", config = true },

  -- =========================
  -- [ 2. EDITOR FEATURES ]
  -- =========================
  {
    "andweeb/presence.nvim",
    config = function()
      require("presence").setup({
        -- General options
        client_id           = "1466198480199618766", -- Discord application client id
        enable_line_number  = true,
        auto_update         = true,
        neovim_image_text   = "YukiVim", -- Text when hovering the logo
        main_image          = "file",               -- Can be "neovim" or "file"
        
        -- Rich Presence text config
        editing_text        = "Cooking in %s",        -- e.g., "Cooking in theme.lua"
        browsing_text       = "Browsing %s",
        file_explorer_text  = "Exploring %s",      -- e.g., "Exploring nvim-tree"
        git_commit_text     = "Committing changes",
        plugin_manager_text = "Managing plugins",
        reading_text        = "Reading %s",
        workspace_text      = "Working on %s",   -- The project name
        
        -- Override the 'Neovim' name to show your custom setup name
        -- buttons = {
        --   { label = "Get YukiVim", url = "https://github.com/yourusername/yukivim" },
        -- },
      })
    end
  },
  -- [ LATEX SUPPORT ]
  {
    "lervag/vimtex",
    lazy = false, 
    init = function()
      vim.g.vimtex_view_method = "zathura"
      vim.g.vimtex_compiler_method = "latexmk"
      -- Automatically open preview on file open
      vim.g.vimtex_view_automatic = 1
    end
  },
  { 
    "nvim-treesitter/nvim-treesitter", 
    build = ":TSUpdate",
    -- This 'init' block runs BEFORE the plugin is loaded,
    -- allowing us to bypass the broken auto-setup logic.
    init = function(plugin)
      require("lazy.core.loader").disable_rtp_plugin(plugin.name)
    end,
    opts = {
      ensure_installed = { "python", "lua", "bash", "markdown" },
      highlight = { 
        enable = true, 
        additional_vim_regex_highlighting = false, 
      },
    },
    config = function(_, opts)
      -- We call the NEW setup location directly
      require("nvim-treesitter").setup(opts)
    end
  },
  { "nvim-telescope/telescope.nvim", dependencies = { "nvim-lua/plenary.nvim" } },
  { "neovim/nvim-lspconfig" },
  { "williamboman/mason.nvim" },
  { "williamboman/mason-lspconfig.nvim" },
  { "hrsh7th/nvim-cmp", dependencies = { "hrsh7th/cmp-nvim-lsp" } },
  { 
    "linux-cultist/venv-selector.nvim", 
    dependencies = { "neovim/nvim-lspconfig", "nvim-telescope/telescope.nvim" },
    opts = { name = { "env", ".venv" }, auto_refresh = false }
  },

  -- =========================
  -- [ 3. AI & AUTOMATION ]
  -- =========================
  { 
    "zbirenbaum/copilot.lua",
    config = function()
      require("copilot").setup({
        suggestion = {
          enabled = true,
          auto_trigger = true,
          keymap = { accept = "<Tab>", next = "<M-]>", prev = "<M-[>", dismiss = "<C-]>" },
        },
      })
    end
  },
  { 
    "zbirenbaum/copilot-cmp", 
    dependencies = { "copilot.lua" },
    config = function() require("copilot_cmp").setup() end
  },
})
