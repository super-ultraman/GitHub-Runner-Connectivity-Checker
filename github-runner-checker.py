import json
import socket
import ssl
import sys
import warnings
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from typing import Dict, List, Tuple

import requests
from colorama import Fore, Style, init
from prettytable import PrettyTable

class DomainChecker:
    def __init__(self, timeout: int = 5):
        self.timeout = timeout
        self.domains = {
            "Essential Operations": [
                "github.com",
                "api.github.com",
                "*.actions.githubusercontent.com"
            ],
            "Downloading Actions": [
                "codeload.github.com",
                "pkg.actions.githubusercontent.com"
            ],
            "GitHub Packages & Publishing Actions": [
                "ghcr.io",
                "*.pkg.github.com",
                "pkg-containers.githubusercontent.com"
            ],
            "Artifacts and Logs": [
                "results-receiver.actions.githubusercontent.com"
            ],
            "Runner Updates": [
                "objects.githubusercontent.com",
                "objects-origin.githubusercontent.com",
                "github-releases.githubusercontent.com",
                "github-registry-files.githubusercontent.com"
            ],
            "OIDC Tokens": [
                "*.actions.githubusercontent.com"
            ],
            "Git LFS": [
                "github-cloud.githubusercontent.com",
                "github-cloud.s3.amazonaws.com"
            ],
            "Dependabot": [
                "dependabot-actions.githubapp.com"
            ]
        }

    def resolve_wildcards(self, domain: str) -> List[str]:
        if not domain.startswith('*'):
            return [domain]
        
        if domain == "*.actions.githubusercontent.com":
            return [
                "pipelines.actions.githubusercontent.com",
                "artifacts.actions.githubusercontent.com",
                "results.actions.githubusercontent.com"
            ]
        elif domain == "*.pkg.github.com":
            return ["npm.pkg.github.com", "nuget.pkg.github.com", "maven.pkg.github.com"]
        
        return [domain.replace("*.", "")]

    def check_domain(self, domain: str) -> Tuple[str, bool, str]:
        try:
            ip = socket.gethostbyname(domain)
            
            try:
                response = requests.get(f"https://{domain}", timeout=self.timeout, verify=True)
                if response.status_code < 500 or response.status_code in [502, 503, 504]:
                    status_desc = "Accessible" if response.status_code < 400 else f"Accessible (Status: {response.status_code})"
                    return domain, True, f"{status_desc} (HTTPS) - IP: {ip}"
                else:
                    return domain, False, f"HTTP Error {response.status_code} - IP: {ip}"
            except requests.exceptions.RequestException as e:
                return domain, True, f"DNS Resolved - IP: {ip} (HTTPS connection failed)"
                
        except socket.gaierror:
            return domain, False, "DNS resolution failed"
        except Exception as e:
            return domain, False, f"Error: {str(e)}"

    def check_all_domains(self) -> Dict:
        results = {}
        
        with ThreadPoolExecutor(max_workers=10) as executor:
            for category, domains in self.domains.items():
                category_results = []
                
                for domain in domains:
                    resolved_domains = self.resolve_wildcards(domain)
                    
                    for resolved_domain in resolved_domains:
                        future = executor.submit(self.check_domain, resolved_domain)
                        domain, success, message = future.result()
                        category_results.append({
                            "domain": domain,
                            "success": success,
                            "message": message
                        })
                
                results[category] = category_results
        
        return results

    def generate_report(self, results: Dict) -> str:
        init()

        console_report = f"\nDomain Accessibility Report - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        table = PrettyTable()
        table.field_names = ["Category", "Status", "Domain", "Details"]
        table.align["Category"] = "l"
        table.align["Domain"] = "l"
        table.align["Details"] = "l"
        table.max_width["Details"] = 60
        
        all_accessible = True
        sorted_categories = sorted(results.keys())
        for category in sorted_categories:
            domains = results[category]
            for domain_info in domains:
                status = f"{Fore.GREEN}✓{Style.RESET_ALL}" if domain_info["success"] else f"{Fore.RED}✗{Style.RESET_ALL}"
                table.add_row([
                    category,
                    status,
                    domain_info['domain'],
                    domain_info['message']
                ])
                
                if not domain_info["success"]:
                    all_accessible = False
        
        console_report += str(table) + "\n"
        
        overall_status = (f"{Fore.GREEN}✓ All domains are accessible{Style.RESET_ALL}" 
                         if all_accessible 
                         else f"{Fore.RED}✗ Some domains are not accessible{Style.RESET_ALL}")
        console_report += f"Overall Status: {overall_status}\n"
        
        return console_report

def main():
    warnings.filterwarnings('ignore', category=Warning)
    
    checker = DomainChecker()
    print("\nChecking domain accessibility... Please wait...")
    results = checker.check_all_domains()
    report = checker.generate_report(results)
    
    print(report)
    

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    json_file = f"domain_check_results_{timestamp}.json"
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nDetailed results saved to: {json_file}")

if __name__ == "__main__":
    main()
