create table tweet_bow(
  tweet_id int(32) primary key,
  word varchar(128),
  tf int
);

create table tweet_info(
  tweet_id int(32) primary key,
  screen_name varchar(64),
  postted_at TIMESTAMP,
  gio_tag varchar(128) -- 座標型ってどうやってもつの
);
