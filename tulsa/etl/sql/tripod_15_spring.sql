-- raw_data.tripod_local_scores_15_spring_ee_class
-- raw_data.tripod_local_scores_15_spring_ue_class
BEGIN;
DROP TABLE IF EXISTS clean_data.tripod_15_spring;
CREATE TABLE clean_data.tripod_15_spring AS

WITH grade_count AS
(
    SELECT teachernumber, COUNT(DISTINCT grade_level) AS num_classes
    FROM clean_data.roster_15_spring 
    WHERE grade_level <= 4
    GROUP BY teachernumber
),
teacher_grade AS 
(
    SELECT DISTINCT teachernumber, grade_level
    FROM clean_data.roster_15_spring
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
    ee."year" AS yr,
    ee.season,
    ee.schoolid_da AS school_id,
    ee.school_name,
    ee.teacherid_da AS teacher_id,
    ee.teacher_name,
    CAST(NULL AS INT) AS class_id,
    CASE 
        WHEN roster.num_classes > 1 THEN -100
        WHEN roster.num_classes = 1 THEN roster.num_classes
    END AS grade,
    ee.responded AS responses,
    ee."Challenges_sajNCE" AS challenge,
    ee."Controls_sajNCE" AS classroom_management,
    ee."Captivates_sajNCE" AS captivate,
    ee."Cares_sajNCE" AS care,
    ee."Clarifies_sajNCE" AS clarify,
    ee."Consolidates_sajNCE" AS consolidate,
    ee."Confers_sajNCE" AS confer,
    ee."sevenCs_sajNCE" AS cs
FROM
    raw_data.tripod_local_scores_15_spring_ee_class AS ee
    LEFT JOIN roster
        ON ee.teacherid_da = roster.teachernumber


UNION


SELECT
    ue."year" AS yr,
    ue.season,
    ue.schoolid_da AS school_id,
    ue.school_name,
    ue.teacherid_da AS teacher_id,
    ue.teacher_name,
    CAST(NULL AS INT) AS class_id,
    CASE 
        WHEN roster.num_classes > 1 THEN -100
        WHEN roster.num_classes = 1 THEN roster.num_classes
    END AS grade,
    ue.responded AS responses,
    ue."Challenges_sajNCE" AS challenge,
    ue."Controls_sajNCE" AS classroom_management,
    ue."Captivates_sajNCE" AS captivate,
    ue."Cares_sajNCE" AS care,
    ue."Clarifies_sajNCE" AS clarify,
    ue."Consolidates_sajNCE" AS consolidate,
    ue."Confers_sajNCE" AS confer,
    ue."sevenCs_sajNCE" AS cs
FROM
    raw_data.tripod_local_scores_15_spring_ue_class AS ue
    LEFT JOIN roster
        ON ue.teacherid_da = roster.teachernumber;
COMMIT;