from ipaddress import ip_address, ip_network

from sqlalchemy.orm import Session

from app.services.list_service import get_list_values


def ip_matches_list(ip: str, entries: set[str]) -> bool:
    try:
        parsed_ip = ip_address(ip)
    except ValueError:
        return False

    for entry in entries:
        try:
            if "/" in entry:
                if parsed_ip in ip_network(entry, strict=False):
                    return True
            elif parsed_ip == ip_address(entry):
                return True
        except ValueError:
            continue

    return False


def is_blocked_ip(db: Session, ip: str) -> bool:
    blocked_ips = get_list_values(db, "blocked_ips")
    return ip_matches_list(ip, blocked_ips)


def is_relay_allowed_ip(db: Session, ip: str) -> bool:
    allowed_ips = get_list_values(db, "relay_allowed_ips")
    return ip_matches_list(ip, allowed_ips)


def is_local_recipient_domain(db: Session, recipient: str) -> bool:
    if "@" not in recipient:
        return False

    domain = recipient.rsplit("@", 1)[1].lower()
    local_domains = get_list_values(db, "local_domains")
    return domain in local_domains
