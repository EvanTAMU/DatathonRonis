from os import listdir
import streamlit as st
import plotly.express as px
import pandas as pd
import matplotlib.pyplot as plt

#First collect all the data
path = '/Users/evanriekert/Downloads/Roni_s Challenge public/Provided Data [FINAL]/'
datasets = listdir('Provided Data [FINAL]')
dataPaths = []
for i in range(len(datasets)):
    dataPaths.append(path + datasets[i])
dateRange = f'{((datasets[0])[:-9])} - {(datasets[-1])[:-9]}'
testdata = None
dates = []
lines = []
orderList = [[]]
orderNum = 0
pastLineNum = ''
mealDict = {}
toppingDict = {}
bowlDict = {}
monthData = {}
        
def convert_month_data_to_df(month_data):
    records = []
    for month, days in month_data.items():
        for day, times in days.items():
            for time in times:
                records.append({'Month': month, 'Day': day, 'Time': time})
    return pd.DataFrame(records)

def streamLitRun(dishes,toppings,bowls):
    df = pd.DataFrame(list(dishes.items()), columns=['Dishes', 'Popularity'])
    dfToppings = pd.DataFrame(list(toppings.items()), columns=['Toppings', '# Ordered in range'])
    dfBowls = pd.DataFrame(list(bowls.items()), columns=['Bowls', '# Ordered in range'])

    st.title('Roni\'s Super-Mac Dashboard')
    st.markdown(
    """
    <style>
    .stApp {
        background-image: url("https://media.istockphoto.com/id/1473988115/vector/italian-pasta-seamless-pattern-isolated-on-green-background-macaroni-pasta.jpg?s=612x612&w=0&k=20&c=uI4AfYrmzPVApxDJm5ztfsQ1uPrQPl3hBRJhnGRO1I4=");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }
    </style>
    """,
    
    unsafe_allow_html=True
    )

    chart_selection = st.selectbox('Choose the Graph to View', ('Dishes Ordered', 'Popular Mac and Cheese Toppings', 'Popular Aggie \'Bowls\'', 'Order Date Trends'))
    if chart_selection == 'Dishes Ordered':
        chart_type = st.radio('Choose Graph Type:', ('Bar Chart','Pie Chart'))
        df_sorted = df.sort_values(by='Popularity', ascending=False)

        if chart_type == 'Bar Chart':
            fig = px.bar(df_sorted, x='Dishes', y='Popularity', title=f'Amount of Dishes Ordered {dateRange} | Bar Chart')
        else:
            fig = px.pie(df_sorted, names='Dishes', values='Popularity', title=f'Amount of Dishes Ordered {dateRange} | Pie Chart')
        st.plotly_chart(fig)
    elif chart_selection == 'Popular Mac and Cheese Toppings': # Fix the values when gotten
        chart_type = st.radio('Choose Radio Type:', ('Bar Chart','Pie Chart'))
        df_sorted = dfToppings.sort_values(by='# Ordered in range', ascending=False)

        if chart_type == 'Bar Chart':
            fig = px.bar(df_sorted, x='Toppings', y='# Ordered in range', title=f'Most Popular Toppings {dateRange} | Bar Chart')
        else:
            fig = px.pie(df_sorted, names='Toppings', values='# Ordered in range', title=f'Most Popular Toppings {dateRange} | Pie Chart')
        st.plotly_chart(fig)
    elif chart_selection == 'Popular Aggie \'Bowls\'': # Fix the values when gotten
        chart_type = st.radio('Choose Graph Type:', ('Bar Chart','Pie Chart'))
        top_n = st.number_input("Input number of bowls to show", 1, len(dfBowls), 10)
        df_sorted = dfBowls.sort_values(by='# Ordered in range', ascending=False).head(top_n)


        if chart_type == 'Bar Chart':
            fig = px.bar(df_sorted, x='Bowls', y='# Ordered in range', title=f'Most Popular Bowls {dateRange} | Bar Chart')
        else:
            fig = px.pie(df_sorted, names='Bowls', values='# Ordered in range', title=f'Most Popular Bowls {dateRange} | Pie Chart')
        st.plotly_chart(fig)
    #------------------------------
    elif chart_selection == 'Order Date Trends': #Working date thing
        df = convert_month_data_to_df(monthData)
        chart_type = st.radio('Choose Graph Type:', ('Bar Chart','Area Chart'))
        st.subheader("Total Orders per Month")
        
        if chart_type == 'Area Chart':
            month_counts = df['Month'].value_counts().sort_index()
            fig_month = px.area(month_counts, x=month_counts.index, y=month_counts.values,
                            labels={'x': 'Month', 'y': 'Total Orders'},
                            title='Total Orders per Month')
            #fig_month.update_traces(marker_color='yellow')
            st.plotly_chart(fig_month)

            # Month selection for day breakdown
            selected_month = st.selectbox("Select a Month", sorted(monthData.keys()), format_func=lambda x: f"Month {x}")
            if selected_month:
                # Filter data for the selected month and plot orders per day
                st.subheader(f"Orders per Day in Month {selected_month}")
                days_in_month = df[df['Month'] == selected_month]['Day'].value_counts().sort_index()
                fig_days = px.area(days_in_month, x=days_in_month.index, y=days_in_month.values,
                                labels={'x': 'Day', 'y': 'Total Orders'},
                                title=f"Total Orders per Day in Month {selected_month}")
                #fig_days.update_traces(marker_color='yellow')
                st.plotly_chart(fig_days)

                # Day selection for time breakdown
                selected_day = st.selectbox("Select a Day", sorted(monthData[selected_month].keys()), format_func=lambda x: f"Day {x}")
                if selected_day:
                    # Filter data for the selected day and plot orders per time
                    st.subheader(f"Order Times on {selected_month}-{selected_day}")
                    times_in_day = df[(df['Month'] == selected_month) & (df['Day'] == selected_day)]['Time'].value_counts().sort_index()
                    fig_times = px.area(times_in_day, x=times_in_day.index, y=times_in_day.values,
                                    labels={'x': 'Time', 'y': 'Order Count'},
                                    title=f"Order Times on {selected_month}-{selected_day}")
                    #fig_times.update_traces(marker_color='yellow')
                    st.plotly_chart(fig_times)
        else:
            month_counts = df['Month'].value_counts().sort_index()
            fig_month = px.bar(month_counts, x=month_counts.index, y=month_counts.values,
                            labels={'x': 'Month', 'y': 'Total Orders'},
                            title='Total Orders per Month')
            #fig_month.update_traces(marker_color='yellow')
            st.plotly_chart(fig_month)

            # Month selection for day breakdown
            selected_month = st.selectbox("Select a Month", sorted(monthData.keys()), format_func=lambda x: f"Month {x}")
            if selected_month:
                # Filter data for the selected month and plot orders per day
                st.subheader(f"Orders per Day in Month {selected_month}")
                days_in_month = df[df['Month'] == selected_month]['Day'].value_counts().sort_index()
                fig_days = px.bar(days_in_month, x=days_in_month.index, y=days_in_month.values,
                                labels={'x': 'Day', 'y': 'Total Orders'},
                                title=f"Total Orders per Day in Month {selected_month}")
                #fig_days.update_traces(marker_color='yellow')
                st.plotly_chart(fig_days)

                # Day selection for time breakdown
                selected_day = st.selectbox("Select a Day", sorted(monthData[selected_month].keys()), format_func=lambda x: f"Day {x}")
                if selected_day:
                    # Filter data for the selected day and plot orders per time
                    st.subheader(f"Order Times on {selected_month}-{selected_day}")
                    times_in_day = df[(df['Month'] == selected_month) & (df['Day'] == selected_day)]['Time'].value_counts().sort_index()
                    fig_times = px.bar(times_in_day, x=times_in_day.index, y=times_in_day.values,
                                    labels={'x': 'Time', 'y': 'Order Count'},
                                    title=f"Order Times on {selected_month}-{selected_day}")
                    #fig_times.update_traces(marker_color='yellow')
                    st.plotly_chart(fig_times)

for i in dataPaths:
    with open(i, encoding="ISO-8859-1") as f:
        pastLineNum = ''
        f.readline()
        lines = f.readlines()
        for line in lines:
            iterations = 0
            
            line = line.strip().split(',')
            
            if line[0] == pastLineNum or pastLineNum == '': #If its the same order, add it to the orderlist
                pastLineNum = line[0]
                orderList[orderNum].append(line)
            else: #if its a new order, make a new empty list and put the line inside
                orderNum += 1
                pastLineNum = line[0]
                orderList.append([])
                orderList[orderNum].append(line)
        #Now Go through each order and make a list of the orders and how many people bought

# Counts the number of meals
#Find the date trends in the data aswell
#Make a point graph, highlight specific high times/days
#Already have month, sort by days and times
for orders in orderList:
    for items in orders:
        if items[3] == 'Choose Your Drink':
            if items[4] in mealDict:
                mealDict[items[4]] += 1
            else:
                mealDict[items[4]] = 1
            
            # Get month and day as strings
            month = (items[1])[5:7]
            day = (items[1])[8:10]
            time = (items[1])[-8:]

            # Initialize month and day in monthData dictionary if they don't exist
            if month not in monthData:
                monthData[month] = {}
            if day not in monthData[month]:
                monthData[month][day] = []

            # Append the time to the corresponding month and day
            monthData[month][day].append(time)
            
            
# Finds the # of toppings
for orders in orderList:
    for items in orders:
        if items[3] == 'Choose Your Toppings' and items[4] == 'Mac and Cheese':
            if items[2] in toppingDict:
                toppingDict[items[2]] += 1
    
            else:
                toppingDict[items[2]] = 1

#Find the diffrent 'Bowls'
#Take the enitre combination of orders
for orders in orderList:
    tempName = ''
    for items in orders:
        if items[3] == 'Choose Your Drink':
            if tempName in bowlDict:
                bowlDict[tempName] += 1
            else:
                bowlDict[tempName] = 1
            tempName = ''
        else:
            #Take the item, add it to the bowl, unless a special order
            optionList = ['Choose Your Toppings', 'Noods', 'Choose Your Cheese', 'Choose Your Meats', 'Choose Your Drizzles']
            if items[3] in optionList:
                #If it is in the list, combine it with the current order
                tempName += items[2] + ' '
del bowlDict['']



#Silly tests
print(mealDict)
print(toppingDict)
#print(monthData)
streamLitRun(mealDict,toppingDict,bowlDict)