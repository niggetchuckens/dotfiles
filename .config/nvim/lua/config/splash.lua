local alpha = require("alpha")
local dashboard = require("alpha.themes.dashboard")

-- [ Logo Section ]
dashboard.section.header.val = {
    "██╗   ██╗██╗   ██╗██╗  ██╗██╗██╗   ██╗██╗███╗   ███╗",
    "╚██╗ ██╔╝██║   ██║██║ ██╔╝██║██║   ██║██║████╗ ████║",
    "  ╚████╔╝ ██║   ██║█████╔╝ ██║██║   ██║██║██╔████╔██║",
    "   ╚██╔╝  ██║   ██║██╔═██╗ ██║╚██╗ ██╔╝██║██║╚██╔╝██║",
    "    ██║   ╚██████╔╝██║  ██╗██║ ╚████╔╝ ██║██║ ╚═╝ ██║",
    "    ╚═╝    ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝  ╚═╝╚═╝     ╚═╝",
}

-- [ Menu Buttons ]
dashboard.section.buttons.val = {
    dashboard.button("f", "  Find File", ":Telescope find_files <CR>"),
    dashboard.button("n", "  New File", ":ene <BAR> startinsert <CR>"),
    dashboard.button("r", "  Recent Files", ":Telescope oldfiles <CR>"),
    dashboard.button("g", "  Find Text", ":Telescope live_grep <CR>"),
    dashboard.button("l", "󰒲  Lazy Plugins", ":Lazy<CR>"),
    dashboard.button("q", "  Quit YukiVim", ":qa<CR>"),
}

-- [ Styling ]
dashboard.section.header.opts.hl = "YukiPurple"
dashboard.section.buttons.opts.hl = "YukiCyan"

alpha.setup(dashboard.config)