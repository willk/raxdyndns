import sys
import socket
import urllib2
import argparse
import pyrax
import pyrax.exceptions as rax_except


def update_record(domain_name, record_name, address, configuration):
    pyrax.set_setting('identity_type', 'rackspace')
    pyrax.set_credential_file('config.ini')
    dns = pyrax.cloud_dns

    try:
        dom = dns.find(name=domain_name)
    except rax_except.NotFound:
        print('Domain %s not found.' % domain_name)
        sys.exit()

    try:
        rec = dom.find_record('A', record_name)
    except rax_except.NotFound:
        print('Record %s not found' % record_name)
        sys.exit()

    rec.update(data=address)


def check_dns(record_name=None):
    current_address = urllib2.urlopen('http://icanhazip.com').read().rstrip()
    record_address = socket.gethostbyname(record_name)

    if current_address == record_address:
        return None
    else:
        return current_address


def main(domain_name, record_name, configuration):
    address = check_dns(record_name)

    if address:
        update_record(domain_name, record_name, address, configuration)

if __name__ == '__main__':
    parse = argparse.ArgumentParser(description='DynDNS for Rackspace CloudDNS')
    parse.add_argument('--domain', dest='domain_name', required=True,
                       help='Domain domain_namee that record is under. ex: example.com')
    parse.add_argument('--record', dest='record_name', required=True,
                       help='Record for the update. ex: sub.example.com')
    parse.add_argument('--config', dest='configuration', required=False,
                       help='Configuration file.')
    args = parse.parse_args()

    if args.configuration:
        configuration = args.configuration
    else:
        configuration = 'config.ini'

    main(args.domain_name, args.record_name, configuration)
