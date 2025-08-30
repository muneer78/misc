-- DS4660

SELECT
	rl.createddate::date,
	count(*),
	rc."name" AS source_campaign,
	ru."name" AS creator_user,
	ru.username 
FROM
	crm.rpl_lead rl
JOIN crm.rpl_campaign rc ON
	rl.source_campaign__c = rc.id
JOIN crm.rpl_user ru ON
	rl.createdbyid = ru.id
WHERE
	rl.isdeleted = 0
	AND rl.createddate > '2024-04-30'
	AND rc."name" LIKE '%FMCSA%'
GROUP BY
	rc."name",
	rl.createddate::date ,
	ru."name",
	ru.username 
ORDER BY
	rl.createddate::date desc