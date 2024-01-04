from flask import Flask, send_file
import matplotlib.pyplot as plt
from io import BytesIO
import pandas as pd

def generate_combined_plot(data, x_column, y_columns, title):
    plt.figure(figsize=(10, 6))
    
    # Create subplots with shared x-axis
    fig, axs = plt.subplots(len(y_columns), sharex=True, figsize=(10, 6))
    fig.suptitle(title)

    # Plot each graph in a separate subplot
    for i, y_column in enumerate(y_columns):
        axs[i].plot(data[x_column], data[y_column], label=y_column)
        axs[i].grid(True)
        axs[i].legend()

    # Set common labels
    axs[-1].set_xlabel('Date')

    # Save the plot to a BytesIO object
    plot_buffer = BytesIO()
    plt.savefig(plot_buffer, format='png', dpi=300)
    plot_buffer.seek(0)

    # Close the plot to free up resources
    plt.close()

    # Return the plot as a response
    return plot_buffer

def generate_combined_image(sample_data):
    df = pd.DataFrame(sample_data)
    df['Date'] = pd.to_datetime(df['Date'])

    # Graphs to combine
    graph_columns = [
        ['Close', 'CloseEMA', 'Regression Lower Band', 'Regression Median', 'Regression Upper Band'],
        ['MACD', 'MACDSignal'],
        ['Volume', 'VolumeEMA'],
        ['RSI']
    ]

    # Titles for each graph
    graph_titles = ['Graph 1', 'Graph 2', 'Graph 3', 'Graph 4']

    # Generate combined plots
    combined_plots = []
    for i, columns in enumerate(graph_columns):
        plot = generate_combined_plot(df, 'Date', columns, graph_titles[i])
        combined_plots.append(plot)

    # Save combined plots to a zip file
    plots = {'combined_graphs.png': combined_plots[0]}  # Only saving the first combined graph

    # Create a zip file with the image
    zip_buffer = BytesIO()
    with pd.ExcelWriter(zip_buffer, engine='xlsxwriter') as writer:
        for filename, plot in plots.items():
            img = plt.imread(plot)
            df_img = pd.DataFrame(img)
            df_img.to_excel(writer, sheet_name=filename, header=False, index=False)
    
    zip_buffer.seek(0)

    # Return the zip file as a response
    return send_file(zip_buffer, mimetype='application/zip', as_attachment=True, download_name='combined_graphs.zip')