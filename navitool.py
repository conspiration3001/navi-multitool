# Core launcher script for Navi Multitool

import sys
import os
import importlib.util
import traceback

from core.display import get_inpt, Colors, Colorate, Theme
from core.modern_ui import ModernUI
from core.paginated_ui import PaginatedUI
# from modules.boot import BootManager  # Not available

MODULES_DIR = "modules/"

class NaviLauncher:
    def __init__(self):
        self.theme = Theme.get_colors()
        self.modules_info = self._load_modules()
        
    def _load_modules(self):
        modules = {}
        for category in ["shell", "exploit", "stealth", "network_advanced", "packet_analysis", "dynamic", "crypto_advanced"]:
            category_path = os.path.join(MODULES_DIR, category)
            if os.path.exists(category_path):
                for filename in os.listdir(category_path):
                    if filename.endswith('.py') and not filename.startswith('_'):
                        module_name = f"{category}.{filename[:-3]}"
                        try:
                            spec = importlib.util.spec_from_file_location(module_name, os.path.join(category_path, filename))
                            module = importlib.util.module_from_spec(spec)
                            spec.loader.exec_module(module)
                            
                            # Find main function or class
                            main_func = None
                            for attr_name in dir(module):
                                if attr_name.startswith('run_') or attr_name.startswith('start_') or attr_name == 'main':
                                    main_func = getattr(module, attr_name)
                                    break
                                    
                            modules[module_name] = {
                                'module': module,
                                'display_name': filename.replace('_', ' ').title(),
                                'description': f"Advanced {category.replace('_', ' ')} tool",
                                'category': category,
                                'has_ui': callable(getattr(module, 'show_ui', None))
                            }
                        except Exception as e:
                            print(f"Error loading {module_name}: {e}")
        return modules
        
    def _draw_advanced_header(self):
        PaginatedUI.draw_logo(self.theme)
        width = 80
        left = "=" * ((width - 20) // 2)
        right = "=" * (width - 20 - len(left))
        print(f"\n{left} Advanced Navi Multitool Launcher {right}\n")
        
    def _draw_module_menu(self):
        by_category = {}
        for mod_name, mod_info in self.modules_info.items():
            cat = mod_info['category']
            if cat not in by_category:
                by_category[cat] = []
            by_category[cat].append((mod_name, mod_info))
            
        for category in ["shell", "exploit", "stealth", "network_advanced", "packet_analysis", "dynamic", "crypto_advanced"]:
            if category in by_category:
                mods = by_category[category]
                print(f"\n{self.theme['head']}[{category.upper()}] Advanced Tools:")
                for i, (mod_name, mod_info) in enumerate(mods[:10], 1):
                    print(f"  {i}. {mod_info['display_name']} - {mod_info['description']}")
                if len(mods) > 10:
                    print(f"  ... and {len(mods) - 10} more tools")
                    
    def _execute_module(self, mod_name):
        try:
            mod_info = self.modules_info[mod_name]
            module = mod_info['module']
            
            if mod_info.get('has_ui') and hasattr(module, 'show_ui'):
                module.show_ui(self.theme)
            elif hasattr(module, 'main'):
                module.main(self.theme)
            elif hasattr(module, '__call__'):
                module(self.theme)
            else:
                print(f"{self.theme['num']}[!] Module {mod_name} has no callable entry point!")
                print(f"{self.theme['txt']}[!] Available methods: {', '.join([m for m in dir(module) if not m.startswith('_')])}")
        except Exception as e:
            print(f"{self.theme['num']}[!] Error executing module {mod_name}:")
            print(f"{self.theme['txt']}[!] {traceback.format_exc()}")
            
    def launch_mode(self):
        self._draw_advanced_header()
        
        total_modules = sum(len(v) for v in self.modules_info.values())
        print(f"{self.theme['txt']}Total available advanced tools: {total_modules}")
        
        while True:
            self._draw_module_menu()
            print(f"\n{self.theme['num']}[0] Exit Launcher")
            print(f"{self.theme['num']}[R] Refresh Modules")
            
            choice = get_inpt(f"{Colors.red}navi@launcher:{Colors.reset} ")
            
            if choice == "0":
                break
            elif choice.upper() == "R":
                self.modules_info = self._load_modules()
                continue
                
            if choice and choice.isdigit():
                choice_idx = int(choice)
                
                ordered_mods = []
                for cat in ["shell", "exploit", "stealth", "network_advanced", "packet_analysis", "dynamic", "crypto_advanced"]:
                    if cat in self.modules_info:
                        ordered_mods.extend(self.modules_info.items())
                        
                if 1 <= choice_idx <= len(ordered_mods):
                    mod_name = ordered_mods[choice_idx - 1][0]
                    print(f"\n{self.theme['head']}[*] Launching module: {self.modules_info[mod_name]['display_name']}")
                    self._execute_module(mod_name)
                    print(f"\n{self.theme['num']}[+] Press Enter to return to launcher...")
                    input()
                else:
                    print(f"{self.theme['num']}[!] Invalid choice. Please select a number between 1 and {len(ordered_mods)}")

if __name__ == "__main__":
    launcher = NaviLauncher()
    launcher.launch_mode()
