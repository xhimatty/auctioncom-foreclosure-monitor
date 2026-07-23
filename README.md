# Auction.com Foreclosure Monitoring System

Automatically extracts real-time active foreclosure listings from Auction.com and exports the results to a structured CSV file daily for monitoring.

## Table of Contents

* [Overview](#overview)

* [Why This Project?](#why-this-project)

* [Features](#features)

* [How It Works](#how-it-works)

* [Result](#result)

* [Sample Output](#sample-output)

* [Structure](#structure)

* [Tech Stack](#tech-stack)

* [GitHub Actions](#github-actions)

* [Notes](#notes)


## Overview

Auction.com updates foreclosure listings constantly as auctions are scheduled, removed, postponed, canceled, or sold. To track these changes reliably without relying on the overhead and fragility of browser automation and HTML parsing, the system analyses network traffic to identify the direct API endpoints used by the website, extracts the listing records directly, and exports daily structured CSV files for continuous monitoring and status tracking.

## Why This Project?

Checking foreclosure listings manually quickly becomes repetitive, especially when new listings appear and existing ones change status, often leading to missed opportunities.

This system automates that process by scraping listing information and exporting it into a usable format that can be searched, filtered, or compared between runs.

## Features

* Collects top active foreclosure listings from Auction.com's website.

* Avoids relying on brittle browser automation and fragile CSS selectors.

* Exports structured listing data to CSV.

* Masks sensitive listing information before export.

* Records scraper activity in a log file.

* Supports scheduled execution with GitHub Actions.

## How It Works

|Step|Description|
|:----|:----|
|Request|Sends a request to the Auction.com API Endpoint|
|Parse|Extracts the listing data from the JSON response.|
|Process|Cleans and prepares the extracted data.|
|Export|Writes the final dataset to a CSV file.|


## Result

|Field|Description|
|:----|:----|
|`listing_id_masked`|Masked listing identifier|
|`status`| Listing status|
|`status_group`|Status category|
|`auction_start_date`|Auction start date|
|`auction_start_time`|Auction start time|
|`auction_end` |Auction end date and time|
|`starting_bid`|Opening bid|
|`address_anonymized`|Street address with house number masked|
|`city_state`|City, state and county|
|`bedrooms`|Number of bedrooms|
|`bathrooms`           | Number of bathrooms|
|`sqft`                | Living area (sq ft)|
|`lot_size`            | Lot size|
|`year_built`          | Year built|
|`structure_type`      | Property type|
|`seller_value`        | Seller valuation|
|`rental_estimate`     | Estimated monthly rent|
|`composite_estimate`  | Estimated property value|
|`deposit_requirement`|Required auction deposit|
|`current_highest_bid`|Current highest bid (when available)|
|`is_hot`|Popular listing indicator|
|`photo`|Property image|
|`product_type`|Product type|
|`asset_type`| Asset category|
|`occupancy_status`|Occupancy status|
|`venue_type`| Auction venue|
|`marketing_tags`|Listing tags|
|`link_masked`|Masked property URL|
|`scraped_at`|Date the data was collected|

## Sample Output

```csv

listing_id_masked,status,status_group,auction_start_date,auction_start_time,auction_end,starting_bid,address_anonymized,city_state,bedrooms,bathrooms,sqft,lot_size,year_built,structure_type,seller_value,rental_estimate,composite_estimate,deposit_requirement,current_highest_bid,is_hot,photo,product_type,asset_type,occupancy_status,venue_type,marketing_tags,link_masked,scraped_at

*****33,SALE_PENDING,ACTIVE,2026-07-23,17:00:00,,623200.0,XXXX N 43rd Pl,"Phoenix, AZ 85050, Maricopa County",3,2.0,2151,0.15,1996,SINGLE_FAMILY_HOME,735700.0,3618.0,734552.0,$10000,,,Available in full report,TRUSTEE,FORECLOSURE,OCCUPIED,LIVE,GOTO,https://www.********************,2026-07-22

```

## Structure

```text

AZ Foreclosure/

│

├── .github/

│   └── workflows/

│       └── az.yml

├── az.py

├── requirements.txt

├── .env

├── README.md

└── az_data.log

```

## Tech Stack

```
Python
Requests
Github Actions
```

## GitHub Actions

The repository includes a GitHub Actions workflow that:

* Checks out the repository.

* Installs the project dependencies.

* Loads repository secrets.

* Runs the scraper.

* Uploads the generated CSV.

* Uploads the scraper log.


Repository secrets required:

| Secret| Description|
|:----| :----|
|`COOKIES`|Auction.com session cookies|
|`HEADERS`|Request headers|


## Notes

>[!NOTE]
>Available fields may vary depending on the listing.

>[!IMPORTANT]
> The available CSV is only a sample and sensitive information has been intentionally anonymized or omitted.
