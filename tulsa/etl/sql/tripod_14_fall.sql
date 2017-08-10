-- raw_data.tripod_accountability_14_fall_sheet1
BEGIN;
DROP TABLE IF EXISTS clean_data.tripod_14_fall;
CREATE TABLE clean_data.tripod_14_fall AS

WITH grade_count AS
(
    SELECT teachernumber, COUNT(DISTINCT grade_level) AS num_classes
    FROM clean_data.roster_14_fall 
    WHERE grade_level <= 4
    GROUP BY teachernumber
),
teacher_grade AS 
(
    SELECT DISTINCT teachernumber, grade_level
    FROM clean_data.roster_14_fall
    WHERE grade_level <= 4
),
roster AS
(
    SELECT
        teachernumber,
        num_classes,
        grade_level
    FROM
        grade_count
        INNER JOIN teacher_grade
            USING (teachernumber)
)

SELECT
    raw."year" AS yr,
    raw.season,
    raw.schoolid_da AS school_id,
    raw.school_name,
    raw.teacherid_da AS teacher_id,
    raw.teacher_name,
    CAST(NULL AS NUMERIC) AS class_id,
    CASE 
        WHEN roster.num_classes > 1 THEN -100
        WHEN roster.num_classes = 1 THEN roster.num_classes
    END AS grade,
    raw.responded AS responses,
    raw."Challenges_sajNCE" AS challenge,
    raw."Controls_sajNCE" AS classroom_management,
    raw."Captivates_sajNCE" AS captivate,
    raw."Cares_sajNCE" AS care,
    raw."Clarifies_sajNCE" AS clarify,
    raw."Consolidates_sajNCE" AS consolidate,
    raw."Confers_sajNCE" AS confer,
    raw."sevenCs_sajNCE" AS cs
FROM
    raw_data.tripod_accountability_14_fall_sheet1 AS raw
    LEFT JOIN roster
        ON raw.teacherid_da = roster.teachernumber;
COMMIT;