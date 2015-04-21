import argparse
from boto import route53

# Read https://support.google.com/a/answer/33915?hl=en
# AWS credentials should go into ~/.boto

parser = argparse.ArgumentParser()
parser.add_argument("--action", dest='action', help="Action - add or delete MX records", default='add')
parser.add_argument("--domain", dest='domain', help="DNS Zone")
parser.add_argument("--force-create", dest='force', type=bool, help="Force creation of missing zones", default=False)
parser.add_argument("--aws-region", dest='aws_region', help="AWS Region", default='eu-west-1')

args = parser.parse_args()

conn = route53.connect_to_region(args.aws_region)

dom = conn.get_zone(args.domain)

if not dom:
    if args.force is True and args.action == 'add':
        dom = conn.create_zone(args.domain)
        print("Forced creation of DNS zone %s" % args.domain)
    else:
        raise Exception("Domain does not exist. Create the zone first or use --force-create option")

if args.action == 'add':
    domain = "%s." % args.domain
    dom.add_record("MX", domain, "1 ASPMX.L.GOOGLE.COM")
    dom.add_record("MX", domain, "5 ALT1.ASPMX.L.GOOGLE.COM")
    dom.add_record("MX", domain, "5 ALT2.ASPMX.L.GOOGLE.COM")
    dom.add_record("MX", domain, "10 ALT3.ASPMX.L.GOOGLE.COM")
    dom.add_record("MX", domain, "10 ALT4.ASPMX.L.GOOGLE.COM")
    print("Added MX records for domain %s" % args.domain)

if args.action == 'delete':
    dom.delete_mx(all=True)
    print("Removed *ALL* MX records for domain %s" % args.domain)