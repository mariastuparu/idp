CREATE DATABASE platform;
use platform;

create table users(
    userId int not null auto_increment,
	userName nvarchar(50) not null,
	userEmail nvarchar(50) not null,
	userPass nvarchar(300) not null,
	userDescription text,
	primary key (userId)
);

create table genres(
	genreId int not null auto_increment,
	genreName varchar(30) not null,
	genrePicturePath varchar(100),
	primary key (genreId),
	unique (genreName)
);

create table series(
	seriesId int not null auto_increment,
	seriesName varchar(70) not null,
	seriesDescription text,
	genreId int,
	seriesPicturePath varchar(100),
	finished int,
	startDate date,
	endDate date,
	episodes int,	
	primary key (seriesId),
	foreign key (genreId) references genres(genreId),
	unique (seriesPicturePath),
	unique (seriesName)
);

create table characters(
	characterId int not null auto_increment,
	characterName nvarchar(70),
	characterDesc text,
	characterPicturePath nvarchar(100),
	seriesId int not null,
	primary key (characterId),
	foreign key (seriesId) references series(seriesId)
);

create table stories(
	storyId int not null auto_increment,
	storyTitle nvarchar(100) not null,
	storyDescription text,
	seriesId int not null,
	userId int not null,
	characterId int,
	primary key (storyId),
	foreign key (seriesId) references series(seriesId),
	foreign key (userId) references users(userId)
);

create table comments(
	commentId int not null auto_increment,
	commentText text not null,
	raiting tinyint, 
	userId int not null,
	storyId int not null,
	postDate date,
	primary key (commentId),
	foreign key (userId) references users(userId),
	foreign key (storyId) references stories(storyId)
);

create table chapters(
	chapterId int not null auto_increment,
	chapterTitle nvarchar(100),
	chapterPath nvarchar(150),
	storyId int not null,
	primaryGenreId int,
	primary key (chapterId),
	foreign key (primaryGenreId) references genres(genreId),
	foreign key (storyId) references stories(storyId)
);


