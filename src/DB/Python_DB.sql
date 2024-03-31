CREATE TABLE User_Users (
    id NUMBER GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    username VARCHAR2(100) NOT NULL,
    password VARCHAR2(100) NOT NULL,
    name VARCHAR2(100) NOT NULL
);

CREATE TABLE User_Interests (
    id NUMBER GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    interestName VARCHAR2(100) NOT NULL
);

CREATE TABLE User_UserInterests (
    userID NUMBER,
    interestID NUMBER,
    CONSTRAINT pk_UserUserInterests PRIMARY KEY (userID, interestID),
    CONSTRAINT fk_UserUserInterests_Users FOREIGN KEY (userID) REFERENCES User_Users(id),
    CONSTRAINT fk_UserUserInterests_Interests FOREIGN KEY (interestID) REFERENCES User_Interests(id)
);

CREATE TABLE User_NewsArticles (
    id NUMBER GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    title VARCHAR2(255) NOT NULL,
    description VARCHAR2(1000),
    url VARCHAR2(1000) NOT NULL,
    publishTime TIMESTAMP,
    source VARCHAR2(255)
);

CREATE TABLE User_UserNewsClicks (
    userID NUMBER,
    newsID NUMBER,
    clickTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT pk_UserUserNewsClicks PRIMARY KEY (userID, newsID, clickTime),
    CONSTRAINT fk_UserUserNewsClicks_Users FOREIGN KEY (userID) REFERENCES User_Users(id),
    CONSTRAINT fk_UserUserNewsClicks_NewsArticles FOREIGN KEY (newsID) REFERENCES User_NewsArticles(id)
);

