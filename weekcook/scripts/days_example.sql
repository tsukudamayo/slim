SELECT
	generate.days,
	sum(customer)
FROM
(
	SELECT
		date('2010-12-1') + a::int as days
	FROM
		generate_series(0, 4) as a
) as generate

LEFT OUTER JOIN
     customer
ON (generate.days = customer.days)
GROUP BY generate.days
ORDER BY generate.days;
