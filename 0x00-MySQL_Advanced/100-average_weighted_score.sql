-- Compute and store the average weighted score for a student
DELIMITER $$
-- Create procedure
CREATE PROCEDURE ComputeAverageWeightedScoreForUser (IN user_id INT)
BEGIN
    DECLARE total_weighted_score FLOAT DEFAULT 0;
    DECLARE total_weight FLOAT DEFAULT 0;
    
    -- Calculate weighted average score
    SELECT SUM(corrections.score * projects.weight) / SUM(projects.weight)
    INTO total_weighted_score
    FROM corrections
    JOIN projects ON corrections.project_id = projects.id
    WHERE corrections.user_id = user_id;
    
    -- Calculate total weight
    SELECT SUM(projects.weight)
    INTO total_weight
    FROM corrections
    JOIN projects ON corrections.project_id = projects.id
    WHERE corrections.user_id = user_id;
    
    -- Update average_score in users table
    UPDATE users
    SET average_score = IF(total_weight > 0, total_weighted_score, 0)
    WHERE id = user_id;
END $$
DELIMITER ;
