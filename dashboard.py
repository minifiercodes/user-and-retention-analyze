import pandas as pd
import plotly.express as px
import plotly.graph_objs as go

# Load data from CSV file
df = pd.read_csv("bagikopi_website_data.csv")

# Create a figure with multiple subplots
fig = make_subplots(rows=2, cols=2, subplot_titles=("User Visits by Page", "Daily User Visits", "User Retention by Page", "Hourly User Visits"))

# Add trace for user visits by page
page_visits = df.groupby('page').count()['user_id']
fig.add_trace(go.Bar(x=page_visits.index, y=page_visits.values), row=1, col=1)

# Add trace for daily user visits
daily_visits = df.groupby(df.timestamp.dt.date).count()['user_id']
fig.add_trace(go.Scatter(x=daily_visits.index, y=daily_visits.values, mode='lines+markers'), row=1, col=2)

# Add trace for user retention by page
page_retention = df.groupby(['page', df.timestamp.dt.date]).nunique()['user_id'].reset_index()
fig.add_trace(go.Scatter(x=page_retention[page_retention['page'] == 'Menu']['timestamp'], y=page_retention[page_retention['page'] == 'Menu']['user_id'], mode='lines+markers', name='Menu'), row=2, col=1)
fig.add_trace(go.Scatter(x=page_retention[page_retention['page'] == 'Outlets']['timestamp'], y=page_retention[page_retention['page'] == 'Outlets']['user_id'], mode='lines+markers', name='Outlets'), row=2, col=1)

# Add trace for hourly user visits
hourly_visits = df.groupby([df.timestamp.dt.hour]).count()['user_id']
fig.add_trace(go.Scatter(x=hourly_visits.index, y=hourly_visits.values, mode='lines+markers'), row=2, col=2)

# Update figure layout
fig.update_layout(title="BagiKopi Website User Analysis Dashboard",
                  xaxis_title="Page/Dates/Hour of Day",
                  yaxis_title="Number of User Visits",
                  height=700,
                  width=1000)

# Display the dashboard
fig.show()
