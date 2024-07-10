-- Compute and store the average student score
DELIMITER $$

-- Create the procedure
CREATE PROCEDURE ComputeAverageScoreForUser (IN user_id INT)
BEGIN
    DECLARE avg_score FLOAT DEFAULT 0;

    -- Calculate the average score for the user
    SELECT IFNULL(AVG(score), 0)
    INTO avg_score
    FROM corrections
    WHERE corrections.user_id = user_id;

    -- Update the user's average score
    UPDATE users
    SET average_score = avg_score
    WHERE id = user_id;
END $$

DELIMITER ;
