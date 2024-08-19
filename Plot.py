import pandas as pd
import plotly.graph_objects as go


# For aggregated topic counts
rolling_mean_param = 4
crypto_token = "ethereum"

df_agg = pd.read_excel("./" + crypto_token + "_agg.xlsx", header=0)

df_agg.set_index('datetime', inplace=True)


# Calculate the moving averages (12 timestamps)
df_agg['Positive_MA'] = df_agg['Positive_Percentage'].rolling(window=rolling_mean_param).mean()
df_agg['Neutral_MA'] = df_agg['Neutral_Percentage'].rolling(window=rolling_mean_param).mean()
df_agg['Negative_MA'] = df_agg['Negative_Percentage'].rolling(window=rolling_mean_param).mean()

# Create the plot
fig = go.Figure()

# Add the positive line (green)
fig.add_trace(go.Scatter(x=df_agg.index, y=df_agg['Positive_Percentage'],
                         mode='lines', name='Positive',
                         line=dict(color='green')))

# Add the positive moving average line (green, dotted)
fig.add_trace(go.Scatter(x=df_agg.index, y=df_agg['Positive_MA'],
                         mode='lines', name=f'Positive MA ({rolling_mean_param})',
                         line=dict(color='green', dash='dot')))

# Add the neutral line (brown)
fig.add_trace(go.Scatter(x=df_agg.index, y=df_agg['Neutral_Percentage'],
                         mode='lines', name='Neutral',
                         line=dict(color='brown')))

# Add the neutral moving average line (brown, dotted)
fig.add_trace(go.Scatter(x=df_agg.index, y=df_agg['Neutral_MA'],
                         mode='lines', name=f'Neutral MA ({rolling_mean_param})',
                         line=dict(color='brown', dash='dot')))

# Add the negative line (red)
fig.add_trace(go.Scatter(x=df_agg.index, y=df_agg['Negative_Percentage'],
                         mode='lines', name='Negative',
                         line=dict(color='red')))

# Add the negative moving average line (red, dotted)
fig.add_trace(go.Scatter(x=df_agg.index, y=df_agg['Negative_MA'],
                         mode='lines', name=f'Negative MA ({rolling_mean_param})',
                         line=dict(color='red', dash='dot')))

# Update layout to include titles and range slider
fig.update_layout(
    title='Sentiment Analysis Over Time with Moving Averages',
    xaxis_title='Date/Time',
    yaxis_title='Percentage',
    xaxis=dict(
        rangeslider=dict(
            visible=True
        ),
        type="date"
    ),
    template='plotly'
)

# Show the plot
fig.show()