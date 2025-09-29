import pandas as pd
import plotly.graph_objects as go

# Load the logged data
log_file = "/home/helgi-runar/Downloads/resource_usage_log.csv"
df = pd.read_csv(log_file)

# Convert timestamp to datetime
df["Timestamp"] = pd.to_datetime(df["Timestamp"])

# Create an interactive line plot
fig = go.Figure()

# Add CPU usage trace
fig.add_trace(
    go.Scatter(
        x=df["Timestamp"], y=df["CPU_Usage(%)"], mode="lines", name="CPU Usage", hoverinfo="x+y", line=dict(width=2)
    )
)

# Add RAM usage trace
fig.add_trace(
    go.Scatter(
        x=df["Timestamp"], y=df["RAM_Usage(MB)"], mode="lines", name="RAM Usage", hoverinfo="x+y", line=dict(width=2)
    )
)

# Add GPU usage trace
fig.add_trace(
    go.Scatter(
        x=df["Timestamp"], y=df["GPU_Usage(%)"], mode="lines", name="GPU Usage", hoverinfo="x+y", line=dict(width=2)
    )
)

# Add GPU Memory trace
fig.add_trace(
    go.Scatter(
        x=df["Timestamp"], y=df["GPU_Memory(MB)"], mode="lines", name="GPU Memory", hoverinfo="x+y", line=dict(width=2)
    )
)

# Customize layout
fig.update_layout(
    title="System Resource Usage Over Time",
    xaxis_title="Timestamp",
    yaxis_title="Usage",
    hovermode="x unified",
    template="plotly_dark",
    xaxis=dict(showgrid=True),
    yaxis=dict(showgrid=True),
)

# Show interactive plot
fig.show()
