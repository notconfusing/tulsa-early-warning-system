--RSA-logs, the reading sufficiency act, the logs of.
BEGIN;
DROP TABLE IF EXISTS clean_data.rsa_logs;
CREATE TABLE clean_data.rsa_logs AS
SELECT
	schoolid,
	studentid,
	student_number,
	subtype,
	entry_date,
	discipline_incidentdate
FROM
    raw_data.rsa_logs_rsa_logs_for_u_of_c;
COMMIT;
