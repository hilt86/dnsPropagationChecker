import requests
import csv
import dns.resolver
import argparse

# Function to download and parse CSV
# Function to download and parse CSV
def get_nameservers(url, country_code=None, city=None):
    response = requests.get(url)
    response.raise_for_status()  # Ensure the request was successful
    csv_data = response.content.decode('utf-8').splitlines()
    reader = csv.reader(csv_data)
    next(reader)  # Skip header row
    nameservers = [row for row in reader if row]
    print(f'Nameservers before filtering: {len(nameservers)}')  # Debug line
    if country_code:
        nameservers = [row for row in nameservers if row[4] == country_code]
    if city:
        nameservers = [row for row in nameservers if row[5] == city]
    print(f'Nameservers after filtering: {len(nameservers)}')  # Debug line
    return [row[0] for row in nameservers]


# Function to query nameservers
def query_nameservers(nameservers, domain):
    for nameserver in nameservers:
        resolver = dns.resolver.Resolver()
        resolver.nameservers = [nameserver]
        try:
            answers = resolver.resolve(domain)
            for rdata in answers:
                print(f'Nameserver: {nameserver}, Answer: {rdata}')
        except dns.resolver.NXDOMAIN:
            print(f'Domain {domain} does not exist on {nameserver}')
        except dns.resolver.Timeout:
            continue  # Omit timeout errors by continuing to the next iteration
        except dns.resolver.NoNameservers:
            print(f'No nameservers available for {nameserver}')

# Main program
def main():
    parser = argparse.ArgumentParser(description='Query nameservers for a specific domain.')
    parser.add_argument('--country_code', help='Country code to filter nameservers by')
    parser.add_argument('--city', help='City to filter nameservers by')
    parser.add_argument('domain', help='The domain to query')
    args = parser.parse_args()

    url = 'https://public-dns.info/nameservers-all.csv'
    nameservers = get_nameservers(url, args.country_code, args.city)
    query_nameservers(nameservers, args.domain)

if __name__ == '__main__':
    main()
