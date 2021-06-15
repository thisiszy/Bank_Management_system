-- Insert 3 Bank subbranch
INSERT INTO Subbranch
VALUES 
('Beijing支行', 0, 'Beijing'),
('Hefei支行', 0, 'Hefei'),
('Shanghai支行', 0, 'Shanghai');

-- Insert Department for each subbranch
INSERT INTO Department
VALUES 
('Beijing支行', 1, 'BeijingDepart1', 0),
('Beijing支行', 2, 'BeijingDepart2', 1),
('Beijing支行', 3, 'BeijingDepart3', 2),
('Hefei支行', 1, 'HefeiDepart1', 0),
('Hefei支行', 2, 'HefeiDepart2', 2),
('Shanghai支行', 1, 'ShanghaiDepart1', 0);

-- Insert Worker
INSERT INTO Worker
VALUES 
('Beijing支行', 1, 250648200002031558, 'Beijing aaa', '2019-1-6'),
('Beijing支行', 1, 133598265843465920, 'Beijing ddd', '2004-8-15'),
('Beijing支行', 1, 844145144382491600, 'Beijing eee', '2020-7-7'),
('Beijing支行', 2, 451044108415953800, 'Beijing bbb', '2008-10-6'),
('Beijing支行', 2, 479498355439864100, 'Beijing bbb', '2008-10-6'),
('Beijing支行', 3, 187610503053292640, 'Beijing ccc', '2016-5-1'),
('Hefei支行', 1, 109082818869501340, 'Hefei aaa', '2020-1-1'),
('Hefei支行', 2, 925647246441803900, 'Hefei bbb', '2021-4-6'),
('Hefei支行', 2, 296864911750890300, 'Hefei ccc', '2010-4-30'),
('Hefei支行', 2, 901569281378761000, 'Hefei ddd', '2017-5-10'),
('Shanghai支行', 1, 320081048272550140, 'Shanghai ccc', '2019-1-6');

-- Insert Manager
INSERT INTO Manager
VALUES 
(250648200002031558, 'Beijing支行', 1),
(451044108415953800, 'Beijing支行', 2),
(187610503053292640, 'Beijing支行', 3),
(109082818869501340, 'Hefei支行', 1),
(925647246441803900, 'Hefei支行', 2),
(320081048272550140, 'Shanghai支行', 1);

