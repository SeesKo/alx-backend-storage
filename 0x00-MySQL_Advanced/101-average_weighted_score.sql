-- Compute and store the average weighted score for all students
DELIMITER $$
-- Create procedure
CREATE PROCEDURE ComputeAverageWeightedScoreForUsers ()
BEGIN
    DECLARE done INT DEFAULT 0;
    DECLARE user_id INT;
    DECLARE total_weighted_score FLOAT;
    DECLARE total_weight FLOAT;

    -- Cursor to iterate over each user
    DECLARE user_cursor CURSOR FOR 
        SELECT id FROM users;
    
    -- Error handling
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = 1;

    -- Open cursor
    OPEN user_cursor;

    -- Loop through each user
    user_loop: LOOP
        FETCH user_cursor INTO user_id;
        IF done = 1 THEN
            LEAVE user_loop;
        END IF;

        -- Initialize variables
        SET total_weighted_score = 0;
        SET total_weight = 0;

        -- Calculate weighted average score for the user
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
    END LOOP;

    -- Close cursor
    CLOSE user_cursor;
END $$
-- Reset delimiter
DELIMITER ;
