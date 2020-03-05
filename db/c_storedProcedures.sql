use platform;

DELIMITER //
CREATE PROCEDURE get_user(IN user_name varchar(50), IN user_pass varchar(50))
BEGIN
  	SELECT u.userEmail, u.userDescription
  	FROM users u
  	WHERE u.userName = user_name and u.userPass = sha2(user_pass, 224);
END//
DELIMITER ;

DELIMITER //
CREATE PROCEDURE insert_user(IN user_name varchar(50), IN user_email varchar(50), 
							IN user_pass varchar(50))
BEGIN
	DECLARE old_user_name varchar(50);
	DECLARE ok_response INT default 0;

  	SET old_user_name = (SELECT userName FROM users
					  	WHERE userName = user_name or userEmail = user_email);

	IF old_user_name IS NULL
	THEN	
		SET ok_response = 1;
		START TRANSACTION;
		INSERT INTO users(userName, userEmail, userPass)
		VALUES(user_name, user_email, sha2(user_pass, 224));
		COMMIT;
	END IF;

	SELECT ok_response;

END//
DELIMITER ;