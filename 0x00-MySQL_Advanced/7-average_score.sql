-- Compute and store the average student score
-- Change the delimiter to define the procedure
DELIMITER $$

-- Create the procedure
CREATE PROCEDURE ComputeAverageScoreForUser (IN user_id INT)
BEGIN
    DECLARE total_score FLOAT DEFAULT 0;
    DECLARE project_count INT DEFAULT 0;
    DECLARE avg_score FLOAT DEFAULT 0;

    -- Calculate the total score and the number of projects for the user
    SELECT IFNULL(SUM(score), 0), COUNT(*)
    INTO total_score, project_count
    FROM corrections
    WHERE corrections.user_id = user_id;

    -- Calculate the average score
    IF project_count > 0 THEN
        SET avg_score = total_score / project_count;
    ELSE
        SET avg_score = 0;
    END IF;

    -- Update the user's average score
    UPDATE users
    SET average_score = avg_score
    WHERE id = user_id;
END $$

-- Reset the delimiter
DELIMITER ;
