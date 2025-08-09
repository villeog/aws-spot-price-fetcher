import boto3
import argparse
from tabulate import tabulate
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta

def get_spot_instance_regions():
    """Retrieve AWS regions that support Spot Instances."""
    ec2_client = boto3.client("ec2", region_name="us-east-1")
    regions = [r["RegionName"] for r in ec2_client.describe_regions()["Regions"]]

    supported_regions = []
    for region in regions:
        try:
            ec2 = boto3.client("ec2", region_name=region)
            ec2.describe_spot_price_history(InstanceTypes=["t3.micro"], MaxResults=1)
            supported_regions.append(region)
        except Exception:
            pass  # Ignore regions where Spot Instances aren't available

    return supported_regions

def fetch_latest_spot_prices(region, instance_type):
    """Fetch the latest spot price for each Availability Zone."""
    try:
        ec2 = boto3.client("ec2", region_name=region)
        response = ec2.describe_spot_price_history(
            InstanceTypes=[instance_type],
            ProductDescriptions=["Linux/UNIX"],
            MaxResults=50,
            StartTime=datetime.utcnow() - timedelta(days=1)
        )

        latest_prices = {}
        for entry in response["SpotPriceHistory"]:
            key = entry["AvailabilityZone"]  # Use only Availability Zone as the key
            price = float(entry["SpotPrice"])
            timestamp = entry["Timestamp"]

            # Keep only the **lowest** price per AZ
            if key not in latest_prices or price < latest_prices[key][2]:
                latest_prices[key] = [entry["AvailabilityZone"], entry["InstanceType"], price, timestamp]

        return list(latest_prices.values())

    except Exception as e:
        print(f"Error fetching spot prices for {region}: {e}")
        return []

def main():
    parser = argparse.ArgumentParser(description="Fetch latest AWS Spot Instance prices.")
    parser.add_argument("--instance-type", required=True, help="AWS instance type (e.g., t3.micro, m5.large)")
    args = parser.parse_args()

    regions = get_spot_instance_regions()

    with ThreadPoolExecutor(max_workers=10) as executor:
        results = list(executor.map(lambda r: fetch_latest_spot_prices(r, args.instance_type), regions))

    spot_prices = sorted([item for sublist in results for item in sublist], key=lambda x: x[2])[:20]

    headers = ["Availability Zone", "Instance", "Price ($)", "Timestamp"]
    print("\nLatest Spot Price Per Unique Availability Zone:")
    print(tabulate(spot_prices, headers=headers, tablefmt="plain"))

if __name__ == "__main__":
    main()
