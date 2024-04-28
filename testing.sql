SELECT 
       CASE WHEN player_1 IS 4 OR player_2 IS 4
       THEN 'PLAYING'
       ELSE 'AVAILABLE'
       END AS player_state
FROM games ;

select name, id, 
(SELECT 
       CASE WHEN player_1 IS players.id OR player_2 IS players.id
       THEN 'PLAYING'
       ELSE 'AVAILABLE'
       END AS player_state
FROM games )
 from players;

select name, id, 
case when exists  (select * from games)
 then 

 (SELECT 
       CASE WHEN player_1 IS players.id OR player_2 IS players.id
       THEN 'PLAYING'
       ELSE 'AVAILABLE'
       END AS player_state
FROM games )
ELSE
 "AVAILABLE"
 end as player_state
 from players;