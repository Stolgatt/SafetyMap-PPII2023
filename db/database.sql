DROP TABLE IF EXISTS scores;
CREATE TABLE scores(id integer primary key autoincrement,
                    time datetime not null, 
                    score integer not null, 
                    ipv4 varchar(15));

DROP TABLE IF EXISTS incident_reports;
CREATE TABLE incident_reports(report_id integer primary key autoincrement, 
                              time datetime not null, 
                              user_id integer not null, 
                              lat numeric not null, 
                              long numeric not null, 
                              type_id integer not null, 
                              foreign key (user_id) references users(user_id), 
                              foreign key (type_id) references incident_types(type_id));

DROP TABLE IF EXISTS incident_types;
CREATE TABLE incident_types(type_id integer primary key autoincrement, 
                            name varchar not null);

DROP TABLE IF EXISTS users;
CREATE TABLE users(user_id integer primary key autoincrement, 
                   username varchar(20) not null unique,
                   password varchar(40) not null,
                   email varchar(50) not null unique,
                   name varchar(50) not null, 
                   registration_time datetime not null,
                   verified boolean not null default 0);

DROP TABLE IF EXISTS sessions;
CREATE TABLE sessions(session_id integer primary key autoincrement,
                         user_id integer not null,
                         ipv4 varchar(15) not null,
                         key varchar not null unique,
                         expiration datetime not null,
                         foreign key (user_id) references users(user_id));

DROP TABLE IF EXISTS admins;
CREATE TABLE admins(admin_id integer primary key autoincrement,
                    user_id integer not null,
                    foreign key (user_id) references users(user_id));

DROP TABLE IF EXISTS feedbacks;
CREATE TABLE feedbacks(feedback_id integer primary key autoincrement,
                       name varchar(50) not null,
                       email varchar(50) not null,
                       time datetime not null,
                       content varchar not null);

--------------- INSERTS ---------------

insert into incident_types(name) values('Agression sexuelle');
insert into incident_types(name) values('Autres');
insert into incident_types(name) values('Dégradation');
insert into incident_types(name) values('Harcèlement de rue');
insert into incident_types(name) values('Individu suspect');
insert into incident_types(name) values('Individu violent');
insert into incident_types(name) values('Vol');

insert into users(username, password, email, name, registration_time, verified) values('admin', '$2b$12$3Z5.zhi3/46XstPmYtv3ge9iwUqlsnQxe5lqkZp1NDLJMve10m25u', 'admin@site.com', 'Jean Jean', '1944-12-07 21:00:00', 1);
insert into users(username, password, email, name, registration_time, verified) values('user', '$2b$12$do2LN56aYboT70polmKDhe45c4/X5/0JftFt1komUvoMoMTzIDYzi', 'user@site.com', 'Pierre Jean','2024-01-01 01:00:00', 1);
insert into users(username, password, email, name, registration_time, verified) values('arthur_s', '$2b$12$eiBxib5b1OHaXh9IsSsCDeSEupO4ejPQdP.77e5OoCekdgaQHeEFy', 'arthur.saunier0@gmail.com', 'Saunier Arthur', '2024-01-07 11:21:52.159573', 1);
insert into users(username, password, email, name, registration_time, verified) values('DonPablito', '$2b$12$zSFZCjQ.ZSRg77rLvQH6YOr6uD6FphdYEgvEOynU66wN0F8o2xMry', 'victor.daville1@gmail.com', 'Davillé Victor', '2024-01-16 18:11:08.021681', 1);

insert into incident_reports(time, user_id, lat, long, type_id) values('2024-01-14 15:02:00', 1, 48.68573, 6.1576, 3);
insert into incident_reports(time, user_id, lat, long, type_id) values('2024-01-14 15:00:00', 2, 48.68571, 6.15786, 1);
insert into incident_reports(time, user_id, lat, long, type_id) values('2024-01-14 14:59:00', 3, 48.68581, 6.15782, 3);
insert into incident_reports(time, user_id, lat, long, type_id) values('2024-01-14 15:00:00', 4, 48.68574, 6.15774, 3);
insert into incident_reports(time, user_id, lat, long, type_id) values('2024-01-14 14:58:00', 2, 48.68565, 6.1573, 3);
insert into incident_reports(time, user_id, lat, long, type_id) values('2024-01-14 14:53:00', 3, 48.6857, 6.15759, 1);
insert into incident_reports(time, user_id, lat, long, type_id) values('2024-01-14 15:05:00', 4, 48.6858, 6.15788, 1);
insert into incident_reports(time, user_id, lat, long, type_id) values('2024-01-05 15:00:00', 1, 48.69028, 6.17575, 6);
insert into incident_reports(time, user_id, lat, long, type_id) values('2024-01-05 14:51:00', 3, 48.69037, 6.17571, 4);
insert into incident_reports(time, user_id, lat, long, type_id) values('2024-01-05 14:50:00', 4, 48.6903, 6.17566, 6);
insert into incident_reports(time, user_id, lat, long, type_id) values('2024-01-03 19:06:00', 2, 48.6796, 6.19893, 6);
insert into incident_reports(time, user_id, lat, long, type_id) values('2024-01-03 19:05:00', 1, 48.67938, 6.1984, 6);
insert into incident_reports(time, user_id, lat, long, type_id) values('2024-01-03 19:07:00', 3, 48.68013, 6.19843, 6);
insert into incident_reports(time, user_id, lat, long, type_id) values('2023-12-24 17:00:00', 1, 48.70524, 6.24558, 3);
insert into incident_reports(time, user_id, lat, long, type_id) values('2023-12-24 17:02:00', 2, 48.70456, 6.24605, 3);
insert into incident_reports(time, user_id, lat, long, type_id) values('2023-12-24 17:03:00', 3, 48.70514, 6.2451, 3);
insert into incident_reports(time, user_id, lat, long, type_id) values('2023-12-24 17:01:00', 4, 48.70434, 6.24594, 6);
insert into incident_reports(time, user_id, lat, long, type_id) values('2024-01-16 23:19:00', 3, 48.68796, 6.14207, 7);
insert into incident_reports(time, user_id, lat, long, type_id) values('2024-01-16 23:05:00', 2, 48.68876, 6.13803, 7);
insert into incident_reports(time, user_id, lat, long, type_id) values('2024-01-16 23:49:00', 2, 48.66943, 6.15509, 3);
insert into incident_reports(time, user_id, lat, long, type_id) values('2024-01-16 23:50:00', 2, 48.66889, 6.1552, 6);

insert into admins(user_id) values(1);
insert into admins(user_id) values(3);
insert into admins(user_id) values(4);

insert into feedbacks(name, email, time, content) values('Victor Davillé', 'victor.daville1@gmail.com', '2024-01-16 18:11:08.021681', 'Super contenu !');
insert into feedbacks(name, email, time, content) values('Arthur Saunier', 'arthur.saunier0@gmail.com', '2024-01-07 11:21:52.159573', 'Super site !');