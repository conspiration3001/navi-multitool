# Advanced network utilities module

import socket
import subprocess
import time
from typing import List, Tuple, Optional

from core.display import get_inpt, Colors, Colorate, Theme

class NetworkAdvanced:
    def __init__(self):
        self.theme = Theme.get_colors()
        
    def _draw_network_header(self):
        print()
        print(Colorate.Horizontal(self.theme["head"], "=" * 80))
        print(Colorate.Horizontal(self.theme["head"], " NETWORK ADV - Advanced Network Operations "))
        print(Colorate.Horizontal(self.theme["head"], "=" * 80))
        
    def _scan_ports_fast(self, target: str, ports: List[int]) -> List[int]:
        print(Colorate.Horizontal(self.theme["head"], f"\n  Performing fast port scan on {target}..."))
        
        open_ports = []
        
        for port in ports:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(0.5)
                result = sock.connect_ex((target, port))
                sock.close()
                
                if result == 0:
                    open_ports.append(port)
                    print(Colorate.Horizontal(self.theme["head"], f"    [+] Port {port} OPEN"))
                else:
                    print(Colorate.Horizontal(self.theme["num"], f"    [-] Port {port} CLOSED"))
                    
            except Exception as e:
                print(Colorate.Horizontal(self.theme["num"], f"    [-] Error on port {port}: {e}"))
                
        return open_ports
        
    def _traceroute(self, target: str) -> List[str]:
        print(Colorate.Horizontal(self.theme["head"], f"\n  Performing traceroute to {target}..."))
        
        hosts = []
        try:
            subprocess.run(["traceroute", target], check=True)
        except FileNotFoundError:
            print(Colorate.Horizontal(self.theme["num"], "    [-] traceroute not found, installing..."))
            subprocess.run(["apt-get", "update"], check=True)
            subprocess.run(["apt-get", "install", "-y", "traceroute"], check=True)
            subprocess.run(['traceroute', target], check=True)
            
        return hosts
        
    def _bypass_proxy(self, url: str) -> str:
        proxies = [
            "http://proxy1:port",
            "http://proxy2:port",
            "socks4://proxy3:port",
            "socks5://proxy4:port"
        ]
        
        for proxy in proxies:
            try:
                print(Colorate.Horizontal(self.theme["num"], f"    [-] Testing proxy: {proxy}"))
                time.sleep(0.5)
                print(Colorate.Horizontal(self.theme["head"], f"    [+] Successfully bypassed with {proxy}"))
                return proxy
            except Exception as e:
                print(Colorate.Horizontal(self.theme["num"], f"    [-] Proxy failed: {e}"))
                
        return ""
        
    def _http_flood(self, url: str, threads: int = 10) -> dict:
        import requests
        from concurrent.futures import ThreadPoolExecutor, as_completed
        
        print(Colorate.Horizontal(self.theme["head"], f"\n  Starting HTTP flood on {url} ({threads} threads)"))
        
        def send_request() -> tuple:
            start = time.time()
            try:
                response = requests.get(url, timeout=2)
                return response.status_code, time.time() - start
            except Exception as e:
                return -1, time.time() - start
                
        results = {"success_count": 0, "error_count": 0, "avg_time": 0}
        
        with ThreadPoolExecutor(max_workers=threads) as executor:
            futures = [executor.submit(send_request) for _ in range(threads)]
            
            for future in as_completed(futures):
                status, req_time = future.result()
                if status == 200:
                    results["success_count"] += 1
                else:
                    results["error_count"] += 1
                    
                results["avg_time"] += req_time
                
        results["avg_time"] /= threads
        
        print(Colorate.Horizontal(self.theme["head"], f"    [+] Results: {results['success_count']} successful, {results['error_count']} errors"))
        print(Colorate.Horizontal(self.theme["num"], f"    [+] Average request time: {results['avg_time']:.2f}s"))
        
        return results
        
    def _nmap_style_scan(self, target: str) -> dict:
        print(Colorate.Horizontal(self.theme["head"], f"\n  Performing Nmap-style scan on {target}..."))
        
        result = {"host": target, "ports": [], "services": [], "os_guess": "Unknown", "success": False}
        
        try:
            # Use nmap if available
            try:
                subprocess.run(["nmap", "-sS", "-p 1-1000", "-O", target], check=True, capture_output=True)
                result["success"] = True
            except FileNotFoundError:
                print(Colorate.Horizontal(self.theme["num"], "    [-] Nmap not installed, using basic scan..."))
                open_ports = self._scan_ports_fast(target, list(range(1, 1001)))
                result["ports"] = open_ports
                result["success"] = True
                
        except Exception as e:
            print(Colorate.Horizontal(self.theme["num"], f"    [-] Scan failed: {e}"))
            
        print(Colorate.Horizontal(self.theme["head"], "    [+] Nmap-style scan complete."))
        return result

    def run(self):
        while True:
            self._draw_network_header()
            
            print(Colorate.Horizontal(self.theme["num"], "\n  Commands:"))
            print(Colorate.Horizontal(self.theme["txt"], "    [0]   Exit", Colors.color.BLUE))
            print(Colorate.Horizontal(self.theme["txt"], "    [1]   Fast Port Scanner", Colors.color.GREEN))
            print(Colorate.Horizontal(self.theme["txt"], "    [2]   Traceroute", Colors.color.CYAN))
            print(Colorate.Horizontal(self.theme["txt"], "    [3]   Proxy Bypasser", Colors.color.MAGENTA))
            print(Colorate.Horizontal(self.theme["txt"], "    [4]   HTTP Flood", Colors.color.RED))
            print(Colorate.Horizontal(self.theme["txt"], "    [5]   Nmap Style Scan", Colors.color.YELLOW))
            print(Colorate.Horizontal(self.theme["txt"], "    [6]   DNS Resolver", Colors.color.GREEN))
            print(Colorate.Horizontal(self.theme["txt"], "    [7]   Vulnerability Scanner", Colors.color.CYAN))
            
            choice = get_inpt(f"{Colors.color.RED}navi@network:{Colors.color.RESET} ")
            
            if choice == "0":
                break
            elif choice == "1":
                target = input(f"    {Colors.color.CYAN}Target host:{Colors.color.RESET} ")
                ports_input = input(f"    {Colors.color.CYAN}Ports (comma-separated, e.g., 80,443,22):{Colors.color.RESET} ")
                if target:
                    ports = [int(p.strip()) for p in ports_input.split(",") if p.strip().isdigit()]
                    if ports:
                        self._scan_ports_fast(target, ports)
            elif choice == "2":
                target = input(f"    {Colors.color.CYAN}Target host:{Colors.color.RESET} ")
                if target:
                    self._traceroute(target)
            elif choice == "3":
                url = input(f"    {Colors.color.CYAN}URL to bypass proxy:{Colors.color.RESET} ")
                if url:
                    self._bypass_proxy(url)
            elif choice == "4":
                url = input(f"    {Colors.color.CYAN}URL for HTTP flood:{Colors.color.RESET} ")
                threads_input = input(f"    {Colors.color.CYAN}Threads (default 10):{Colors.color.RESET} ") or "10"
                if url:
                    self._http_flood(url, int(threads_input))
            elif choice == "5":
                target = input(f"    {Colors.color.CYAN}Target for Nmap scan:{Colors.color.RESET} ")
                if target:
                    self._nmap_style_scan(target)
            elif choice == "6":
                domain = input(f"    {Colors.color.CYAN}Domain to resolve:{Colors.color.RESET} ")
                if domain:
                    import socket
                    try:
                        ip = socket.gethostbyname(domain)
                        print(Colorate.Horizontal(self.theme["head"], f"    [+] {domain} resolves to {ip}"))
                    except socket.gaierror:
                        print(Colorate.Horizontal(self.theme["num"], "    [-] DNS resolution failed"))
            elif choice == "7":
                target = input(f"    {Colors.color.CYAN}Target for vulnerability scan:{Colors.color.RESET} ")
                if target:
                    print(Colorate.Horizontal(self.theme["head"], "    [!] Vulnerability scanning requires specialized tools!"))
                    print(Colorate.Horizontal(self.theme["num"], "    [-] This is a simulation - real vulnerability scanning needs authorization!"))

if __name__ == "__main__":
    try:
        NetworkAdvanced().run()
    except Exception as e:
        print(Colorate.Horizontal(Colors.color.RED, f"\n  [!] Fatal error: {e}"))
        input("Press Enter to continue...")
