CREATE TABLE mastodon_posts
(
  id                    BINARY(16) NOT NULL DEFAULT (UUID_TO_BIN(UUID())),  # Unique ID for the record. This a smallish and not a very high performance db this should be fine. 
  post_id               BINARY(16),                                         # name of author
  mastodon_post         VARCHAR(150),                                        # THE POST ID.. if it returns
  PRIMARY KEY           (id)                                                # Make the id the primary key
);
