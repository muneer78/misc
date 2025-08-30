-- title: Ref-FieldLookup
SELECT column_name 
FROM pg_catalog.svv_columns 
WHERE table_name = 'dim_busunit_customer_alias'
ORDER BY column_name ASC

SELECT *
FROM shamrock_dimdw.dim_busunit_cust_alias_status dbcas 
LIMIT 100