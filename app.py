import pandas as pd
import numpy as np
import streamlit as st
import pickle
import math


team_list=['Chennai Super Kings', 'Delhi Capitals', 'Kings XI Punjab',
       'Kolkata Knight Riders', 'Mumbai Indians', 'Rajasthan Royals',
       'Royal Challengers Bangalore', 'Sunrisers Hyderabad']
venue_list=['Barabati Stadium', 'Brabourne Stadium', 'Buffalo Park',
       'De Beers Diamond Oval', 'Dr DY Patil Sports Academy',
       'Dr. Y.S. Rajasekhara Reddy ACA-VDCA Cricket Stadium',
       'Dubai International Cricket Stadium', 'Eden Gardens',
       'Feroz Shah Kotla', 'Himachal Pradesh Cricket Association Stadium',
       'Holkar Cricket Stadium', 'JSCA International Stadium Complex',
       'Kingsmead', 'M Chinnaswamy Stadium',
       'MA Chidambaram Stadium, Chepauk', 'New Wanderers Stadium',
       'Newlands', 'OUTsurance Oval',
       'Punjab Cricket Association Stadium, Mohali',
       'Rajiv Gandhi International Stadium, Uppal',
       'Sardar Patel Stadium, Motera', 'Sawai Mansingh Stadium',
       'Shaheed Veer Narayan Singh International Stadium',
       'Sharjah Cricket Stadium', 'Sheikh Zayed Stadium',
       "St George's Park", 'Subrata Roy Sahara Stadium',
       'SuperSport Park', 'Vidarbha Cricket Association Stadium, Jamtha',
       'Wankhede Stadium']

model=pickle.load(open('Model.pkl','rb'))

st.title('My IPL Predictions!')
st.subheader('Enter the match situation below and I will estimate the winning probabilities of both teams.')

col1, col2 = st.columns(2)

with col1:
       bat = st.selectbox('Batting Team',team_list)


with col2:
       bowl = st.selectbox('Bowling Team',team_list)


venue = st.selectbox('Venue',venue_list)
venue=str(venue)

bat_num=team_list.index(bat)
ball_num=team_list.index(bowl)
venue_num=venue_list.index(venue)

col3, col4, col5, col6 = st.columns(4)
with col3:
       target = st.number_input('Target',step=1, value=0)

with col4:
       runs = st.number_input('Runs',step=1, value=0)

with col5:
       wickets = st.number_input('Wickets',step=1, value=0)

with col6:
       overs = st.number_input('Over',step=1e-1, value=0.0)

if (bat == bowl):
       st.error('Batting and Bowling teams must be DIFFERENT.', icon="🚨")
       st.stop()

if (wickets > 10 or wickets < 0):
       st.error('Please enter valid number of wickets', icon="🚨")
       st.stop()

if (runs < 0):
       st.error('Please enter valid number of runs', icon="🚨")
       st.stop()

if (runs > target):
       st.error('Please enter valid number of runs', icon="🚨")
       st.stop()

if (target < 0):
       st.error('Please enter a valid Target', icon="🚨")
       st.stop()

if (round(math.modf(overs)[0], 1) < 0.0 or round(math.modf(overs)[0], 1) > 0.5):
       st.error('Please enter valid over number (Eg: 5.5, 0.2, 16.4. (Use 4.0 instead of 3.6))', icon="🚨")
       st.stop()

if(overs*10!=int(overs*10)):
       st.error('Please enter valid over number (Eg: 5.5, 0.2, 16.4. (Use 4.0 instead of 3.6))', icon="🚨")
       st.stop()

if(overs>20):
       st.error('Please enter valid over number (Eg: 5.5, 0.2, 16.4. (Use 4.0 instead of 3.6))', icon="🚨")
       st.stop()


runs_left=target-runs
over=math.floor(overs)
ball=round(math.modf(overs)[0],1)*10
balls=over*6+ball
balls_left=120-balls
wickets_left=10-wickets
rrr=runs_left*6/balls_left


st.subheader('Click below for predictions!')

if st.button('Predict'):

       pred_val=model.predict_proba([[bat_num,ball_num,venue_num,runs_left,balls_left,wickets_left]])
       win_pred=pred_val[0][1]
       lose_pred=pred_val[0][0]
       temp=abs(win_pred-lose_pred)*100

       st.write(bat,' requires ',runs_left,'runs in ',balls_left,'balls at a required run rate of ',round(rrr,2),'runs per over.')
       if(temp<=20):
              if(win_pred>lose_pred):
                     st.write('The match seems fairly in balance but still ',bat,' are a step ahead at this point.')
                     st.write('At this stage ',bat,' has ',round(win_pred*100,1),
                              '% chance of winning but no one knows what might happen next!')

              if (win_pred < lose_pred):
                     st.write('The match seems fairly in balance but still ', bowl, ' are a step ahead at this point.')
                     st.write('At this stage ', bowl, ' has ', 100-round(win_pred*100, 1),
                              '% chance of winning but no one knows what might happen next!')

       if (temp>20 and temp<80):
              if (win_pred > lose_pred):
                     st.write( bat, ' are visibly quite ahead at this point.')
                     st.write('At this stage ', bat, ' has ', round(win_pred * 100, 1),
                              '% chance of winning and it looks like eventually they are gonna '
                              'win so we have to wait and watch!')

              if (win_pred < lose_pred):
                     st.write( bowl, ' are visibly quite ahead at this point.')
                     st.write('At this stage ', bowl, ' has ',100- round(win_pred * 100, 1),
                              '% chance of winning and it looks like eventually they are gonna '
                              'win so we have to wait and watch!')


       if (temp>=80) :
              if (win_pred > lose_pred):
                     st.write( bat, ' are way ahead at this point and it does not seem they are going to lose from here.')
                     st.write('At this stage ', bat, ' has ', round(win_pred * 100, 1),
                              '% chance of winning and ',bowl, 'need to pull off a miracle to win this game!')

              if (win_pred < lose_pred):
                     st.write(bowl, ' are way ahead at this point and it does not seem they are going to lose from here.')
                     st.write('At this stage ', bowl, ' has ', 100-round(win_pred * 100, 1),
                              '% chance of winning and ', bat, 'need to pull off a miracle to win this game!')









