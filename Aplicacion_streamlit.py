import streamlit as st
import pandas as pd
import plotly.express as px

ufc_final = pd.read_csv('ufc_top35_stats.csv')

st.title("UFC Top 35 Fighters")
st.markdown("### Ranking and Stats for the top MMA fighters")

st.sidebar.title("Graphs")
graph_option = st.sidebar.radio(
    "Select a graph to display:",
    ('Fighters per Weightclass', 'Striking defence vs Weight', 'Takedown Accuracy vs Takedown Defense', 'Strikes Landed vs Takedowns Landed')
)

st.markdown("### TOP 35")
top_35 = ufc_final[['ID','Fighter', 'Record', 'height_cm', 'weight_in_kg', 'weightclass']]
st.dataframe(top_35) 

st.markdown("<h2 style='text-align: center;'>Selected Graph</h2>", unsafe_allow_html=True)
if graph_option == 'Fighters per Weightclass':
    weightclass_counts = ufc_final['weightclass'].value_counts().reset_index()
    weightclass_counts.columns = ['Weightclass', 'Number of Fighters']
    bar_chart = px.bar(
        weightclass_counts,
        x='Weightclass',
        y='Number of Fighters',
        title='Number of Fighters per Weight Class',
        labels={'Weightclass': 'Weight Class', 'Number of Fighters': 'Number of Fighters'},
        template='plotly_white',
        color_discrete_sequence=['red']
    )
    st.plotly_chart(bar_chart, use_container_width=True)

elif graph_option == 'Striking defence vs Weight':
    scatter_fig = px.scatter(
        ufc_final,
        x='weight_in_kg',
        y='significant_strike_defence',
        hover_name='Fighter',
        title='Weight vs Striking Defence',
        labels={'weight_in_kg': 'Weight (kg)', 'significant_strike_defence': 'Striking Defence (%)'},
        template='plotly_white'
    )
    scatter_fig.update_layout(
        width=900,
        height=600,
        xaxis=dict(title='Weight (kg)', range=[ufc_final['weight_in_kg'].min() - 5, ufc_final['weight_in_kg'].max() + 5]),
        yaxis=dict(title='Striking Defence (%)', range=[ufc_final['significant_strike_defence'].min() - 5, ufc_final['significant_strike_defence'].max() + 5])
    )
    scatter_fig.update_traces(marker=dict(size=10, opacity=0.8))
    st.plotly_chart(scatter_fig, use_container_width=True)

elif graph_option == 'Takedown Accuracy vs Takedown Defense':
    scatter_fig2 = px.scatter(
        ufc_final,
        x='takedown_accuracy',
        y='takedown_defense',
        hover_name='Fighter', 
        title='Takedown Accuracy vs Takedown Defense',
        labels={'takedown_accuracy': 'Takedown Accuracy (%)', 'takedown_defense': 'Takedown Defense (%)'},
        template='plotly_white'
    )
    scatter_fig2.update_layout(
        width=900,
        height=600,
        xaxis=dict(title='Takedown Accuracy (%)', range=[ufc_final['takedown_accuracy'].min() - 5, ufc_final['takedown_accuracy'].max() + 5]),
        yaxis=dict(title='Takedown Defense (%)', range=[ufc_final['takedown_defense'].min() - 5, ufc_final['takedown_defense'].max() + 5])
    )
    scatter_fig2.update_traces(marker=dict(size=10,color='green'))
    st.plotly_chart(scatter_fig2, use_container_width=True)

elif graph_option == 'Strikes Landed vs Takedowns Landed':
    scatter_fig = px.scatter(
        ufc_final,
        x='significant_strikes_landed_per_minute',
        y='average_takedowns_landed_per_15_minutes',
        color='weightclass', 
        hover_name='Fighter',  
        title='Strikes Landed vs Takedowns Landed',
        labels={
            'significant_strikes_landed_per_minute': 'Strikes Landed',
            'average_takedowns_landed_per_15_minutes': 'Takedowns Landed',
            'weightclass': 'Weight Class'
        },
        template='plotly_white'
    )
    scatter_fig.update_layout(
        width=900,
        height=600,
        xaxis=dict(title='Strikes Landed'),
        yaxis=dict(title='Takedowns Landed')
    )
    scatter_fig.update_traces(marker=dict(size=10))
    st.plotly_chart(scatter_fig, use_container_width=True)

selected_fighter = st.selectbox(
    "Select a fighter for more details",
    top_35['Fighter']
)
if selected_fighter:
    st.markdown(f"## {selected_fighter} stats")
    fighter_stats = ufc_final[ufc_final['Fighter'] == selected_fighter].iloc[0]

    st.write(f"**Nickname:** {fighter_stats['nickname']}")
    st.write(f"**Record:** {fighter_stats['Record']}")
    st.write(f"**Height:** {fighter_stats['height_cm']} cm")
    st.write(f"**Weight:** {fighter_stats['weight_in_kg']} kg")
    st.write(f"**Points:** {fighter_stats['Points']}")
    st.write(f"**Date of birth:** {fighter_stats['date_of_birth']}")
    st.write(f"**Weight Class:** {fighter_stats['weightclass']}")
    
    st.markdown("### Striking stats")
    st.write(f"**Significant strikes landed per minute:** {fighter_stats['significant_strikes_landed_per_minute']}")
    st.write(f"**Significant strikes accuracy:** {fighter_stats['significant_striking_accuracy']}%")
    st.write(f"**Significant strikes absorbed per minute:** {fighter_stats['significant_strikes_absorbed_per_minute']}")
    st.write(f"**Significant strikes defense accuracy:** {fighter_stats['significant_strike_defence']}%")

    st.markdown("### Takedown Stats")
    st.write(f"**Takedowns landed per 15 minutes:** {fighter_stats['average_takedowns_landed_per_15_minutes']}")
    st.write(f"**Takedown accuracy:** {fighter_stats['takedown_accuracy']}%")
    st.write(f"**Takedown defense:** {fighter_stats['takedown_defense']}%")

    st.markdown("### Submission stats")
    st.write(f"**Submissions attempted per 15 minutes:** {fighter_stats['average_submissions_attempted_per_15_minutes']}")


        
