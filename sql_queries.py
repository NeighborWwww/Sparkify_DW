import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

# DROP TABLES

staging_events_table_drop = "DROP TABLE IF EXISTS staging_events"
staging_songs_table_drop = "DROP TABLE IF EXISTS staging_songs"
songplay_table_drop = "DROP TABLE IF EXISTS songplays"
user_table_drop = "DROP TABLE IF EXISTS users"
song_table_drop = "DROP TABLE IF EXISTS songs"
artist_table_drop = "DROP TABLE IF EXISTS artists"
time_table_drop = "DROP TABLE IF EXISTS time"

# CREATE TABLES

staging_events_table_create = ("""CREATE TABLE IF NOT EXISTS staging_events (
    event_id        INT IDENTITY(0,1),
    artist_name     VARCHAR,
    auth            VARCHAR,
    user_first_name VARCHAR,
    user_gender     VARCHAR,
    item_in_session INT,
    user_last_name  VARCHAR,
    length          DOUBLE PRECISION,
    user_level      VARCHAR,
    user_location   VARCHAR,
    method          VARCHAR,
    page            VARCHAR,
    registration    VARCHAR,
    session_id      BIGINT,
    song            VARCHAR,
    status          INT,
    ts              BIGINT,
    user_agent      TEXT,
    user_id         VARCHAR,
    PRIMARY KEY(event_id)
)
""")

staging_songs_table_create = ("""CREATE TABLE IF NOT EXISTS staging_songs (
    song_id         VARCHAR,
    num_songs       INT,
    artist_id       VARCHAR,
    artist_latitude DOUBLE PRECISION,
    artist_longitude DOUBLE PRECISION,
    artist_location VARCHAR,
    artist_name     VARCHAR,
    title           VARCHAR,
    duration        DOUBLE PRECISION,
    year            INT,
    PRIMARY KEY (song_id)
)
""")

songplay_table_create = ("""CREATE TABLE IF NOT EXISTS songplays (
    songplay_id     INT IDENTITY(0,1), 
    start_time      TIMESTAMP NOT NULL, 
    user_id         VARCHAR NOT NULL, 
    level           VARCHAR, 
    song_id         VARCHAR NOT NULL, 
    artist_id       VARCHAR NOT NULL, 
    session_id      BIGINT, 
    location        VARCHAR, 
    user_agent      VARCHAR,
    PRIMARY KEY(songplay_id)
    );
""")

user_table_create = ("""CREATE TABLE IF NOT EXISTS users (
    user_id         VARCHAR NOT NULL, 
    first_name      VARCHAR, 
    last_name       VARCHAR, 
    gender          VARCHAR, 
    level           VARCHAR NOT NULL, 
    PRIMARY KEY(user_id)
    );
""")

song_table_create = ("""CREATE TABLE IF NOT EXISTS songs (
    song_id         VARCHAR NOT NULL, 
    title           VARCHAR, 
    artist_id       VARCHAR NOT NULL, 
    year            INTEGER NOT NULL, 
    duration        DOUBLE PRECISION, 
    PRIMARY KEY(song_id)
    );
""")

artist_table_create = ("""CREATE TABLE IF NOT EXISTS artists (
    artist_id       VARCHAR NOT NULL, 
    name            VARCHAR NOT NULL, 
    location        VARCHAR, 
    latitude        DOUBLE PRECISION, 
    longitude      DOUBLE PRECISION, 
    PRIMARY KEY(artist_id)
    );
""")

time_table_create = ("""CREATE TABLE IF NOT EXISTS times (
    start_time      TIMESTAMP, 
    hour            INTEGER, 
    day             INTEGER, 
    week            INTEGER, 
    month           INTEGER, 
    year            INTEGER, 
    weekday         INTEGER, 
    PRIMARY KEY(start_time)
    );
""")

# STAGING TABLES

staging_events_copy = ("""COPY staging_events 
                        FROM {} 
                        IAM_ROLE {} 
                        JSON {};
""").format(config.get('S3', 'LOG_DATA'), config.get('IAM_ROLE', 'ARN'), config.get('S3', 'LOG_JSONPATH'))


staging_songs_copy = ("""COPY staging_songs 
                        FROM {} 
                        IAM_ROLE {} 
                        JSON 'auto';
""").format(config.get('S3', 'SONG_DATA'), config.get('IAM_ROLE', 'ARN'))

# FINAL TABLES

songplay_table_insert = ("""INSERT INTO songplays (start_time, user_id, level, song_id, artist_id, session_id, location, user_agent) 
                        SELECT
                        TIMESTAMP 'epoch' + e.ts/1000 * interval '1 second' as start_time,
                        e.user_id,
                        e.user_level,
                        s.song_id,
                        s.artist_id,
                        e.session_id,
                        e.user_location,
                        e.user_agent
                        FROM staging_events e 
                        JOIN staging_songs s
                        ON e.song=s.title 
                        AND e.artist_name=s.artist_name
                        AND e.length=s.duration;
""")

user_table_insert = ("""INSERT INTO users (user_id, first_name, last_name, gender, level) 
                        SELECT DISTINCT 
                        user_id, 
                        user_first_name,
                        user_last_name,
                        user_gender,
                        user_level 
                        FROM staging_events 
                        WHERE user_id IS NOT NULL
""")

song_table_insert = ("""INSERT INTO songs (song_id, title, artist_id, year, duration) 
                        SELECT DISTINCT 
                        song_id,
                        title, 
                        artist_id,
                        year,
                        duration 
                        FROM staging_songs 
                        WHERE song_id IS NOT NULL
""")

artist_table_insert = ("""INSERT INTO artists (artist_id, name, location, latitude, longitude) 
                        SELECT DISTINCT 
                        artist_id,
                        artist_name,
                        artist_location,
                        artist_latitude,
                        artist_longitude
                        FROM staging_songs 
                        WHERE artist_id IS NOT NULL
""")

time_table_insert = ("""INSERT INTO times (start_time, hour, day, week, month, year, weekday) 
                        SELECT 
                        start_time,
                        extract (hour from start_time),
                        extract (day from start_time),
                        extract (week from start_time),
                        extract (month from start_time),
                        extract (year from start_time),
                        extract (dayofweek from start_time) 
                        FROM songplays
                        
""")

# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]
