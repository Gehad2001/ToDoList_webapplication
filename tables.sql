
CREATE TABLE todo (
  id INTEGER,
  txt TEXT NOT NULL,
  task_status boolean default false,
  PRIMARY KEY("id" AUTOINCREMENT)
 
);
