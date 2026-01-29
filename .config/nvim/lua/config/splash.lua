local alpha_ok, alpha = pcall(require, "alpha")
if not alpha_ok then return end

local dashboard = require("alpha.themes.dashboard")

-- [ Logo Section with yukivim ]
dashboard.section.header.val = {
    " ██╗   ██╗██╗   ██╗██╗  ██╗██╗██╗   ██╗██╗███╗   ███╗",
    " ╚██╗ ██╔╝██║   ██║██║ ██╔╝██║██║   ██║██║████╗ ████║",
    "  ╚████╔╝ ██║   ██║█████╔╝ ██║██║   ██║██║██╔████╔██║",
    "   ╚██╔╝  ██║   ██║██╔═██╗ ██║╚██╗ ██╔╝██║██║╚██╔╝██║",
    "    ██║   ╚██████╔╝██║  ██╗██║ ╚████╔╝ ██║██║ ╚═╝ ██║",
    "    ╚═╝    ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝  ╚═╝╚═╝     ╚═╝",
    "             --- yukivim Edition ---                 ",
}

-- [ Menu Buttons ]
dashboard.section.buttons.val = {
    dashboard.button("f", "  Find File", ":Telescope find_files <CR>"),
    dashboard.button("n", "  New File", ":ene <BAR> startinsert <CR>"),
    dashboard.button("r", "  Recent Files", ":Telescope oldfiles <CR>"),
    dashboard.button("u", "󰚰  Update Plugins", ":Lazy sync<CR>"),
    dashboard.button("q", "󰩈  Quit", ":qa<CR>"),
}

alpha.setup(dashboard.config)