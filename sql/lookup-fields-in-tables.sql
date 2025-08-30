-- title: Ref-TableLookup
SELECT table_schema,
       table_name,
       column_name,
       data_type
FROM information_schema.columns
WHERE column_name ILIKE '%cred%'
	and table_name ilike '%cadence%'
--	AND table_schema = 'crm'
ORDER BY table_schema asc;