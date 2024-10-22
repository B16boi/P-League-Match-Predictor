import psycopg2

connection = psycopg2.connect(user="DB_USER",
                             password="DB_PWORD",
                             host="DB_AWS_CRED",
                             port="DB_POPRT",
                             database="DB_PLG")
#gets the credentials from .aws/credentials

sql0="""
select away
from upcoming
where date = '%s' and home = '%s'
"""

sql1="""
with awayavg as (select score, lost from %s where arena = 'A'),
     alasttenavg as (select score, lost from %s order by date desc limit 10 ),
     awayteamavg as (select score, lost from %s), 
     
     homeavg as (select score, lost from %s where arena = 'H'),
     hlasttenavg as (select score, lost from %s order by date desc limit 10 ), 
     hometeamavg as (select score, lost from %s) 
select ( (avg(homeavg.score) +  avg(hlasttenavg.score) + avg(hometeamavg.score)) 
       - (avg(awayavg.score) + avg(alasttenavg.score) + avg(awayteamavg.score)) 
       + (avg(awayavg.lost) + avg(alasttenavg.lost) + avg(awayteamavg.lost)) 
       - (avg(homeavg.lost) +  avg(hlasttenavg.lost) + avg(hometeamavg.lost))) / 6 as point_spread 
       
from awayavg, alasttenavg, awayteamavg, homeavg, hlasttenavg, hometeamavg
"""
connection.autocommit=True
cursor = connection.cursor()
print("請輸入以下P+球隊: braves/kings/dreamer/lioneers/pilots/steelers")
input0=input("請輸入日期: ")
input1=input("請輸入客隊: ")
input2=input("請輸入主隊: ")

cursor.execute(sql0 %(input0, input1))
matchup = cursor.fetchone()
if matchup is None:
    print("Incorrect matchup!")
else:
    j = matchup[0]
    if input2 != j:
        print("Incorrect matchup!")
    else:
        cursor.execute(sql1 %(input2, input2, input2, input1, input1, input1))
        record=cursor.fetchone()
        i = float(record[0])
        print("Point_spread: ", '%.1f' %i)
        if i < 0 :
            print("Favorite team:  Away Team")
        else:
            print("Favorite team:  Home Team")
        sql2="""
        with awayavg as (select score, lost from %s where arena = 'A'),
             alasttenavg as (select score, lost from %s order by date desc limit 10 ), 
             awayteamavg as (select score, lost from %s), 

             homeavg as (select score, lost from %s where arena = 'H'),
             hlasttenavg as (select score, lost from %s order by date desc limit 10 ), 
             hometeamavg as (select score, lost from %s)

             select ( (avg(homeavg.score) +  avg(hlasttenavg.score) + avg(hometeamavg.score)) 
             + (avg(awayavg.score) + avg(alasttenavg.score) + avg(awayteamavg.score))
	         + (avg(awayavg.lost) + avg(alasttenavg.lost) + avg(awayteamavg.lost))
             + (avg(homeavg.lost) +  avg(hlasttenavg.lost) + avg(hometeamavg.lost))) / 6 as Combined_Total
       
             from awayavg, alasttenavg, awayteamavg, homeavg, hlasttenavg, hometeamavg
            """
        cursor.execute(sql2 %(input2, input2, input2, input1, input1, input1))
        record=cursor.fetchone()
        i = float(record[0])
        print("Projected Total: ", '%.1f' %i)

        sql3="""
        with awayavg as (select score, lost from %s where arena = 'A'),
             alasttenavg as (select score, lost from %s order by date desc limit 10 ), 
             awayteamavg as (select score, lost from %s), 

             homeavg as (select score, lost from %s where arena = 'H'),
             hlasttenavg as (select score, lost from %s order by date desc limit 10 ), 
             hometeamavg as (select score, lost from %s)

        select ( (avg(homeavg.score) +  avg(hlasttenavg.score) + avg(hometeamavg.score)) 
        	   + (avg(awayavg.lost) + avg(alasttenavg.lost) + avg(awayteamavg.lost))) / 6 as HomeTeam_Total
       
        from awayavg, alasttenavg, awayteamavg, homeavg, hlasttenavg, hometeamavg   
        """
        cursor.execute(sql3 %(input2, input2, input2, input1, input1, input1))
        record=cursor.fetchone()
        i = float(record[0])
        print("Projected Home Team Total: ", '%.1f' %i)