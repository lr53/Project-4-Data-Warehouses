import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

# DROP TABLES

staging_events_table_drop = "DROP TABLE IF EXISTS staging_events;"
staging_songs_table_drop = "DROP TABLE IF EXISTS staging_songs;"
songplay_table_drop = "DROP TABLE IF EXISTS songplay;"
user_table_drop = "DROP TABLE IF EXISTS users;"
song_table_drop = "DROP TABLE IF EXISTS song;"
artist_table_drop = "DROP TABLE IF EXISTS artist;"
time_table_drop = "DROP TABLE IF EXISTS time;"

# CREATE TABLES

staging_events_table_create= ("""
CREATE TABLE IF NOT EXISTS staging_events(
    artist VARCHAR,
    auth VARCHAR,
    firstName VARCHAR,
    gender CHAR(1),
    itemInSession INTEGER,
    lastName VARCHAR,
    length FLOAT,
    level VARCHAR,
    location VARCHAR,
    method VARCHAR,
    page VARCHAR,
    registration FLOAT,
    sessionId INTEGER,
    song VARCHAR,
    status INTEGER,
    ts BIGINT NOT NULL,
    userAgent VARCHAR,
    userId VARCHAR
);
""")

staging_songs_table_create = ("""
CREATE TABLE IF NOT EXISTS staging_songs ( 
    num_songs INTEGER,
    artist_id VARCHAR,
    artist_latitude FLOAT,
    artist_longitude FLOAT,
    artist_location VARCHAR,
    artist_name VARCHAR,
    song_id VARCHAR,
    title VARCHAR,
    duration FLOAT,
    year INTEGER
);
""")

songplay_table_create = ("""
CREATE TABLE IF NOT EXISTS songplay(
    songplay_id INTEGER IDENTITY (0,1) PRIMARY KEY,
    start_time TIMESTAMP,
    user_id INTEGER,
    level VARCHAR,
    song_id VARCHAR,
    artist_id VARCHAR,
    session_id INTEGER,
    location VARCHAR,
    user_agent VARCHAR
);

""")

user_table_create = ("""
CREATE TABLE IF NOT EXISTS users(
    user_id INTEGER PRIMARY KEY,
    first_name VARCHAR,
    last_name VARCHAR,
    gender CHAR(1),
    level VARCHAR
);
""")

song_table_create = ("""
CREATE TABLE IF NOT EXISTS song (
    song_id VARCHAR PRIMARY KEY,
    title VARCHAR,
    artist_id VARCHAR,
    year INTEGER,
    duration FLOAT
);
""")

artist_table_create = ("""
CREATE TABLE IF NOT EXISTS artist (
    artist_id VARCHAR PRIMARY KEY,
    name VARCHAR,
    location VARCHAR,
    latitude FLOAT,
    longitude FLOAT
);
""")

time_table_create = ("""
CREATE TABLE IF NOT EXISTS time (
    start_time TIMESTAMP PRIMARY KEY,
    hour INTEGER,
    day INTEGER,
    week INTEGER,
    month INTEGER,
    year INTEGER,
    weekday VARCHAR
)
""")

# STAGING TABLES

staging_events_copy = ("""
COPY staging_events
FROM {}
CREDENTIALS 'aws_iam_role={}'
REGION 'us-west-2'
FORMAT AS json {};
""").format(config.get('S3','LOG_DATA'), config.get('IAM_ROLE', 'ARN'), config.get('S3', 'LOG_JSONPATH'))

staging_songs_copy = ("""
COPY staging_songs
FROM {}
CREDENTIALS 'aws_iam_role={}'
REGION 'us-west-2'
FORMAT AS json 'auto';
""").format(config.get('S3', 'SONG_DATA'), config.get('IAM_ROLE', 'ARN'))

# FINAL TABLES

songplay_table_insert = ("""
    INSERT INTO songplay (start_time, user_id, level, song_id, artist_id, session_id, location, user_agent)
    SELECT se.ts,
           se.userId,
           se.level,
           ss.song_id,
           ss.artist_id,
           se.sessionId,
           se.location,
           se.userAgent
    FROM staging_events se
    JOIN staging_songs ss
    ON (se.song = ss.title) AND (se.artist = ss.artist_name) AND (se.length = ss.duration)
    WHERE se.page='NextSong'
;
""")

user_table_insert = ("""
    INSERT INTO users (user_id, first_name, last_name, gender, level)
    SELECT DISTINCT userId, firstName, lastName, gender, level
    FROM staging_events
    WHERE page = 'NextSong'
    AND user_id NOT IN (SELECT DISTINCT user_id FROM user)
;
""")

song_table_insert = ("""
    INSERT INTO song (song_id, title, artist, year, duration)
    SELECT song_id, title, artist_name, year, duration
    FROM staging_songs
;
""")

artist_table_insert = ("""
    INSERT INTO artist (artist_id, name, location, latitude, longitude)
    SELECT DISTINCT artist_id, artist_name, artist_location, artist_longitude
    FROM staging_songs
;
""")

time_table_insert = ("""
    INSERT INTO time (start_time, hour, day, week, month, year, weekday)
    SELECT DISTINCT TIMESTAMP 'epoch' + (ts/1000) * INTERVAL '1 second' AS start_time, 
           EXTRACT (HOUR FROM start_time) AS hour,
           EXTRACT (DAY FROM start_time) AS day,
           EXTRACT (WEEK FROM start_time) AS week,
           EXTRACT (MONTH FROM start_time) AS month,
           EXTRACT (YEAR FROM start_time) AS year,
           EXTRACT (WEEKDAY FROM start_time) AS weekday
    FROM staging_events
;          
""")


# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]
