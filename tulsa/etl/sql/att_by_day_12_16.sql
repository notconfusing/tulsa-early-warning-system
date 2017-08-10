DROP TABLE IF EXISTS clean_data.att_by_day_12_16;
CREATE TABLE clean_data.att_by_day_12_16 AS
SELECT
    schoolid AS school_id,
    studentid,
    "1state_studentnumber" AS state_studentnumber,
    TO_DATE(att_date, 'MM/DD/YYYY') AS att_date,
    CASE "156att_code" 
        WHEN 'A' THEN 'absent'
        WHEN 'B' THEN 'truancy'
        WHEN 'C' THEN 'counselor'
        WHEN 'D' THEN 'administrator'
        WHEN 'E' THEN 'excused'
        WHEN 'HDA' THEN 'half day absent'
        WHEN 'I' THEN 'in-school suspension'
        WHEN 'L' THEN 'leaves early'
        WHEN 'N' THEN 'nurse'
        WHEN 'R' THEN 'school activity'
        WHEN 'T' THEN 'tardy'
        WHEN 'U' THEN 'unexcused'
        WHEN 'W' THEN 'with explanation'
        ELSE 'other'
    END AS att_code,
    CASE "138name"
        WHEN 'AM ATT' THEN 'AM'
        WHEN 'AM Attendance' THEN 'AM'
        WHEN 'Morning Attendance' THEN 'AM'
        WHEN 'AM' THEN 'AM'
        WHEN 'PM ATT' THEN 'PM'
        WHEN 'PM Attendance' THEN 'PM'
        WHEN 'Afternoon Attendance' THEN 'PM'
        WHEN 'PM' THEN 'PM'
    END AS att_name
FROM
    raw_data.att_by_day_12_16;