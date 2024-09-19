import streamlit as st
import pandas as pd
import plotly.express as px

# Load data from the provided URL
path = "https://linked.aub.edu.lb/pkgcube/data/b49644dfb203975571146f1ff8d4fee1_20240907_152325.csv"
df = pd.read_csv(path)

# Title of the Streamlit Page
st.title("Social Data Insights and Visualizations")

# Add a subheader for the introduction
st.subheader("Introduction")

# Write a description of the purpose of the analysis
st.write("""
This dashboard presents an analysis of social demographic data across various towns. 
The visualizations included aim to provide insights into key metrics such as gender distribution, family sizes, 
and the elderly population. These insights are essential for understanding the social structure of the towns and can 
support community planning, resource allocation, and policy-making efforts.
""")

# Explain the dataset you're working with
st.write("""
**Data Source:** The dataset contains demographic information for various towns, including gender breakdowns, 
average family sizes, and elderly population percentages. The data is crucial for analyzing social patterns and trends within communities.
""")

# Dataset Overview Section
st.subheader("Dataset Overview")


# Show basic statistics of the dataset (optional, but useful for context)
st.write("Here are some summary statistics of the key metrics in the dataset:")
st.write(df.describe())

# Highlight key columns in the dataset for context
st.write("""
The dataset includes the following columns:
- **Town**: The name of the town.
- **Percentage of Women**: The percentage of women in the town.
- **Percentage of Men**: The percentage of men in the town.
- **Average Family Size**: The average family size, broken down by categories (1-3 members, 4-6 members, 7 or more members).
- **Percentage of Elderly (65+ years)**: The percentage of elderly people in the town.
""")

# Mention what the next sections will cover
st.write("""
In the sections below, we will explore two key aspects of the data:
1. **Gender Distribution Across Towns**: A bar chart showing the gender breakdown (percentage of men and women) across the towns.
2. **Average Family Size vs. Elderly Population**: A scatter plot analyzing the relationship between average family sizes and the percentage of elderly people in each town.
""")

# Clean up the column names by stripping any leading or trailing spaces
df.columns = df.columns.str.strip()

# Select the number of towns to display (Slider)
num_towns = st.slider('Number of towns to display', min_value=10, max_value=70, value=70, step=10)

# Extract relevant columns for plotting
town = df['Town'][:num_towns]
percentage_women = df['Percentage of Women'][:num_towns]
percentage_men = df['Percentage of Men'][:num_towns]

# Create the bar plot using Plotly Express
df_plot = pd.DataFrame({
    'Town': town,
    'Percentage of Women': percentage_women,
    'Percentage of Men': percentage_men
})

# Melt the data to a long format for easier plotting with Plotly Express
df_melted = df_plot.melt(id_vars='Town', var_name='Gender', value_name='Percentage')

# Create the bar plot
fig = px.bar(df_melted, x='Town', y='Percentage', color='Gender', 
             barmode='group', title='Gender by Town')

# Update layout for better display
fig.update_layout(xaxis_tickangle=-90, xaxis_title='Town', yaxis_title='Percentage')

# Display the plot using Streamlit
st.plotly_chart(fig)

# Strip any leading or trailing spaces in column names
df.columns = df.columns.str.strip()

# Calculate the average family size using weighted sums
df['Average family size'] = (
    1.5 * df['Average family size - 1 to 3 members'] + 
    5 * df['Average family size - 4 to 6 members'] + 
    7 * df['Average family size - 7 or more members']
    ) / (
        df['Average family size - 1 to 3 members'] +
        df['Average family size - 4 to 6 members'] +
        df['Average family size - 7 or more members']
    )

# Allow the user to select specific towns
selected_towns = st.multiselect(
    'Select towns to annotate on the scatter plot:', 
    options=df['Town'].unique(),
    default=['Aain El Saydeh', 'Aabadiyeh', 'Aachqout', 'Khreibet Baabda', 'Aabdine', 'Fourzol']
)

# Extract relevant columns for the plot
df_plot = df[['Town', 'Average family size', 'Percentage of Eldelry - 65 or more years']]

# Create the scatter plot using Plotly Express
fig = px.scatter(
    df_plot, 
    x='Average family size', 
    y='Percentage of Eldelry - 65 or more years', 
    hover_name='Town',  # Display town names on hover
    title='Scatter Plot of Average Family Size vs. Percentage of Eldelry',
    labels={'Average family size': 'Average Family Size', 'Percentage of Eldelry - 65 or more years': 'Percentage of Elderly (65 or more years)'},
    color_discrete_sequence=['blue'],
    opacity=0.6
)

# Annotate selected towns with custom markers
for town in selected_towns:
    town_data = df_plot[df_plot['Town'] == town]
    fig.add_scatter(
        x=town_data['Average family size'], 
        y=town_data['Percentage of Eldelry - 65 or more years'], 
        mode='markers+text',
        text=town_data['Town'], 
        textposition='top right',
        marker=dict(size=10, color='red', line=dict(color='pink', width=2)), 
        showlegend=False
    )

# Display the plot in Streamlit
st.plotly_chart(fig)



# Sample data (replace this with your actual data or file uploader)
data = {
    'Town': ['Town A', 'Town B', 'Town C'],
    'Percentage of Women': [55, 60, 65],
    'Percentage of Men': [45, 40, 35]
}
df = pd.DataFrame(data)

# Streamlit form for selecting a row
with st.form(key='my_form'):
    st.write("Select a town to view gender distribution:")
    
    # Dropdown to select the town (row)
    selected_town = st.selectbox("Select Town", df['Town'])

    # Submit button
    submit_button = st.form_submit_button(label='Show Distribution')

# Action when the form is submitted
if submit_button:
    # Get the selected row based on the town name
    selected_row = df[df['Town'] == selected_town].iloc[0]
    
    # Prepare data for the pie chart
    pie_data = pd.DataFrame({
        'Gender': ['Women', 'Men'],
        'Percentage': [selected_row['Percentage of Women'], selected_row['Percentage of Men']]
    })

    # Create the pie chart using Plotly Express
    fig = px.pie(
        pie_data, 
        values='Percentage', 
        names='Gender', 
        title=f"Gender Distribution in {selected_row['Town']}",
        color_discrete_map={'Women': 'pink', 'Men': 'blue'},
        hole=0.4,  # Create a donut-style pie chart if needed
    )

    # Display the plot in Streamlit
    st.plotly_chart(fig)
    


# Strip any leading or trailing spaces from column names
df.columns = df.columns.str.strip()

# Bar Chart: Percentage of Women, Men, Youth, and Eldelry by Town
st.write("### Gender and Age Distribution by Town")

# Select which percentages to show
selected_columns = st.multiselect(
    'Select data to visualize:', 
    options=['Percentage of Women', 'Percentage of Men', 'Percentage of Youth - 15-24 years', 'Percentage of Eldelry - 65 or more years'],
    default=['Percentage of Women', 'Percentage of Men']
)

# Plot the selected columns for each town
df_plot = df[['Town'] + selected_columns]
df_plot = df_plot.melt(id_vars='Town', var_name='Category', value_name='Percentage')

fig = px.bar(df_plot, x='Town', y='Percentage', color='Category', 
             title='Distribution by Town', barmode='group')

# Display the chart
st.plotly_chart(fig)

# Scatter Plot: Average Family Size vs. Percentage of Youth or Eldelry
st.write("### Average Family Size vs. Percentage of Youth or Eldelry")

# Let the user select between youth or elderly for the scatter plot
age_group = st.radio("Select the age group:", 
                     ('Percentage of Youth - 15-24 years', 'Percentage of Eldelry - 65 or more years'))

# Calculate the average family size
df['Average family size'] = (
    1.5 * df['Average family size - 1 to 3 members'] + 
    5 * df['Average family size - 4 to 6 members'] + 
    7 * df['Average family size - 7 or more members']
    ) / (
        df['Average family size - 1 to 3 members'] +
        df['Average family size - 4 to 6 members'] +
        df['Average family size - 7 or more members']
    )

# Create scatter plot
fig_scatter = px.scatter(
    df, x='Average family size', y=age_group, hover_name='Town', 
    title=f'Average Family Size vs. {age_group}', 
    labels={'Average family size': 'Average Family Size', age_group: age_group},
    color='Town'
)

# Display the scatter plot
st.plotly_chart(fig_scatter)
