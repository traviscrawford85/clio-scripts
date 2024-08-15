import csv
import os
import sys
import requests
import json

# Set the API key and base URL
CLIO_API_KEY = os.getenv('CLIO_API_KEY')
if not CLIO_API_KEY:
    sys.exit("Error: CLIO_API_KEY environment variable not set.")

CLIO_BASE_URL_MANAGE = 'https://app.clio.com/api/v4/'
CLIO_BASE_URL_GROW = 'https://app.grow.clio.com/api/v4/'
HEADERS = {
    'Authorization': f'Bearer {CLIO_API_KEY}',
    'Content-Type': 'application/json'
}

# Set the output file name
OUTPUT_FILE = 'clio_custom_fields_audit.csv'

def fetch_data(endpoint, system='manage'):
    """Fetch data from Clio API."""
    base_url = CLIO_BASE_URL_MANAGE if system == 'manage' else CLIO_BASE_URL_GROW
    url = f"{base_url}{endpoint}"
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        sys.exit(f"API request failed: {e}")

def get_custom_fields(system='manage'):
    """Get custom fields from Clio Manage or Grow."""
    return fetch_data('custom_fields', system)

def get_field_sets(system='manage'):
    """Get field sets from Clio Manage or Grow."""
    return fetch_data('field_sets', system)

def compare_data(manage_data, grow_data):
    """Compare data between Clio Manage and Clio Grow."""
    manage_set = {item['name']: item for item in manage_data['data']}
    grow_set = {item['name']: item for item in grow_data['data']}
    
    mismatches = {}
    for name, manage_item in manage_set.items():
        grow_item = grow_set.get(name)
        if not grow_item or manage_item != grow_item:
            mismatches[name] = {
                'manage': manage_item,
                'grow': grow_item
            }
    return mismatches

def write_csv_output(mismatches):
    """Write mismatches to a CSV file."""
    with open(OUTPUT_FILE, 'w', newline='') as csvfile:
        fieldnames = ['name', 'manage', 'grow']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for name, fields in mismatches.items():
            writer.writerow({
                'name': name,
                'manage': json.dumps(fields['manage'], ensure_ascii=False),
                'grow': json.dumps(fields['grow'], ensure_ascii=False)
            })

def save_json(data, filename):
    """Save data to a JSON file."""
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

# Example usage
def main():
    # Fetch data
    fields_manage = get_cust
