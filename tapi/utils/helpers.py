from ipaddress import ip_network


def is_ip_valid(ip: str) -> bool:
    try:
        ip_network(ip, strict=False)
        return True
    except ValueError:
        return False