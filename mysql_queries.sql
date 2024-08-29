INSERT IGNORE INTO nsdl_details_join 
(isin, type, issuer_details, coupon_details, redemption_details, listing_details, updated_date)
SELECT 
    isin, type, issuer_details, coupon_details, redemption_details, listing_details, updated_date
FROM mmm;

SELECT COUNT(d.isin) AS total_isin_in_details,
       COUNT(j.isin) AS total_isin_in_join
FROM nsdl_details d
LEFT JOIN nsdl_details_join j ON d.isin = j.isin;


SELECT nsr.* FROM nsdl_securities_report nsr
LEFT JOIN nsdl_instrument_details nid ON nsr.isin = nid.isin
WHERE nid.isin IS null

SELECT 
    isin,
    COUNT(*) as duplicate_count
FROM 
    nsdl_securities_report
GROUP BY 
    isin
HAVING 
    COUNT(*) > 1;

UPDATE nsdl_instrument_details AS nid
JOIN nsdl_details AS nd
ON nid.isin = nd.isin
SET nid.coupon_details = nd.coupon_details,
    nid.redemption_details = nd.redemption_details,
    nid.listing_details = nd.listing_details;

   
INSERT INTO nsdl_instrument_details (isin, coupon_details, redemption_details, listing_details)
SELECT isin, coupon_details, redemption_details, listing_details
FROM nsdl_details
ON DUPLICATE KEY UPDATE
  coupon_details = VALUES(coupon_details),
  redemption_details = VALUES(redemption_details),
  listing_details = VALUES(listing_details);
