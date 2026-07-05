import os

installers = [
    "hyprland-dots/default-config/install.py",
    "hyprland-dots/minimalist-config/install.py",
    "i3-dots/fancy-config/install.py",
    "i3-dots/minimalist-config/install.py",
    "xfce/fancy-config/install.py",
    "xfce/minimalist-config/install.py",
]

prompt_code_kb = """
    kb_choice = input(f"{YELLOW}[?]{NC} Choose keyboard layout (1=US English, 2=Spanish, 3=Latin American) [1/2/3]: ").strip()
    if kb_choice == '2': kb_layout = 'es'
    elif kb_choice == '3': kb_layout = 'latam'
    else: kb_layout = 'us'
"""

patch_code_hyprland_kb = """
    # Patch keyboard layout
    inputs_conf = os.path.join(user_home, ".config", "hypr", "configs", "inputs.conf")
    if os.path.exists(inputs_conf):
        with open(inputs_conf, 'r') as f: content = f.read()
        content = content.replace("kb_layout = us", f"kb_layout = {kb_layout}")
        with open(inputs_conf, 'w') as f: f.write(content)
"""

patch_code_i3_kb = """
    # Patch keyboard layout
    i3_config = os.path.join(user_home, ".config", "i3", "config")
    if os.path.exists(i3_config):
        with open(i3_config, 'a') as f: 
            f.write(f"\\n# Set keyboard layout\\nexec_always --no-startup-id setxkbmap {kb_layout}\\n")
"""

patch_code_xfce_kb = """
    # Patch keyboard layout
    xfce_kb = os.path.join(user_home, ".config", "xfce4", "xfconf", "xfce-perchannel-xml", "keyboard-layout.xml")
    os.makedirs(os.path.dirname(xfce_kb), exist_ok=True)
    with open(xfce_kb, 'w') as f:
        f.write(f'''<?xml version="1.0" encoding="UTF-8"?>
<channel name="keyboard-layout" version="1.0">
  <property name="Default" type="empty">
    <property name="XkbDisable" type="bool" value="false"/>
    <property name="XkbLayout" type="string" value="{kb_layout}"/>
    <property name="XkbVariant" type="string" value=""/>
  </property>
</channel>''')
"""

for path in installers:
    full_path = os.path.join("/home/sane/Documentos/INF/dotfiles", path)
    if not os.path.exists(full_path):
        continue
        
    with open(full_path, "r") as f:
        lines = f.readlines()
        
    new_lines = []
    already_patched_prompt_kb = False
    for line in lines:
        if 'main_mod = "ALT"' in line and not already_patched_prompt_kb:
            new_lines.append(line)
            new_lines.append(prompt_code_kb)
            already_patched_prompt_kb = True
        elif 'keybind_conf = os.path.join' in line and "hyprland" in path:
            new_lines.append(patch_code_hyprland_kb)
            new_lines.append(line)
        elif 'i3_config = os.path.join' in line and "i3" in path:
            new_lines.append(patch_code_i3_kb)
            new_lines.append(line)
        elif 'xfce_keys = os.path.join' in line and "xfce" in path:
            new_lines.append(patch_code_xfce_kb)
            new_lines.append(line)
        else:
            new_lines.append(line)
            
    with open(full_path, "w") as f:
        f.writelines(new_lines)
    print(f"Patched {path}")
