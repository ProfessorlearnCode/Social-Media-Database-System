Use social_media;
GO

-- 1. Location of User 
SELECT * FROM post
WHERE location IN ('agra' ,'maharashtra','west bengal');


-- 2. Most Followed Hashtag
SELECT TOP 5
    hashtags.hashtag_name AS 'Hashtags',
    COUNT(hashtag_follow.hashtag_id) AS 'Total Follows'
FROM hashtag_follow
JOIN hashtags ON hashtags.hashtag_id = hashtag_follow.hashtag_id
GROUP BY hashtags.hashtag_name
ORDER BY COUNT(hashtag_follow.hashtag_id) DESC;


-- 3. Most Used Hashtags
SELECT TOP 10
    hashtag_name AS 'Trending Hashtags', 
    COUNT(post_tags.hashtag_id) AS 'Times Used'
FROM hashtags, post_tags
WHERE hashtags.hashtag_id = post_tags.hashtag_id
GROUP BY hashtags.hashtag_name
ORDER BY COUNT(post_tags.hashtag_id) DESC;


-- 4. Most Inactive User
SELECT user_id, username AS 'Most Inactive User'
FROM users
WHERE user_id NOT IN (SELECT user_id FROM post);

 
-- 5. Most Likes Posts
SELECT post_likes.user_id, post_likes.post_id, COUNT(post_likes.post_id) AS 'Likes Count'
FROM post_likes
JOIN post ON post.post_id = post_likes.post_id 
GROUP BY post_likes.user_id, post_likes.post_id
ORDER BY COUNT(post_likes.post_id) DESC;

-- 6. Average post per user
SELECT ROUND((COUNT(post_id) / COUNT(DISTINCT user_id) ),2) AS 'Average Post per User' 
FROM post;

-- 7. no. of log_in by per user
SELECT u.user_id, u.email, u.username, l.log_in_id AS log_in_number
FROM users u
INNER JOIN log_in l ON u.user_id = l.user_id;

-- 8. User Never Comment 
SELECT user_id, username AS 'User Never Comment'
FROM users
WHERE user_id NOT IN (SELECT user_id FROM comments);

-- 9. User Not Followed by anyone
SELECT user_id, username AS 'User Not Followed by anyone'
FROM users
WHERE user_id NOT IN (SELECT followee_id FROM follows);

-- 10. User Not Following Anyone
SELECT user_id, username AS 'User Not Following Anyone'
FROM users
WHERE user_id NOT IN (SELECT follower_id FROM follows);

-- 11. Posted more than 5 times
SELECT user_id, COUNT(user_id) AS post_count 
FROM post
GROUP BY user_id
HAVING COUNT(user_id) > 5
ORDER BY COUNT(user_id) DESC;

-- 12. Followers > 40
SELECT followee_id, COUNT(follower_id) AS follower_count FROM follows
GROUP BY followee_id
HAVING COUNT(follower_id) > 40
ORDER BY COUNT(follower_id) DESC;

-- 13. Any specific word in comment
SELECT * 
FROM comments
WHERE comment_text LIKE '%good%' OR comment_text LIKE '%beautiful%';


-- 14. Longest captions in post
SELECT TOP 5 
	user_id, caption, LEN(post.caption) AS caption_length FROM post
ORDER BY caption_length DESC;

