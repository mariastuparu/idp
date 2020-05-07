use platform;

insert into users(userName, userEmail, userPass, userDescription)
values('Maria', 'marias_97@yahoo.com', sha2('parola', 224), 'ADMIN');
insert into users(userName, userEmail, userPass)
values('Maria Stuparu', 'marias_97@yahoo.com', sha2('parola1', 224));
insert into users(userName, userEmail, userPass)
values('Rares', 'rares_97@yahoo.com', sha2('parola2', 224));
insert into users(userName, userEmail, userPass)
values('Andreea', 'andreea_97@yahoo.com', sha2('parola3', 224));

insert into genres(genreName, genrePicturePath) values('Drama', './poze/genresPictures/drama_copy_62.jpg');
insert into genres(genreName, genrePicturePath) values('Comedy', './poze/genresPictures/comedy_copy_62.jpg');
insert into genres(genreName, genrePicturePath) values('Action', './poze/genresPictures/action_copy_62.jpg');
insert into genres(genreName, genrePicturePath) values('Sci-Fi', './poze/genresPictures/sciFi_copy_62.jpg');
insert into genres(genreName, genrePicturePath) values('Adventure', './poze/genresPictures/adventure_copy_62.png');
insert into genres(genreName, genrePicturePath) values('History', './poze/genresPictures/history_copy_62.jpg');
insert into genres(genreName, genrePicturePath) values('Romance', './poze/genresPictures/romance_copy_62.jpg');

insert into series(seriesName, seriesDescription, genreId, seriesPicturePath, finished, startDate, endDate, episodes) values('Friends', 'Follows the personal and professional lives of six twenty to thirty-something-year-old friends living in Manhattan.', 2, './poze/seriesPictures/friends_copy_200.jpg', 1, '1994-09-22', '2004-05-06', 236);
insert into series(seriesName, seriesDescription, genreId, seriesPicturePath, finished, startDate, endDate, episodes) values('Being Erica', 'Therapist Dr. Tom - who is constantly spouting famous and not so famous historical quotes - is Erica Strange\'s savior and worst enemy.', 5, './poze/seriesPictures/beingErica_copy_200.jpg', 1, '2009-02-19', '2011-12-12', 55);
insert into series(seriesName, seriesDescription, genreId, seriesPicturePath, finished, startDate, endDate, episodes) values('Game of Thrones', 'Nine noble families fight for control over the mythical lands of Westeros, while an ancient enemy returns after being dormant for thousands of years.', 5, './poze/seriesPictures/got_copy_200.jpg', 1, '2011-04-17', '2019-05-19', 73);
insert into series(seriesName, seriesDescription, genreId, seriesPicturePath, finished, startDate, endDate, episodes) values('Once Upon a Time', 'A young woman with a troubled past is drawn to a small town in Maine where fairy tales are to be believed.', 5, './poze/seriesPictures/ouat_copy_200.jpg', 1, '2011-10-23', '2018-05-18', 156);
insert into series(seriesName, seriesDescription, genreId, seriesPicturePath, finished, startDate, endDate, episodes) values('Breaking Bad', 'When chemistry teacher Walter White is diagnosed with Stage III cancer and given only two years to live, he decides he has nothing to lose.', 1, './poze/seriesPictures/breakingBad_copy_200.png', 1, '2008-01-20', '2013-09-29', 62);
insert into series(seriesName, seriesDescription, genreId, seriesPicturePath, finished, startDate, episodes) values('Grey\'s Anatomy', 'A medical based drama centered around Meredith Grey, an aspiring surgeon and daughter of one of the best surgeons, Dr. Ellis Grey.', 1, './poze/seriesPictures/greys_copy_200.jpg', 0, '2005-03-27', 355);
insert into series(seriesName, seriesDescription, genreId, seriesPicturePath, finished, startDate, endDate, episodes) values('The Tudors', 'A dramatic series about the reign and marriages of King Henry VIII.', 6, './poze/seriesPictures/tudors_copy_200.jpg', 1, '2007-04-01', '2010-06-20', 38);
insert into series(seriesName, seriesDescription, genreId, seriesPicturePath, finished, startDate, episodes) values('Black Mirror', 'An anthology series exploring a twisted, high-tech multiverse where humanity\'s greatest innovations and darkest instincts collide.', 4, './poze/seriesPictures/blackMirror_copy_200.jpg', 0, '2011-12-04', 22);


insert into stories(storyTitle, storyDescription, seriesId, userId) values('The One That Could Have Been', 'News that Barry and Mindy are getting divorced gets the gang wondering what their lives would be like if Rachel married Barry', 1, 2);
insert into stories(storyTitle, storyDescription, seriesId, userId) values('The Last One', 'Joey buys a new chick and duck as a house-warming gift for Chandler and Monica, the previous pair having gone to that "special farm" for old birds. Gunther confesses him love to Rachel.', 1, 2);
insert into stories(storyTitle, storyDescription, seriesId, userId) values('The Last One 2', 'The real last one', 1, 2);
insert into stories(storyTitle, storyDescription, seriesId, userId) values('El Camino', 'This story follows fugitive Jesse Pinkman as he runs from his captors, the law and his past.', 5, 3);
insert into stories(storyTitle, storyDescription, seriesId, userId) values('McDreamy', 'This story follows Derek Sheperd.', 6, 2);
insert into stories(storyTitle, storyDescription, seriesId, userId) values('DO you know?', 'Follows Christina s life as she wonders how her life would take shape based on a single decision.', 6, 4);


insert into chapters(chapterTitle, chapterPath, storyId, primaryGenreId) values('Chapter 1', './chapters/thelastone_ch1.txt', 2, 1);
insert into chapters(chapterTitle, chapterPath, storyId, primaryGenreId) values('Chapter 2', './chapters/thelastone_ch2.txt', 2, 7);
insert into chapters(chapterTitle, chapterPath, storyId, primaryGenreId) values('Chapter 3', './chapters/thelastone_ch3.txt', 2, 2);
insert into chapters(chapterTitle, chapterPath, storyId, primaryGenreId) values('A chapter with a very very very very very very very long title', './chapters/thelastone_ch4.txt', 2, 2);
insert into chapters(chapterTitle, chapterPath, storyId, primaryGenreId) values('Chapter 1', './chapters/elcamino_ch1.txt', 4, 3);
insert into chapters(chapterTitle, chapterPath, storyId, primaryGenreId) values('Chapter 2', './chapters/elcamino_ch2.txt', 4, 5);
insert into chapters(chapterTitle, chapterPath, storyId, primaryGenreId) values('Chapter 1', './chapters/mcdreamy_ch1.txt', 5, 7);


insert into comments(commentText, raiting, userId, storyId, postDate) values('Great story!!!', 97, 2, 2, '2020-03-07');
insert into comments(commentText, raiting, userId, storyId, postDate) values('I read it again!!!', 100, 2, 2, '2020-03-29');
insert into comments(commentText, raiting, userId, storyId, postDate) values('Too much romance.... But it was ok', 70, 3, 2, '2020-03-09');
insert into comments(commentText, raiting, userId, storyId, postDate) values('I\'m writing a comment to my own story...', 100, 1, 3, '2019-12-20');
insert into comments(commentText, raiting, userId, storyId, postDate) values('Random comment but very very long  Random comment but very veryg  Random comment but very very long  Random comment but very very long  Random comment but very very long ', 100, 1, 3, '2020-02-20');
insert into comments(commentText, raiting, userId, storyId, postDate) values('Random comment but very very long  Random comment but very very long  Random comment but very very long  Random comment but very very long  Random comment but very very long  Random comment but very very long  Random commomment but very very long  Random comment but very very long  Random comment but very very long  Random comment but very very long  Random comment but very very long  Random comment but very very long  Random comment but very very long  Random comment but very very long  Random comment but very very long  Random comment but very very long  Random comment but very very long Random comment but very very long  Random comment but very very long  Random comment but very very long  Random comment but very very long  Random comment but very very long  Random comment but very very long  Random comment but very very long  Random comment but very very long  Random comment but very very lbut very very long  Random comment but very very long ', 50, 1, 2, '2020-04-01');