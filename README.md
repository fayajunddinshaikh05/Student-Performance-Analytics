# Student-Performance-Analytics
Analyzing student data using SQL, Power BI and AI recommendations


-- Student Performance Analytics
-- SQL Queries


-- 1. View Complete Dataset
SELECT *
FROM student_performance;


-- 2. Low Performing Students

SELECT 
    student_name,
    course,
    avg_grade,
    attendance_pct,
    risk_tier
FROM student_performance
WHERE avg_grade < 50
   OR attendance_pct < 70
ORDER BY avg_grade ASC;



-- 3. Risk Summary

SELECT 
    risk_tier,
    COUNT(*) AS total_students,
    ROUND(AVG(avg_grade), 1) AS avg_grade,
    ROUND(AVG(attendance_pct), 1) AS avg_attendance
FROM student_performance
GROUP BY risk_tier
ORDER BY avg_grade ASC;



-- 4. Risk Scoring

SELECT 
    student_name,
    avg_grade,
    attendance_pct,
    CASE
        WHEN avg_grade < 40 THEN 'High Risk'
        WHEN avg_grade < 55 THEN 'Moderate Risk'
        ELSE 'On Track'
    END AS risk_tier
FROM student_performance
ORDER BY avg_grade ASC;



-- 5. Risk Score Calculation

SELECT 
    student_id,
    student_name,
    (
        grade_score * 0.5 +
        attendance_score * 0.3 +
        submission_score * 0.2
    ) AS risk_score
FROM student_performance;



-- 6. Student Risk Classification

SELECT
    student_id,
    student_name,
    course,
    CASE
        WHEN risk_score < 40 THEN 'High Risk'
        WHEN risk_score < 65 THEN 'Moderate Risk'
        WHEN risk_score < 80 THEN 'Needs Monitoring'
        ELSE 'On Track'
    END AS risk_category
FROM student_performance;



-- 7. Dual Risk Students

SELECT *,
       CASE
           WHEN grade_score < 40
            AND attendance_score < 60
           THEN 1
           ELSE 0
       END AS dual_risk_flag
FROM student_performance
WHERE grade_score < 40
  AND attendance_score < 60;


-- 8. Good Performing Students

SELECT *
FROM student_performance
WHERE attendance_pct > 75
  AND avg_grade > 70;



-- 9. Course-wise Performance Summary

SELECT
    course,
    COUNT(*) AS total_students,
    ROUND(AVG(avg_grade), 1) AS avg_grade,
    ROUND(AVG(attendance_pct), 1) AS avg_attendance,
    ROUND(AVG(submission_pct), 1) AS avg_submission,
    SUM(
        CASE
            WHEN risk_tier = 'High Risk'
            THEN 1
            ELSE 0
        END
    ) AS high_risk_count
FROM student_performance
GROUP BY course
ORDER BY avg_grade DESC;


-- 10. Student Support Recommendations

SELECT
    student_id,
    student_name,
    course,
    class,
    avg_grade,
    attendance_pct,
    risk_score,
    risk_tier,

    CASE
        WHEN risk_tier = 'High Risk'
        THEN 'Immediate advisor support required'

        WHEN risk_tier = 'Moderate Risk'
        THEN 'Weekly academic monitoring required'

        WHEN risk_tier = 'Needs Monitoring'
        THEN 'Progress review in next assessment'

        ELSE 'No action required'
    END AS priority_action

FROM student_performance
WHERE risk_tier != 'On Track'
ORDER BY risk_score ASC;



-- 11. Course Ranking

SELECT
    student_name,
    course,
    avg_grade,

    RANK() OVER (
        PARTITION BY course
        ORDER BY avg_grade DESC
    ) AS rank_in_course

FROM student_performance;
