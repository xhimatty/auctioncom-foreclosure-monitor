import requests
import json
from urllib.parse import urljoin
from datetime import datetime
import pandas as pd
import os
from dotenv import load_dotenv
import logging

load_dotenv()


logging.basicConfig(
    filename="az_data.log",
    filemode="a",
    level=logging.DEBUG,
    format="%(asctime)s | %(levelname)s | %(filename)s:%(lineno)d | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)



session = requests.Session()

COOKIES = json.loads(os.getenv("cookies", "{}"))
HEADERS = json.loads(os.getenv("headers", "{}"))

session.cookies.update(COOKIES)
session.headers.update(HEADERS)

json_data = {
    'query': '\n        \n      fragment ListingCardFields on Listing {\n        __typename\n        listing_id\n        urn\n        listing_status_group\n        listing_status\n        listing_status_label(intent: SEARCH)\n        primary_photo\n        primary_property_id\n        listing_photos_count\n        listing_page_path\n        reserve_price @include(if: $hasAuthenticatedUser)\n        is_hot\n        formatted_address(format: DOUBLE_LINE)\n\n        listing_configuration {\n          product_type\n          is_reserve_displayed\n          is_reserve_price_available\n          broker_commission\n          financing_available\n          buyer_premium_available\n          interior_access_allowed\n          occupancy_status\n          asset_type\n          is_first_look_enabled\n          is_direct_offer_enabled\n          is_third_party_online\n        }\n\n        attribution_source {\n          origin_code\n        }\n\n        external_identifiers {\n          data_source\n          external_identifier\n        }\n\n        venue {\n          venue_type\n        }\n\n        event {\n          event_code\n          trustee_sale\n        }\n\n        valuation {\n          seller_current_value_amount\n        }\n\n        strategy {\n          selling_method_attributes {\n            online_segment_type\n          }\n        }\n\n        seller_property {\n          street_description\n          municipality\n          country_primary_subdivision\n          country_secondary_subdivision\n          postal_code\n        }\n\n        program_configuration {\n          program_enrollment_code\n        }\n\n        seller_terms {\n          inspection_terms {\n            is_option_contingency\n            is_contingency\n          }\n          leaseback_terms {\n            leaseback_period_in_days\n            leaseback_period_rent\n          }\n          finance_terms {\n            finance_preference\n            is_contingency\n          }\n          intent\n        }\n\n        primary_property {\n          property_id\n          summary {\n            total_bedrooms\n            total_bathrooms\n            square_footage\n            lot_size\n            year_built\n            valuation\n            structure_type_code\n            structure_type_group\n            address {\n              coordinates {\n                lon\n                lat\n              }\n            }\n          }\n          is_currently_saved @include(if: $hasAuthenticatedUser)\n          is_newly_listed\n          current_user_tracking_state {\n            is_seen\n            is_updated\n          }\n        }\n\n        auction {\n          start_date\n          end_date\n          starting_bid\n          is_online\n          visible_auction_start_date_time\n          bid_instruction {\n            nos_amount\n          }\n        }\n\n        marketing_tags {\n          tag\n        }\n\n        open_houses {\n          local_date\n          start_time\n          end_time\n        }\n\n        listing_summary {\n          is_remote_bid_enabled\n          is_remote_before_and_during_auction_enabled\n          show_opening_bid\n        }\n\n        external_information(resolvePolicy: CACHE_ONLY) {\n          collateral {\n            summary {\n              estimated\n              low\n              high\n              type\n            }\n          }\n        }\n\n        selling_method(resolvePolicy: CACHE_ONLY) {\n          __typename\n          ... on OnlineAuctionSegment {\n            _alias_OnlineAuctionSegment__starting_bid_amount: starting_bid_amount\n\n            _alias_OnlineAuctionSegment__configuration: configuration {\n              is_match_bidding_enabled\n              is_registration_deposit_required_enabled\n              bid_again_count\n              should_bid_again\n            }\n            listing_id\n            __typename\n            start_date\n            segment_type\n            initial_end_date\n            current_time\n            reserve_status\n            starting_bid_amount\n            subject_to_status\n            current_highest_bid {\n              bid_id\n              updated_date\n              bid_amount\n              type\n              terms {\n                status\n              }\n            }\n            segment_status\n            current_increment_amount\n            bid_count\n            result {\n              winning_bid_amount\n            }\n          }\n          ... on LiveAuctionSegment {\n            _alias_LiveAuctionSegment__starting_bid_amount: starting_bid_amount\n\n            _alias_LiveAuctionSegment__configuration: configuration {\n              state_deposit_rule\n            }\n            current_highest_bid {\n              bid_amount\n            }\n          }\n        }\n      }\n     \n        query resiSearch_blueprint_seekListingsFromFilters(\n          $filters: ListingCompatabilityFilters!,\n          $aggregationFields: [String!]!,\n          $hasAuthenticatedUser: Boolean!,\n          $requiresAggregation: Boolean!\n        ) {\n          seek_listings_from_filters(filters: $filters) {\n            total_count\n            total_pages\n            size\n            current_page\n            aggregation(fields: $aggregationFields) @include(if: $requiresAggregation)\n            derived_signals {\n              recognized_locations {\n                urn\n                label\n                location_type\n              }\n            }\n            content {\n              ...ListingCardFields\n            }\n          }\n        }\n      ',
    'variables': {
        'filters': {
            'property_state': 'AZ',
            'property_city': 'Phoenix',
            'geo_location': '33.4483771,-112.0740373',
            'listing_type': 'active',
            'sort': 'auction_date_order',
            'limit': 500,
            'marketing_tags': 'goto',
            'nearby_search': 'y',
            'nearby_search_radius': 50,
            'usecode_product_type': 'resi_ft',
            'version': 1,
            'offset': 0,
        },
        'hasAuthenticatedUser': False,
        'aggregationFields': [
            'primary_property_summary.structure_type_code.keyword',
            'listing_summary.is_remote_bid_enabled',
            'seller_property.municipality.keyword',
        ],
        'requiresAggregation': True,
    },
}

def fetch_data():
    response = session.post('https://graph.auction.com/graphql', json=json_data)

    if response.status_code == 200:
        logging.info(f'Request OK: {response.status_code}')
        return response
    else:
        logging.error(f'Request failed: {response.status_code}')
        return None
    # print(response.json())


def top_foreclosure(response):
    jd = response.json()
    listings = jd["data"]["seek_listings_from_filters"]["content"]

    if not listings:
        logging.error('No listings found')
        return []

    items = []

    for auction in listings:
        listing_id = auction.get("listing_id", "")
        status = auction.get("listing_status", "")
        status_group = auction.get("listing_status_group", "")

        auction_start = auction.get("auction", {}).get("start_date", "")
        auction_end = auction.get("auction", {}).get("end_date", "")
        is_online = auction.get("auction", {}).get("is_online", "")
        starting_bid = auction.get("auction", {}).get("starting_bid", "")

        address = auction.get("formatted_address", [""])[0]
        city_state = auction.get("formatted_address", ["", ""])[1]
        summary = auction.get("primary_property", {}).get("summary", {})
        bedrooms = summary.get("total_bedrooms", "")
        bathrooms = summary.get("total_bathrooms", "")
        sqft = summary.get("square_footage", "")
        lot_size = summary.get("lot_size", "")
        year_built = summary.get("year_built", "")
        structure_type = summary.get("structure_type_code", "")

        seller_value = auction.get("valuation", {}).get("seller_current_value_amount", "")

        # collateral is a list of dicts tagged by "type" (rental / composite) - pull each out by type
        collateral_summary = ((auction.get("external_information") or {}).get("collateral") or {}).get("summary", [])
        rental_estimate = next((c.get("estimated", "") for c in collateral_summary if c.get("type") == "rental"), "")
        composite_estimate = next((c.get("estimated", "") for c in collateral_summary if c.get("type") == "composite"), "")

        selling_method = auction.get("selling_method", {})
        deposit_requirement = selling_method.get("_alias_LiveAuctionSegment__configuration", {}).get("state_deposit_rule", "")
        current_highest_bid = selling_method.get("current_highest_bid", "")

        latitude = summary.get("address", {}).get("coordinates", {}).get("lat", "")
        longitude = summary.get("address", {}).get("coordinates", {}).get("lon", "")

        is_hot = auction.get("is_hot", "")
        
        photo = auction.get("primary_photo", "")

        product_type = auction.get("listing_configuration", {}).get("product_type", "")
        asset_type = auction.get("listing_configuration", {}).get("asset_type", "")
        occupancy_status = auction.get("listing_configuration", {}).get("occupancy_status", "")

        
        venue_type = auction.get("venue", {}).get("venue_type", "")

        marketing_tags = ", ".join(t.get("tag", "") for t in (auction.get("marketing_tags") or []))

        link = urljoin("https://www.auction.com", auction.get("listing_page_path", ""))

        items.append({
            "listing_id": listing_id,
            "status": status,
            "status_group": status_group,
            "auction_start": auction_start,
            "auction_end": auction_end,
            "is_online": is_online,
            "starting_bid": starting_bid,
            "address": address,
            "city_state": city_state,
            "bedrooms": bedrooms,
            "bathrooms": bathrooms,
            "sqft": sqft,
            "lot_size": lot_size,
            "year_built": year_built,
            "structure_type": structure_type,
            "seller_value": seller_value,
            "rental_estimate": rental_estimate,
            "composite_estimate": composite_estimate,
            "deposit_requirement": deposit_requirement,
            "current_highest_bid": current_highest_bid,
            "latitude": latitude,
            "longitude": longitude,
            "is_hot": is_hot,
            "photo": photo,
            "product_type": product_type,
            "asset_type": asset_type,
            "occupancy_status": occupancy_status,
            "venue_type": venue_type,
            "marketing_tags": marketing_tags,
            "link": link,
            "scraped_at": datetime.now().strftime('%Y-%m-%d'),
        })
        
    return items

def process_and_save_csv(get_data):
    if not get_data:
        logging.error('No data found')
        raise SystemExit(1)
    
    df = pd.DataFrame(get_data)
    df["listing_id_masked"] = "*****" + df["listing_id"].astype(str).str[-2:]
    df["auction_start"] = pd.to_datetime(
    df["auction_start"], errors="coerce").dt.strftime("%Y-%m-%d")
    df["address_anonymized"] = (df["address"].fillna("").astype(str).str.replace(r"^\d+", "XXXX", regex=True))
    df["link_masked"] = df['link'].str[:12] + "********************"
    df['photo'] = "Available in full report"

    df = df.drop(columns=["latitude", "longitude", "listing_id", "link", "is_online"])

    new_order = [
    'listing_id_masked', 'status', 'status_group', 'auction_start', 
    'auction_end', 'starting_bid', 'address_anonymized', 
    'city_state', 'bedrooms', 'bathrooms', 'sqft', 'lot_size', 
    'year_built', 'structure_type', 'seller_value', 'rental_estimate', 
    'composite_estimate', 'deposit_requirement', 'current_highest_bid', 
    'is_hot', 'photo', 'product_type', 'asset_type', 'occupancy_status', 
    'venue_type', 'marketing_tags', 'link_masked', 'scraped_at'
    ]

    df = df[new_order]

    df.to_csv('az_top_foreclosure.csv', index=False)

if __name__ == '__main__':
    response = fetch_data()
    if response is None:
        logging.error('Aborting: no valid response from Auction.com')
        raise SystemExit(1)

    logging.info('Getting the data...')
    get_data = top_foreclosure(response)

    logging.info('Saving to CSV...')
    process_and_save_csv(get_data)
    logging.info('Successfully saved to CSV!')
