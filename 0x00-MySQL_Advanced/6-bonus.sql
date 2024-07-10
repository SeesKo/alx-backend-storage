-- Adds a new correction for a student with a stored procedure
DELIMITER $$
CREATE PROCEDURE AddBonus(
    IN user_id INT,
    IN project_name VARCHAR(255),
    IN score INT
)
BEGIN
    DECLARE project_id INT;

    -- Check if project_name exists, create if not
    SELECT id INTO project_id FROM projects WHERE name = project_name;
    
    IF project_id IS NULL THEN
        INSERT INTO projects (name) VALUES (project_name);
        SET project_id = LAST_INSERT_ID();
    END IF;

    -- Add or update score for the user and project
    INSERT INTO corrections (user_id, project_id, score)
    VALUES (user_id, project_id, score)
    ON DUPLICATE KEY UPDATE score = score + VALUES(score);
END $$
DELIMITER ;
