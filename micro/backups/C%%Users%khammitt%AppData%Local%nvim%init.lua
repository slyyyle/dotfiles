-- bootstrap lazy.nvim, LazyVim and your plugins
require("nvim-treesitter.install").prefer_guit = false
require("nvim-treesitter.install").compilers = { "clang", "gcc" }
require("config.lazy")w