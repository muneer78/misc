SELECT
    e.employee_id,
    e.name,
    COALESCE(s.salary, 0) AS salary
FROM
    employees e
LEFT JOIN
    salaries s
ON
    e.employee_id = s.employee_id;
