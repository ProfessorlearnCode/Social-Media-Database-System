USE master;
GO
ALTER DATABASE social_media SET SINGLE_USER WITH ROLLBACK IMMEDIATE;
GO
DROP DATABASE social_media;
GO

CREATE DATABASE social_media;
USE social_media;
GO

CREATE TABLE users (
    user_id INT IDENTITY(1,1) PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    profile_photo_url VARCHAR(255) DEFAULT 'https://th.bing.com/th/id/R.6b635dff497042ec0b6f3ea47dc47170?rik=wsuwv2QLQfQv6g&pid=ImgRaw&r=0&sres=1&sresct=1',
    bio VARCHAR(255),
    created_at DATETIME DEFAULT GETDATE(),
);

ALTER TABLE users
ADD email VARCHAR(30) NOT NULL;

CREATE TABLE photos (
    photo_id INT IDENTITY(1,1) PRIMARY KEY,
    photo_url VARCHAR(255) NOT NULL UNIQUE,
    post_id	INT NOT NULL,
    created_at DATETIME DEFAULT GETDATE(),
    size FLOAT CHECK (size<5)
);

CREATE TABLE videos (
  video_id INT IDENTITY(1,1) PRIMARY KEY,
  video_url VARCHAR(255) NOT NULL UNIQUE,
  post_id INT NOT NULL,
  created_at DATETIME DEFAULT GETDATE(),
  size FLOAT CHECK (size<10)
  
);

CREATE TABLE post (
	post_id INT IDENTITY(1,1) PRIMARY KEY,
    photo_id INT,
    video_id INT,
    user_id INT NOT NULL,
    caption VARCHAR(200) NULL, 
    location VARCHAR(50) NULL,
    created_at DATETIME DEFAULT GETDATE(),
    FOREIGN KEY(user_id) REFERENCES users(user_id),
	FOREIGN KEY(photo_id) REFERENCES photos(photo_id),
    FOREIGN KEY(video_id) REFERENCES videos(video_id)
);

CREATE TABLE comments (
    comment_id INT IDENTITY(1,1) PRIMARY KEY,
    comment_text VARCHAR(255) NOT NULL,
    post_id INT NOT NULL,
    user_id INT NOT NULL,
    created_at DATETIME DEFAULT GETDATE(),
    FOREIGN KEY(post_id) REFERENCES post(post_id),
    FOREIGN KEY(user_id) REFERENCES users(user_id)
);

CREATE TABLE post_likes (
    user_id INT NOT NULL,
    post_id INT NOT NULL,
    created_at DATETIME DEFAULT GETDATE(),
    FOREIGN KEY(user_id) REFERENCES users(user_id),
    FOREIGN KEY(post_id) REFERENCES post(post_id),
    PRIMARY KEY(user_id, post_id)
);

CREATE TABLE comment_likes (
    user_id INT NOT NULL,
    comment_id INT NOT NULL,
    created_at DATETIME DEFAULT GETDATE(),
    FOREIGN KEY(user_id) REFERENCES users(user_id),
    FOREIGN KEY(comment_id) REFERENCES comments(comment_id),
    PRIMARY KEY(user_id, comment_id)
);

CREATE TABLE follows (
    follower_id INT NOT NULL,
    followee_id INT NOT NULL,
    created_at DATETIME DEFAULT GETDATE(),
    FOREIGN KEY(follower_id) REFERENCES users(user_id),
    FOREIGN KEY(followee_id) REFERENCES users(user_id),
    PRIMARY KEY(follower_id, followee_id)
);

CREATE TABLE hashtags (
  hashtag_id INT IDENTITY(1,1) PRIMARY KEY,
  hashtag_name VARCHAR(255) UNIQUE,
  created_at DATETIME DEFAULT GETDATE()
);

CREATE TABLE hashtag_follow (
	user_id INT NOT NULL,
    hashtag_id INT NOT NULL,
    created_at DATETIME DEFAULT GETDATE(),
    FOREIGN KEY(user_id) REFERENCES users(user_id),
    FOREIGN KEY(hashtag_id) REFERENCES hashtags(hashtag_id),
    PRIMARY KEY(user_id, hashtag_id)
);

CREATE TABLE post_tags (
    post_id INT NOT NULL,
    hashtag_id INT NOT NULL,
    FOREIGN KEY(post_id) REFERENCES post(post_id),
    FOREIGN KEY(hashtag_id) REFERENCES hashtags(hashtag_id),
    PRIMARY KEY(post_id, hashtag_id)
);

CREATE TABLE bookmarks (
  post_id INT NOT NULL,
  user_id INT NOT NULL,
  created_at DATETIME DEFAULT GETDATE(),
  FOREIGN KEY(post_id) REFERENCES post(post_id),
  FOREIGN KEY(user_id) REFERENCES users(user_id),
  PRIMARY KEY(user_id, post_id)
);

CREATE TABLE log_in (
  log_in_id INT NOT NULL IDENTITY(1,1) PRIMARY KEY,
  user_id INT NOT NULL,
  ip VARCHAR(50) NOT NULL,
  log_in_time DATETIME NOT NULL DEFAULT GETDATE(),
  FOREIGN KEY(user_id) REFERENCES users(user_id)
);

select * from users;
select * from photos;
select * from videos;
select * from comments;
select * from comment_likes;
select * from post;
select * from post_likes;
select * from post_tags;
select * from hashtags;
select * from hashtag_follow;
select * from log_in;
select * from bookmarks;
select * from follows;