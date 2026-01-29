local set_hl = vim.api.nvim_set_hl

-- [ 1. SYNTHWAVE '84 OFFICIAL PALETTE ]
local colors = {
  -- Base colors
  bg          = "#262335",
  bg_dark     = "#1e1a2c",
  bg_lighter  = "#2d2b45",
  fg          = "#ffffff",
  fg_dim      = "#e8e8e8",
  
  -- Neon colors
  pink        = "#ff7edb",  -- Variables, properties (vibrant hot pink)
  cyan        = "#03edf9",  -- Functions, methods
  yellow      = "#fede5d",  -- Keywords, operators
  orange      = "#f97e72",  -- Strings
  purple      = "#b893ce",  -- Types, classes
  red         = "#fe4450",  -- Errors, special (and modules)
  green       = "#72f1b8",  -- Numbers, constants
  
  -- UI colors
  grey        = "#848bb2",
  grey_dark   = "#5c4a7a",
  selection   = "#444267",
  line_hl     = "#2d2b45",
}

-- [ 2. BASE UI ELEMENTS ]
-- Default base text should be white; specific syntax (like variables) will override this to pink
set_hl(0, "Normal", { bg = colors.bg, fg = colors.fg })
set_hl(0, "NormalFloat", { bg = colors.bg_dark, fg = colors.fg })
set_hl(0, "FloatBorder", { bg = colors.bg_dark, fg = colors.purple })
set_hl(0, "Pmenu", { bg = colors.bg_lighter, fg = colors.fg })
set_hl(0, "PmenuSel", { bg = colors.selection, fg = colors.cyan, bold = true })
set_hl(0, "PmenuSbar", { bg = colors.bg_lighter })
set_hl(0, "PmenuThumb", { bg = colors.purple })

-- Line numbers and cursor
set_hl(0, "LineNr", { fg = colors.grey_dark })
set_hl(0, "CursorLineNr", { fg = colors.yellow, bold = true })
set_hl(0, "CursorLine", { bg = colors.line_hl })
set_hl(0, "CursorColumn", { bg = colors.line_hl })

-- Visual selection
set_hl(0, "Visual", { bg = colors.selection })
set_hl(0, "VisualNOS", { bg = colors.selection })

-- Search
set_hl(0, "Search", { bg = colors.yellow, fg = colors.bg, bold = true })
set_hl(0, "IncSearch", { bg = colors.pink, fg = colors.bg, bold = true })
set_hl(0, "CurSearch", { bg = colors.cyan, fg = colors.bg, bold = true })

-- Status line
set_hl(0, "StatusLine", { bg = colors.bg_lighter, fg = colors.cyan })
set_hl(0, "StatusLineNC", { bg = colors.bg_dark, fg = colors.grey })

-- Splits and borders
set_hl(0, "VertSplit", { fg = colors.grey_dark })
set_hl(0, "WinSeparator", { fg = colors.grey_dark })

-- Tabs
set_hl(0, "TabLine", { bg = colors.bg_dark, fg = colors.grey })
set_hl(0, "TabLineFill", { bg = colors.bg_dark })
set_hl(0, "TabLineSel", { bg = colors.bg, fg = colors.cyan, bold = true })

-- [ 3. SYNTAX HIGHLIGHTING ]

-- Keywords and control flow (Neon Yellow)
set_hl(0, "Keyword", { fg = colors.yellow, bold = true })
set_hl(0, "Statement", { fg = colors.yellow, bold = true })
set_hl(0, "Conditional", { fg = colors.yellow, bold = true })
set_hl(0, "Repeat", { fg = colors.yellow, bold = true })
set_hl(0, "Label", { fg = colors.yellow, bold = true })
set_hl(0, "Operator", { fg = colors.yellow })
set_hl(0, "Exception", { fg = colors.yellow, bold = true })
set_hl(0, "@keyword", { link = "Keyword" })
set_hl(0, "@keyword.function", { link = "Keyword" })
set_hl(0, "@keyword.operator", { link = "Operator" })
set_hl(0, "@keyword.return", { link = "Keyword" })
set_hl(0, "@conditional", { link = "Conditional" })
set_hl(0, "@repeat", { link = "Repeat" })
set_hl(0, "@label", { link = "Label" })
set_hl(0, "@operator", { link = "Operator" })

-- Variables and identifiers (Neon Pink)
set_hl(0, "Identifier", { fg = colors.pink })
set_hl(0, "@variable", { fg = colors.pink })
set_hl(0, "@variable.builtin", { fg = colors.yellow, italic = true })
set_hl(0, "@variable.parameter", { fg = colors.pink, italic = true })
set_hl(0, "@variable.member", { fg = colors.pink })
set_hl(0, "@property", { fg = colors.pink })
set_hl(0, "@field", { fg = colors.pink })
set_hl(0, "@attribute", { fg = colors.pink })

-- Functions and methods (Electric Cyan)
set_hl(0, "Function", { fg = colors.cyan, bold = true })
set_hl(0, "@function", { fg = colors.cyan, bold = true })
set_hl(0, "@function.call", { fg = colors.cyan })
set_hl(0, "@function.builtin", { fg = colors.cyan, bold = true })
set_hl(0, "@method", { fg = colors.cyan })
set_hl(0, "@method.call", { fg = colors.cyan })
set_hl(0, "@constructor", { fg = colors.cyan, bold = true })

-- Strings (Sunset Orange)
set_hl(0, "String", { fg = colors.orange })
set_hl(0, "@string", { link = "String" })
set_hl(0, "@string.escape", { fg = colors.red, bold = true })
set_hl(0, "@string.special", { fg = colors.red })

-- Numbers and constants (Neon Green)
set_hl(0, "Number", { fg = colors.green })
set_hl(0, "Float", { fg = colors.green })
set_hl(0, "Boolean", { fg = colors.green, bold = true })
set_hl(0, "Constant", { fg = colors.green })
set_hl(0, "@number", { link = "Number" })
set_hl(0, "@float", { link = "Float" })
set_hl(0, "@boolean", { link = "Boolean" })
set_hl(0, "@constant", { link = "Constant" })
set_hl(0, "@constant.builtin", { fg = colors.green, bold = true })

-- Types and classes (Purple)
set_hl(0, "Type", { fg = colors.purple, bold = true })
set_hl(0, "StorageClass", { fg = colors.yellow, bold = true })
set_hl(0, "Structure", { fg = colors.purple, bold = true })
set_hl(0, "Typedef", { fg = colors.purple, bold = true })
set_hl(0, "@type", { link = "Type" })
set_hl(0, "@type.builtin", { link = "Type" })
set_hl(0, "@type.definition", { link = "Type" })
set_hl(0, "@storageclass", { link = "StorageClass" })

-- Parameters
set_hl(0, "@parameter", { fg = colors.pink, italic = true })

-- Comments (Grey Italic)
set_hl(0, "Comment", { fg = colors.grey, italic = true })
set_hl(0, "@comment", { link = "Comment" })
set_hl(0, "@comment.documentation", { fg = colors.grey, italic = true })

-- Punctuation
set_hl(0, "@punctuation.delimiter", { fg = colors.fg })
set_hl(0, "@punctuation.bracket", { fg = colors.yellow })
set_hl(0, "@punctuation.special", { fg = colors.yellow })

-- Tags (HTML/JSX)
set_hl(0, "Tag", { fg = colors.pink })
set_hl(0, "@tag", { fg = colors.pink })
set_hl(0, "@tag.attribute", { fg = colors.cyan })
set_hl(0, "@tag.delimiter", { fg = colors.yellow })

-- Markup
set_hl(0, "@markup.heading", { fg = colors.cyan, bold = true })
set_hl(0, "@markup.italic", { fg = colors.pink, italic = true })
set_hl(0, "@markup.strong", { fg = colors.pink, bold = true })
set_hl(0, "@markup.link", { fg = colors.cyan, underline = true })
set_hl(0, "@markup.link.url", { fg = colors.orange })
set_hl(0, "@markup.raw", { fg = colors.orange })

-- Diagnostics
set_hl(0, "DiagnosticError", { fg = colors.red })
set_hl(0, "DiagnosticWarn", { fg = colors.yellow })
set_hl(0, "DiagnosticInfo", { fg = colors.cyan })
set_hl(0, "DiagnosticHint", { fg = colors.grey })
set_hl(0, "DiagnosticUnderlineError", { undercurl = true, sp = colors.red })
set_hl(0, "DiagnosticUnderlineWarn", { undercurl = true, sp = colors.yellow })
set_hl(0, "DiagnosticUnderlineInfo", { undercurl = true, sp = colors.cyan })
set_hl(0, "DiagnosticUnderlineHint", { undercurl = true, sp = colors.grey })

-- Git signs
set_hl(0, "GitSignsAdd", { fg = colors.green })
set_hl(0, "GitSignsChange", { fg = colors.yellow })
set_hl(0, "GitSignsDelete", { fg = colors.red })

-- Diffs
set_hl(0, "DiffAdd", { bg = "#1a3329", fg = colors.green })
set_hl(0, "DiffChange", { bg = "#2d2a1a", fg = colors.yellow })
set_hl(0, "DiffDelete", { bg = "#3a1f23", fg = colors.red })
set_hl(0, "DiffText", { bg = "#3a3a1a", fg = colors.yellow, bold = true })

-- Special
set_hl(0, "Special", { fg = colors.red })
set_hl(0, "SpecialChar", { fg = colors.red })
set_hl(0, "SpecialComment", { fg = colors.grey, italic = true, bold = true })

-- Errors and warnings
set_hl(0, "Error", { fg = colors.red, bold = true })
set_hl(0, "ErrorMsg", { fg = colors.red, bold = true })
set_hl(0, "WarningMsg", { fg = colors.yellow, bold = true })

-- Spell checking
set_hl(0, "SpellBad", { undercurl = true, sp = colors.red })
set_hl(0, "SpellCap", { undercurl = true, sp = colors.yellow })
set_hl(0, "SpellLocal", { undercurl = true, sp = colors.cyan })
set_hl(0, "SpellRare", { undercurl = true, sp = colors.purple })

-- [ 4. LANGUAGE-SPECIFIC ENHANCEMENTS ]

-- Namespaces and modules (Red)
set_hl(0, "@namespace", { fg = colors.red, bold = true })
set_hl(0, "@module", { fg = colors.red, bold = true })
set_hl(0, "@module.builtin", { fg = colors.red, bold = true })
set_hl(0, "Include", { fg = colors.yellow, bold = true })
set_hl(0, "PreProc", { fg = colors.yellow, bold = true })
set_hl(0, "@include", { fg = colors.yellow, bold = true })
set_hl(0, "@preproc", { fg = colors.yellow, bold = true })

-- Macros and defines (Yellow)
set_hl(0, "Macro", { fg = colors.yellow, bold = true })
set_hl(0, "Define", { fg = colors.yellow, bold = true })
set_hl(0, "PreCondit", { fg = colors.yellow, bold = true })
set_hl(0, "@macro", { fg = colors.yellow, bold = true })
set_hl(0, "@define", { fg = colors.yellow, bold = true })

-- Annotations and decorators (Pink)
set_hl(0, "@annotation", { fg = colors.pink, italic = true })
set_hl(0, "@decorator", { fg = colors.pink, italic = true })

-- Escape sequences and special characters (Red)
set_hl(0, "@character", { fg = colors.green })
set_hl(0, "@character.special", { fg = colors.red, bold = true })

-- Embedded code (template literals, etc)
set_hl(0, "@embedded", { fg = colors.fg })

-- Text and markup
set_hl(0, "@text", { fg = colors.fg })
set_hl(0, "@text.literal", { fg = colors.orange })
set_hl(0, "@text.emphasis", { fg = colors.pink, italic = true })
set_hl(0, "@text.strong", { fg = colors.pink, bold = true })
set_hl(0, "@text.underline", { underline = true })
set_hl(0, "@text.strike", { strikethrough = true })
set_hl(0, "@text.title", { fg = colors.cyan, bold = true })
set_hl(0, "@text.uri", { fg = colors.cyan, underline = true })
set_hl(0, "@text.math", { fg = colors.purple })
set_hl(0, "@text.reference", { fg = colors.cyan, underline = true })
set_hl(0, "@text.environment", { fg = colors.purple })
set_hl(0, "@text.environment.name", { fg = colors.yellow })
set_hl(0, "@text.note", { fg = colors.cyan, bold = true })
set_hl(0, "@text.warning", { fg = colors.yellow, bold = true })
set_hl(0, "@text.danger", { fg = colors.red, bold = true })

-- Regex
set_hl(0, "@regex", { fg = colors.red })
set_hl(0, "@string.regex", { fg = colors.red })

-- Language-specific keywords
set_hl(0, "@keyword.import", { fg = colors.yellow, bold = true })
set_hl(0, "@keyword.export", { fg = colors.yellow, bold = true })
set_hl(0, "@keyword.modifier", { fg = colors.yellow })
set_hl(0, "@keyword.type", { fg = colors.yellow })
set_hl(0, "@keyword.coroutine", { fg = colors.yellow, bold = true })

-- Special identifiers
set_hl(0, "@symbol", { fg = colors.pink })
set_hl(0, "@namespace.builtin", { fg = colors.red, bold = true })

-- Class and struct
set_hl(0, "@class", { fg = colors.purple, bold = true })
set_hl(0, "@struct", { fg = colors.purple, bold = true })

-- Enums
set_hl(0, "@enum", { fg = colors.purple, bold = true })
set_hl(0, "@enumMember", { fg = colors.green, bold = true })

-- Interfaces (TypeScript, etc)
set_hl(0, "@interface", { fg = colors.purple, bold = true })

-- Constants and null/undefined
set_hl(0, "@constant.macro", { fg = colors.green, bold = true })
set_hl(0, "@none", { fg = colors.green, bold = true })
set_hl(0, "@null", { fg = colors.green, bold = true })

-- Function modifiers
set_hl(0, "@function.macro", { fg = colors.cyan, bold = true })
set_hl(0, "@function.method", { fg = colors.cyan, bold = true })

-- Attributes (Rust, C++, etc)
set_hl(0, "@attribute.builtin", { fg = colors.pink, italic = true })

-- Conceal
set_hl(0, "Conceal", { fg = colors.grey })

-- Debug
set_hl(0, "Debug", { fg = colors.red, bold = true })

-- Underlined
set_hl(0, "Underlined", { fg = colors.cyan, underline = true })

-- Ignore
set_hl(0, "Ignore", { fg = colors.grey_dark })

-- Todo, Fixme, Note
set_hl(0, "Todo", { fg = colors.bg, bg = colors.yellow, bold = true })
set_hl(0, "@text.todo", { fg = colors.bg, bg = colors.yellow, bold = true })
set_hl(0, "@text.todo.unchecked", { fg = colors.yellow, bold = true })
set_hl(0, "@text.todo.checked", { fg = colors.green, bold = true })

-- [ 5. LSP SEMANTIC TOKENS ]
-- These provide more semantic highlighting when LSP is active

set_hl(0, "@lsp.type.namespace", { fg = colors.red, bold = true })
set_hl(0, "@lsp.type.type", { link = "@type" })
set_hl(0, "@lsp.type.class", { link = "@class" })
set_hl(0, "@lsp.type.enum", { link = "@enum" })
set_hl(0, "@lsp.type.interface", { link = "@interface" })
set_hl(0, "@lsp.type.struct", { link = "@struct" })
set_hl(0, "@lsp.type.parameter", { fg = colors.pink, italic = true })
set_hl(0, "@lsp.type.variable", { fg = colors.pink })
set_hl(0, "@lsp.type.property", { fg = colors.pink })
set_hl(0, "@lsp.type.enumMember", { link = "@enumMember" })
set_hl(0, "@lsp.type.function", { fg = colors.cyan })
set_hl(0, "@lsp.type.method", { fg = colors.cyan })
set_hl(0, "@lsp.type.macro", { link = "@macro" })
set_hl(0, "@lsp.type.decorator", { link = "@decorator" })
set_hl(0, "@lsp.type.comment", { link = "@comment" })

-- LSP type modifiers
set_hl(0, "@lsp.mod.readonly", { italic = true })
set_hl(0, "@lsp.mod.deprecated", { strikethrough = true, fg = colors.grey })
set_hl(0, "@lsp.mod.static", { bold = true })

-- Catch-all for unmatched identifiers
set_hl(0, "@lsp.typemod.variable.defaultLibrary", { fg = colors.pink })
set_hl(0, "@lsp.typemod.function.defaultLibrary", { fg = colors.cyan })
set_hl(0, "@lsp.typemod.class.defaultLibrary", { fg = colors.red, bold = true })
set_hl(0, "@lsp.typemod.method.defaultLibrary", { fg = colors.cyan })

-- [ 6. MATCHPAREN ]
set_hl(0, "MatchParen", { bg = colors.selection, fg = colors.yellow, bold = true })

-- [ 7. FOLDS ]
set_hl(0, "Folded", { bg = colors.bg_lighter, fg = colors.grey })
set_hl(0, "FoldColumn", { fg = colors.grey_dark })

-- [ 8. WILDMENU ]
set_hl(0, "WildMenu", { bg = colors.selection, fg = colors.cyan, bold = true })

-- [ 9. DIRECTORY ]
set_hl(0, "Directory", { fg = colors.cyan, bold = true })

-- [ 10. QUESTION AND MORE MSG ]
set_hl(0, "Question", { fg = colors.green, bold = true })
set_hl(0, "MoreMsg", { fg = colors.green, bold = true })
set_hl(0, "ModeMsg", { fg = colors.cyan, bold = true })

-- [ 11. NON-TEXT CHARACTERS ]
set_hl(0, "NonText", { fg = colors.grey_dark })
set_hl(0, "SpecialKey", { fg = colors.grey_dark })
set_hl(0, "Whitespace", { fg = colors.grey_dark })

-- [ 12. COLOR COLUMN ]
set_hl(0, "ColorColumn", { bg = colors.bg_lighter })

-- [ 13. SIGN COLUMN ]
set_hl(0, "SignColumn", { bg = colors.bg })

set_hl(0, "@variable.member", { link = "YukiPink" })   -- Fixes self.attributes
set_hl(0, "@property", { link = "YukiPink" })         -- Fixes property calls
set_hl(0, "@variable.builtin", { fg = colors.yellow, italic = true }) -- 'self' in yellow
set_hl(0, "@parameter", { fg = "#ffffff", italic = true }) -- Args in white italic

-- Apply the theme
vim.g.colors_name = "synthwave84"
