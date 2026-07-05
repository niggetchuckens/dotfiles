import os

installers = [
    "hyprland-dots/default-config/install.py",
    "hyprland-dots/minimalist-config/install.py",
    "i3-dots/fancy-config/install.py",
    "i3-dots/minimalist-config/install.py",
    "xfce/fancy-config/install.py",
    "xfce/minimalist-config/install.py",
]

prompt_code = """
    mod_choice = input(f"{YELLOW}[?]{NC} Choose main modifier key (a=ALT, s=SUPER) [a/S]: ").strip().lower()
    main_mod = "ALT" if mod_choice == 'a' else "SUPER"
"""

patch_code_hyprland = """
    # Patch main modifier key
    keybind_conf = os.path.join(user_home, ".config", "hypr", "configs", "keybind.conf")
    if os.path.exists(keybind_conf):
        with open(keybind_conf, 'r') as f: content = f.read()
        content = content.replace("$mod = SUPER", f"$mod = {main_mod}").replace("$mod = ALT", f"$mod = {main_mod}")
        with open(keybind_conf, 'w') as f: f.write(content)
"""

patch_code_i3 = """
    # Patch main modifier key
    i3_config = os.path.join(user_home, ".config", "i3", "config")
    if os.path.exists(i3_config):
        with open(i3_config, 'r') as f: content = f.read()
        target_mod = "Mod1" if main_mod == "ALT" else "Mod4"
        content = content.replace("set $mod Mod1", f"set $mod {target_mod}").replace("set $mod Mod4", f"set $mod {target_mod}")
        with open(i3_config, 'w') as f: f.write(content)
"""

patch_code_xfce = """
    # Patch main modifier key
    xfce_keys = os.path.join(user_home, ".config", "xfce4", "xfconf", "xfce-perchannel-xml", "xfce4-keyboard-shortcuts.xml")
    if os.path.exists(xfce_keys):
        with open(xfce_keys, 'r') as f: content = f.read()
        if main_mod == "SUPER":
            content = content.replace("&lt;Alt&gt;", "&lt;Super&gt;")
            content = content.replace("&lt;Super&gt;Tab", "&lt;Alt&gt;Tab")
            content = content.replace("&lt;Super&gt;F2", "&lt;Alt&gt;F2")
            content = content.replace("&lt;Super&gt;F3", "&lt;Alt&gt;F3")
        else:
            content = content.replace("&lt;Super&gt;", "&lt;Alt&gt;")
        with open(xfce_keys, 'w') as f: f.write(content)
"""

for path in installers:
    full_path = os.path.join("/home/sane/Documentos/INF/dotfiles", path)
    if not os.path.exists(full_path):
        print(f"File not found: {full_path}")
        continue
        
    with open(full_path, "r") as f:
        lines = f.readlines()
        
    new_lines = []
    already_patched_prompt = False
    for i, line in enumerate(lines):
        # Insert prompt before deploying dotfiles
        if "# --- 2. Deploy Dotfiles ---" in line and not already_patched_prompt:
            new_lines.append(prompt_code)
            new_lines.append(line)
            already_patched_prompt = True
        elif 'copy_file(".bashrc")' in line:
            new_lines.append(line)
            # Insert patch logic after bashrc copy
            if "hyprland" in path:
                new_lines.append(patch_code_hyprland)
            elif "i3" in path:
                new_lines.append(patch_code_i3)
            elif "xfce" in path:
                new_lines.append(patch_code_xfce)
        else:
            new_lines.append(line)
            
    with open(full_path, "w") as f:
        f.writelines(new_lines)
    print(f"Patched {path}")
