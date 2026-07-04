local msg = require("mp.msg")
local opts = require("mp.options")
local utils = require("mp.utils")

function detect_platform() 
	local o = {}
	if mp.get_property_native('options/vo-mmcss-profile', o) ~= o then
		return "windows"
	elseif mp.get_property_native('options/input-app-events', o) ~= o then
		return "darwin"
	end
	return "linux" 
end

local user_os = detect_platform()

local binary_paths = {
	"/usr/bin/mpv-discord",
	"/usr/local/bin/mpv-discord",
	os.getenv("HOME") .. "/.local/bin/mpv-discord",
	"mpv-discord.exe"
}

function file_exists(path)
	local f = io.open(path, "r")
	if f ~= nil then
		io.close(f)
		return true
	end
	return false
end

local function find_binary()
    for _, path in ipairs(binary_paths) do
        if file_exists(path) then return path end
    end
    return nil
end

local options = {
	key = "c",
	active = true,
	client_id = "737663962677510245",
	binary_path = find_binary() or "", -- Try to find existing first if can't find it triggers autoinstall
	socket_path = (user_os ~= "windows" and "/tmp/" or "") .. "mpvsocket",
	autohide_threshold = 0,
}
opts.read_options(options, "discord")

local function auto_install_binary()
    if user_os ~= "linux" then return nil end
    
    local paths = {"/etc/os-release", "/usr/lib/os-release"}
    for _, path in ipairs(paths) do
        local f = io.open(path, "r")
        if f then
            local content = f:read("*all")
            f:close()

            local id = content:match('\nID=([^%s\n]+)') or content:match('^ID=([^%s\n]+)')
            local id_like = content:match('\nID_LIKE=([^%s\n]+)') or ""
            id = (id or ""):gsub('"', "")

            -- Case 1: Arch Linux (using yay as requested)
            if id == "arch" or id_like:find("arch") then
                msg.info("Arch Linux detected. Installing with yay...")
                mp.osd_message("yukivim: Installing RPC via yay...", 5)
                utils.subprocess_detached({
                    args = {"yay", "-S", "--noconfirm", "mpv-discord-git"}
                })
                return "/usr/bin/mpv-discord"

            -- Case 2: Debian/Ubuntu
            elseif id == "debian" or id == "ubuntu" or id_like:find("debian") then
                msg.info("Debian-based distro detected. Installing via git/make...")
                mp.osd_message("yukivim: Building RPC from source...", 5)
                local install_cmd = "git clone https://github.com/tnychn/mpv-discord.git /tmp/mpv-discord && cd /tmp/mpv-discord && make && sudo make install"
                utils.subprocess_detached({
                    args = {"sh", "-c", install_cmd}
                })
                return "/usr/local/bin/mpv-discord"
            end
        end
    end
    return nil
end

-- Logic to trigger installation if binary is missing
if options.binary_path == "" then
    options.binary_path = auto_install_binary() or ""
end

if options.binary_path == "" then
	msg.error("Discord RPC binary not found. Please install it manually.")
end

local socket_path = options.socket_path:gsub("{pid}", utils.getpid())
mp.set_property("input-ipc-server", socket_path)

local cmd = nil

local function start()
	if cmd == nil and file_exists(options.binary_path) then
		cmd = mp.command_native_async({
			name = "subprocess",
			playback_only = false,
			args = { options.binary_path, socket_path, options.client_id },
		}, function() cmd = nil end)
		mp.osd_message("yukivim\nDiscord RPC: Online") -- Added splash screen
	end
end

function stop()
	if cmd ~= nil then
		mp.abort_async_command(cmd)
		cmd = nil
		mp.osd_message("Discord RPC: Offline")
	end
end

-- Events and Bindings
if options.active then
	mp.register_event("file-loaded", start)
end

mp.add_key_binding(options.key, "toggle-discord", function()
	if cmd ~= nil then stop() else start() end
end)

mp.register_event("shutdown", function()
	stop()
	if user_os ~= "windows" then os.remove(socket_path) end
end)