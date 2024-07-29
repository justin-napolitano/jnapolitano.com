CREATE TABLE IF NOT EXISTS authors
(
  id                    BINARY(16) NOT NULL DEFAULT (UUID_TO_BIN(UUID())),  # Unique ID for the record. This a smallish and not a very high performance db this should be fine. 
  name                  VARCHAR(150),                                      # name of author
  PRIMARY KEY           (id)                                                # Make the id the primary key
);
