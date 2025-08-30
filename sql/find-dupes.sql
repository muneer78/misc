-- DS-5232

WITH lead_dupes AS (SELECT COUNT(*) AS lead_cnt, rl.dot_number__c 
FROM crm.rpl_lead rl
WHERE isdeleted = 0
GROUP BY rl.dot_number__c
HAVING COUNT(*) > 1)
SELECT ld.lead_cnt AS totalleads
	,rl.id 
	,rl."name" 
	,rl.dot_number__c 
	,rl.statecode 
	,rl.lastactivitydate 
	,rl.createddate 
	,rl.isconverted
FROM crm.rpl_lead rl 
INNER JOIN lead_dupes ld on rl.dot_number__c = ld.dot_number__c
WHERE isdeleted = 0
	AND isconverted = 0
--	AND rl.dot_number__c NOT LIKE '%.%'
--	AND rl.dot_number__c NOT LIKE '0'
--	AND rl.dot_number__c NOT LIKE '1'
--	AND rl.dot_number__c NOT ILIKE '%lease%'
--	AND rl.dot_number__c NOT ILIKE '%tbd%'
--	AND rl.dot_number__c NOT ILIKE '%agent%'
--	AND rl.dot_number__c NOT ILIKE '%n%'
--	AND rl.dot_number__c NOT LIKE '?'
ORDER BY totalleads DESC, rl.dot_number__c DESC