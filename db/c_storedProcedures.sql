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

DELIMITER //
CREATE PROCEDURE insert_genre(IN name varchar(30), IN img_path varchar(100))
BEGIN
	DECLARE old_name varchar(30);
	DECLARE ok_response INT default 0;

  	SET old_name = (SELECT genreName FROM genres
					  	WHERE genreName = name);

	IF old_name IS NULL
	THEN	
		SET ok_response = 1;
		START TRANSACTION;
		INSERT INTO genres(genreName, genrePicturePath)
		VALUES(name, img_path);
		COMMIT;
	END IF;

	SELECT ok_response;

END//
DELIMITER ;


DELIMITER //
CREATE PROCEDURE insert_series(IN name varchar(70), IN description text,
								IN img_path varchar(100), IN genName varchar(30),
								IN episodes int)
BEGIN
	DECLARE old_name varchar(70);
	DECLARE genre_id int;
	DECLARE ok_response INT default 0;

  	SET old_name = (SELECT seriesName FROM series
					  	WHERE seriesName = name);
  	SET genre_id = (SELECT genreId from genres
  						WHERE genreName = genName);

	IF old_name IS NULL AND genre_id IS NOT NULL
	THEN	
		SET ok_response = 1;
		START TRANSACTION;
		INSERT INTO series(seriesName, seriesDescription, genreId, seriesPicturePath, episodes)
		VALUES(name, description, genre_id, img_path, episodes);
		COMMIT;
	END IF;

	SELECT ok_response;

END//
DELIMITER ;

DELIMITER //
CREATE PROCEDURE get_characters(IN seriesId int)
BEGIN
  	SELECT c.characterId, c.characterName
  	FROM characters c
  	WHERE c.seriesId = seriesId;
END//
DELIMITER ;

DELIMITER //
CREATE PROCEDURE get_character(IN chacaterId int)
BEGIN
  	SELECT c.characterName, c.characterDesc, c.characterPicturePath, c.actor
  	FROM characters c
  	WHERE c.characterId = characterId;
END//
DELIMITER ;

DELIMITER //
CREATE PROCEDURE get_chapters(IN storyId int)
BEGIN
  	SELECT c.chapterId, c.chapterTitle, c.primaryGenreId
  	FROM chapters c
  	WHERE c.storyId = storyId;
END//
DELIMITER ;

DELIMITER //
CREATE PROCEDURE get_number_of_chapters(IN storyName varchar(100))
BEGIN
  	SELECT count(c.chapterId)
  	FROM chapters c JOIN stories s ON c.storyId = s.storyId
  	WHERE s.storyTitle = storyName;
END//
DELIMITER ;

DELIMITER //
CREATE PROCEDURE get_chapter(IN chapterId int)
BEGIN
  	SELECT c.chapterPath
  	FROM chapters c
  	WHERE c.chapterId = chapterId;
END//
DELIMITER ;

DELIMITER //
CREATE PROCEDURE insert_chapter(IN chapterT varchar(100),
								IN chapterPath varchar(150),
								IN storyId int, IN genre varchar(30))
BEGIN
	DECLARE genId int;
	IF genre is NULL
	THEN 
		SET genId = NULL;
	ELSE
		SET genId = (SELECT genreId from genres WHERE genreName = genre);
	END IF;

  	START TRANSACTION;
	INSERT INTO chapters(chapterTitle, chapterPath, storyId, primaryGenreId)
	VALUES(chapterT, chapterPath, storyId, genId);
	COMMIT;
	SELECT 1;
END//
DELIMITER ;

DELIMITER //
CREATE PROCEDURE get_comments(IN storyId int)
BEGIN
  	SELECT c.commentText, c.raiting, c.postDate, u.userName
  	FROM comments c JOIN users u ON c.userId = u.userId
  	WHERE c.storyId = storyId ORDER BY c.postDate DESC;
END//
DELIMITER ;

DELIMITER //
CREATE FUNCTION get_grade(storyId int)
RETURNS INT
DETERMINISTIC
BEGIN
	DECLARE grade INT;

  	SET grade = (SELECT AVG(c.raiting) DIV 10
  				FROM comments c
  				WHERE c.storyId = storyId GROUP BY c.storyId);

  	RETURN grade;
END//
DELIMITER ;

DELIMITER //
CREATE PROCEDURE insert_comments(IN commText text,
								IN raiting int,
								IN userName varchar(50), IN storyId int,
								IN postDate varchar(10))
BEGIN
	DECLARE userId INT;
	SET userId = (SELECT u.userId FROM users u WHERE u.userName = userName);

  	START TRANSACTION;
	INSERT INTO comments(commentText, raiting, userId, storyId, postDate)
	VALUES(commText, raiting, userId, storyId, postDate);
	COMMIT;
	SELECT 1;
END//
DELIMITER ;

DELIMITER //
CREATE PROCEDURE get_genres()
BEGIN
  SELECT * FROM genres;
END//
DELIMITER ;

DELIMITER //
CREATE PROCEDURE get_allSeries()
BEGIN
  	SELECT s.seriesId, s.seriesName, s.seriesDescription, s.seriesPicturePath,
  		(SELECT count(st.storyId) FROM stories st
  		WHERE st.seriesId = s.seriesId
  		GROUP BY st.seriesId)
  	FROM series s ORDER BY s.seriesName;
END//
DELIMITER ;

DELIMITER //
CREATE PROCEDURE get_commentsRate()
BEGIN
  	SELECT MONTH(c.postDate), YEAR(c.postDate), COUNT(*)
  	FROM comments c
  	GROUP BY MONTH(c.postDate), YEAR(c.postDate)
  	ORDER BY YEAR(c.postDate), MONTH(c.postDate);
END//
DELIMITER ;

DELIMITER //
CREATE PROCEDURE get_mostStories()
BEGIN
  	SELECT s.seriesId, s.seriesName, s.seriesDescription, s.seriesPicturePath,
  		(SELECT count(st.storyId) FROM stories st
  		WHERE st.seriesId = s.seriesId
  		GROUP BY st.seriesId)
  	FROM series s
  	WHERE
  		(SELECT count(*) FROM series a
  		WHERE 
  			(SELECT count(*) FROM stories st WHERE st.seriesId = s.seriesId) < (SELECT count(*) FROM stories st WHERE st.seriesId = a.seriesId)) 
  		BETWEEN 0 AND 2;
END//
DELIMITER ;

DELIMITER //
CREATE PROCEDURE get_mostStoriesByCh()
BEGIN
  	SELECT s.storyId, s.storyTitle, ss.seriesName, u.userName,
  		(SELECT count(st.chapterId) FROM chapters st
  		WHERE st.storyId = s.storyId
  		GROUP BY st.storyId)
  	FROM stories s, series ss, users u
  	WHERE
  		s.seriesId = ss.seriesId
  		AND 
  		s.userId = u.userId
  		AND
  		(SELECT count(*) FROM stories a
  		WHERE 
  			(SELECT count(*) FROM chapters st WHERE st.storyId = s.storyId) < (SELECT count(*) FROM chapters st WHERE st.storyId = a.storyId)) 
  		IN (0, 1, 2);
END//
DELIMITER ;

DELIMITER //
CREATE PROCEDURE get_StoriesNoByUser()
BEGIN
  	SELECT u.userName, count(s.storyId)
  	FROM users u JOIN stories s ON u.userId = s.userId
  	GROUP BY s.userId;
END//
DELIMITER ;

DELIMITER //
CREATE PROCEDURE get_CommentsNoByUser()
BEGIN
  	SELECT u.userName, count(c.commentId)
  	FROM users u JOIN comments c ON u.userId = c.userId
  	GROUP BY c.userId;
END//
DELIMITER ;

DELIMITER //
CREATE PROCEDURE get_seriesByGenre(IN genreName varchar(30))
BEGIN
  	SELECT s.seriesId, s.seriesName, s.seriesDescription, s.seriesPicturePath, 
  		(SELECT count(st.storyId) FROM stories st
  		WHERE st.seriesId = s.seriesId
  		GROUP BY st.seriesId)
  	FROM series s join genres g on s.genreId = g.genreId
  	WHERE g.genreName = genreName
  	ORDER BY s.seriesName;
END//
DELIMITER ;

DELIMITER //
CREATE PROCEDURE get_stories(IN seriesId int, IN userName varchar(50))
BEGIN

	IF userName IS NULL
	THEN
	  	SELECT s.storyId, s.storyTitle, s.storyDescription, 
	  			get_grade(storyId) as grade,
	  			(select count(c.commentId) from comments c
	  			where c.storyId = s.storyId),
	  			(select se.seriesName from series se
	  			where se.seriesId = s.seriesId),
				s.characterId	 
	  	FROM stories s
	  	WHERE s.seriesId = seriesId;
	ELSE 
		SELECT s.storyId, s.storyTitle, s.storyDescription, 
				get_grade(storyId) as grade,
				(select count(c.commentId) from comments c
	  			where c.storyId = s.storyId),
	  			(select se.seriesName from series se
	  			where se.seriesId = s.seriesId),
	  			s.characterId
	  	FROM stories s JOIN users u ON u.userId = s.userId
	  	WHERE u.userName = userName;
	END IF;
END//
DELIMITER ;

DELIMITER //
CREATE PROCEDURE get_storiesss(IN seriesId int, IN userName varchar(50))
BEGIN

	IF userName IS NULL
	THEN
	  	SELECT s.storyId, s.storyTitle, s.storyDescription, 
	  			get_grade(storyId) as grade,
	  			(select count(c.commentId) from comments c
	  			where c.storyId = s.storyId),
	  			(select se.seriesName from series se
	  			where se.seriesId = s.seriesId),
				s.characterId,
				(select u.userName from users u where s.userId = u.userId)
	  	FROM stories s
	  	WHERE s.seriesId = seriesId;
	ELSE 
		SELECT s.storyId, s.storyTitle, s.storyDescription, 
				get_grade(storyId) as grade,
				(select count(c.commentId) from comments c
	  			where c.storyId = s.storyId),
	  			(select se.seriesName from series se
	  			where se.seriesId = s.seriesId),
	  			s.characterId,
	  			userName
	  	FROM stories s JOIN users u ON u.userId = s.userId
	  	WHERE u.userName = userName;
	END IF;
END//
DELIMITER ;

DELIMITER //
CREATE PROCEDURE insert_story(IN title varchar(50), IN description text,
							IN series int, IN usser varchar(50),
							IN charName varchar(70))
BEGIN
	DECLARE old_title varchar(50);
	DECLARE ok_response INT default 0;
	DECLARE user_id INT;

	SET user_id = (SELECT userId FROM users
					WHERE userName = usser);

  	SET old_title = (SELECT storyTitle FROM stories
					  	WHERE storyTitle = title);

	IF old_title IS NULL
	THEN	
		START TRANSACTION;
		INSERT INTO stories(storyTitle, storyDescription, seriesId, userId)
		VALUES(title, description, series, user_id);

		IF NOT (charName IS NULL)
		THEN
			UPDATE stories set characterId = (SELECT c.characterId FROM characters c
										WHERE c.characterName = charName)
			WHERE storyTitle = title;
		END IF;
		COMMIT;
		SET ok_response = (SELECT storyId FROM stories WHERE storyTitle = title);
	END IF;

	SELECT ok_response;

END//
DELIMITER ;