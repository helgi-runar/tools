import pandas as pd
import plotly.graph_objects as go


# Load process log
def load_process_log(file_path):
    process_df = pd.read_csv(file_path, usecols=["process", "process_runtime"])
    return process_df


# Plot function
def plot_runtime(process_df):
    fig = go.Figure()

    for process in process_df["process"].unique():
        subset = process_df[process_df["process"] == process]
        fig.add_trace(go.Scatter(x=subset.index, y=subset["process_runtime"], mode="lines+markers", name=process))

    fig.update_layout(
        title="Process Runtime Over Time",
        xaxis_title="Process Index",
        yaxis_title="Time (seconds)",
        hovermode="x unified",
    )
    fig.show()


# File path
process_log_file = "/home/helgi-runar/Downloads/test_log.txt"  # Replace with actual file path

# Execute
process_df = load_process_log(process_log_file)
plot_runtime(process_df)
