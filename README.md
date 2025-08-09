# 🌀 AWS Spot Price Fetcher

A lightweight Python script to query the **latest AWS EC2 spot prices** for a given instance type across all supported regions and availability zones. Designed for DevOps engineers, cloud practitioners, and cost-conscious builders who want real-time visibility into spot pricing trends.

---

## 🔧 Features

- Queries AWS EC2 Spot Price History using `boto3`
- Filters for the **lowest price per Availability Zone** in the past 24 hours
- Supports any EC2 instance type (e.g. `t3a.medium`, `m5.large`, etc.)
- Parallel region querying via `ThreadPoolExecutor`
- Outputs a clean, tabular summary using `tabulate`

---

## 📦 Requirements

Make sure you have the following installed:

- Python 3.9+
- AWS CLI configured with valid credentials
- Python packages:
  ```bash
  pip install boto3 tabulate
