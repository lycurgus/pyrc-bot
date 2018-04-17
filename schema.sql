create table users(
	id INTEGER PRIMARY KEY,
	username TEXT,
	nicknameOf INTEGER,
	pronouns TEXT,
	isBot INTEGER,
	utcOffset INTEGER,
	businessHoursStart INTEGER,
	businessHoursEnd INTEGER,
	catFacts INTEGER
);

create table calendarEvents(
	id INTEGER PRIMARY KEY,
	userId INTEGER,
	datetimeEndUtc TEXT,
	description TEXT
);

create table tickIntervals(
	id INTEGER PRIMARY KEY,
	name TEXT,
	days INTEGER,
	hours INTEGER,
	minutes INTEGER,
	seconds INTEGER,
	enabled INTEGER
);

create table tickIntervalMappings(
	intervalId INTEGER,
	identityId INTEGER
);

create table servers(
	id INTEGER PRIMARY KEY,
	name TEXT,
	host TEXT,
	port TEXT,
	enabled INTEGER
);

create table channels(
	id INTEGER PRIMARY KEY,
	serverId INTEGER,
	name TEXT,
	auto INTEGER
);

create table identities(
	id INTEGER PRIMARY KEY,
	serverId INTEGER,
	nick TEXT,
	ns_pass TEXT,
	boss TEXT,
	waketime INTEGER
	bedtime INTEGER,
);

create table petnames(
	id INTEGER PRIMARY KEY,
	identityId INTEGER,
	name TEXT
);

