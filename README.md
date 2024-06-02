# Database Administrator

## Overview

This Python-based Database Administrator program provides a user-friendly interface to manage databases efficiently. It enables users to perform various operations such as connecting to a server, browsing databases and tables, executing SQL queries, inserting, updating, and deleting data, and more.

## Sections

- **Database Administrator - Front End**
- **Database Connection**
- **Database Management**
- **SQL Operations**
- **File Operations**
- **Main Functionality**

--------------------------------------------------------------------------------------------------

### [Database Administrator - Front End](https://github.com/ProfessorlearnCode/Social-Media-Database-System/blob/main/Database_administator.py)

The front end of the program handles user authentication and provides a menu-driven interface for interacting with the database. It includes functions for user authorization, connecting to the server, and displaying a menu with various database management options.

### Database Connection

The `connection_to_server` function establishes a connection to a SQL Server using pyodbc in Python. It takes no parameters and returns a connection string object upon successful connection.

### Database Management

- `show_databases`: Retrieves and displays the names of databases in a given server using a SQL query.
- `change_database`: Switches the connection to a different database using the provided connection string.
- `show_tables`: Retrieves and displays the names of all base tables in a database using the provided connection string.
- `create_table`: Prompts the user to input a table name and attributes, then creates a table with the specified attributes in the current database.
- `show_column_names`: Retrieves the column names of a specified table in a database using a given connection string.

### SQL Operations

- `Insertion`: Allows users to insert values into a specified table in a database, handling cases where a timestamp column is present or not.
- `Updatation`: Takes user input for table name and update script, then executes an SQL query to update the specified table in the database.
- `deletion`: Deletes records from a specified table in the database based on user-provided conditions.
- `table_truncation`: Truncates a specified table in a database connection using SQL `TRUNCATE TABLE` or `DELETE FROM` based on the provided table name.
- `drop_table`: Drops a specified table in a database connection, handling potential errors related to primary and foreign keys.

### File Operations

- `open_sql_file`: Reads and executes SQL commands from a specified file using a provided database connection string.
- `export_to_csv`: Exports data from a database table to a CSV file.

### Main Functionality

The `main` function serves as the entry point of the program. It first checks for user authorization using the `user_authorization()` function. If the user is authorized, it clears the screen and displays a menu with various database management options. Users can choose an option from the menu to perform specific database operations.

## Conclusion

This Database Administrator program provides a robust and intuitive interface for managing databases efficiently. Whether you need to perform basic CRUD operations, execute SQL queries, or export data to external files, this program offers a comprehensive solution for database management tasks.


# [MSSQL THREADS Database Schema](https://github.com/ProfessorlearnCode/Social-Media-Database-System/blob/main/schema.sql)

## Overview

The MSSQL Database Schema presented here defines the structure of a social media platform's database. It includes tables for users, posts, comments, likes, follows, hashtags, bookmarks, login logs, and more. This schema forms the backbone of the social media platform, facilitating data storage and retrieval for various features and functionalities.

## Sections

- **User Management**
- **Content Management**
- **Interaction and Engagement**
- **Metadata and Logging**

--------------------------------------------------------------------------------------------------

### User Management

The user management section defines tables related to user profiles, authentication, and interactions.

- `Users`: Stores information about users, including their username, profile photo URL, bio, email, and registration date.
- `Log_in`: Records login activity, including the user's ID, IP address, and login time.

### Content Management

This section encompasses tables related to content creation, such as posts, photos, videos, and hashtags.

- `Posts`: Represents individual posts made by users, including captions, location, and creation date.
- `Photos`: Stores information about uploaded photos, including the photo URL, post ID, and creation date.
- `Videos`: Stores information about uploaded videos, including the video URL, post ID, and creation date.
- `Comments`: Stores user comments on posts, including the comment text, post ID, user ID, and creation date.
- `Hashtags`: Stores unique hashtags used in posts, along with their creation date.

### Interaction and Engagement

This section focuses on tables related to user interactions, engagement metrics, and social connections.

- `Post_likes`: Records instances of users liking posts, including the user ID, post ID, and creation date.
- `Comment_likes`: Records instances of users liking comments, including the user ID, comment ID, and creation date.
- `Follows`: Represents user follow relationships, including the follower ID, followee ID, and creation date.
- `Hashtag_follow`: Tracks instances of users following hashtags, including the user ID, hashtag ID, and creation date.
- `Bookmarks`: Stores instances of users bookmarking posts for later reference, including the user ID, post ID, and creation date.

### Metadata and Logging

This section includes tables for metadata management and logging user activities.

- `Post_tags`: Associates posts with hashtags, allowing users to categorize and discover content.
- `Bookmark`: Tracks instances of users bookmarking posts for later reference, including the user ID, post ID, and creation date.

## Conclusion

The MSSQL Database Schema provided here serves as the foundation for building a social media platform, offering comprehensive data modeling for user management, content creation, interaction, engagement, and metadata management. By following this schema, developers can design and implement a robust database backend capable of supporting various social networking features and functionalities.

# [Sample Queries for Database](https://github.com/ProfessorlearnCode/Social-Media-Database-System/blob/main/queries.sql)

## Overview

This section provides a set of sample queries designed to extract insightful information from the social media database. These queries offer valuable insights into user behavior, engagement patterns, and content popularity, enabling developers to analyze and optimize their platform's performance.

## Sections

- **User Location and Activity**
- **Hashtag Analysis**
- **User Engagement**
- **User Activity and Interaction**

--------------------------------------------------------------------------------------------------

### User Location and Activity

These queries focus on analyzing user activity based on location and engagement metrics.

1. `Location of User`: Retrieves posts made by users in specific locations like Agra, Maharashtra, or West Bengal.

2. `Most Inactive User`: Identifies users who have not made any posts on the platform, helping to identify inactive accounts.

3. `Average Posts per User`: Calculates the average number of posts made per user on the platform.

4. `Number of Logins per User`: Counts the number of login activities performed by each user.

### Hashtag Analysis

These queries analyze the popularity and usage of hashtags on the platform.

5. `Most Followed Hashtag`: Identifies the top 5 most followed hashtags based on user subscriptions.

6. `Most Used Hashtags`: Lists the top 10 trending hashtags based on the number of times they have been used in posts.

7. `Hashtags in Comments`: Searches for comments containing specific words like "good" or "beautiful".

### User Engagement

These queries analyze user engagement metrics such as likes and comments.

8. `Most Liked Posts`: Identifies posts with the highest number of likes, helping to gauge content popularity.

9. `User Never Comment`: Identifies users who have never commented on any posts.

10. `User Not Followed by Anyone`: Identifies users who have not been followed by any other users.

11. `User Not Following Anyone`: Identifies users who are not following any other users.

12. `Posted More Than 5 Times`: Identifies users who have posted more than 5 times on the platform.

### User Activity and Interaction

These queries analyze user activity and interaction patterns on the platform.

13. `Longest Captions in Posts`: Lists the top 5 posts with the longest captions, allowing for analysis of user-generated content.

14. `Followers Count`: Identifies users with more than 40 followers, indicating their influence and popularity on the platform.

## Conclusion

The sample queries provided here offer valuable insights into various aspects of the social media platform, including user activity, engagement, and content popularity. By running these queries on the database, developers can gain a deeper understanding of user behavior and preferences, allowing them to make informed decisions to improve the platform's performance and user experience.
