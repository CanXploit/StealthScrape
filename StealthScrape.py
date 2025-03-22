from plugins.banner import print_banner as banner
from plugins.fetch import check_host
from plugins.log import log
from plugins.grab_links import grab_links

banner()


domain = input("Enter the domain: ")
check_host(domain)

grab_links(domain)