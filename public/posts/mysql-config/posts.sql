CREATE TABLE posts
(
  id                    BINARY(16) NOT NULL DEFAULT (UUID_TO_BIN(UUID())),  # Unique ID for the record. This a smallish and not a very high performance db this should be fine. 
  author                BINARY(16),                                         # id of author
  publish_date          DATE,                                               # publish date
  description           VARCHAR(150),                                       # post description
  link                  VARCHAR(150),                                       # Link to post
  title                 VARCHAR(150),                                       # title of hte post
  PRIMARY KEY           (id)                                                # Make the id the primary key
);
