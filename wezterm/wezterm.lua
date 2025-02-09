local wezterm = require 'wezterm'
local config = {}

config.font = wezterm.font_with_fallback({
    {
        family = "DaddyTimeMono Nerd Font",
    },
    {
        family = "Hack Nerd Font",
    },
})

config.audible_bell = 'Disabled'
config.automatically_reload_config = true
config.color_scheme = 'Nocturnal Winter'
config.window_background_opacity = 0.7
config.text_background_opacity = 0.7
config.default_prog = {'pwsh', '-NoLogo'}
config.enable_scroll_bar = true
config.enable_tab_bar = true
config.colors = {
    scrollbar_thumb = 'white',
}
config.exit_behavior = 'CloseOnCleanExit'
config.cursor_blink_rate = 800
config.bold_brightens_ansi_colors = 'BrightAndBold'
config.macos_window_background_blur = 20
config.max_fps = 120
config.prefer_to_spawn_tabs = true
config.scrollback_lines = 7000
config.show_tab_index_in_tab_bar = false
config.window_close_confirmation = 'NeverPrompt'
return config
