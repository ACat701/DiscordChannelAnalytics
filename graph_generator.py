# TODO: Add Total Count
# TODO: Make it so that the line goes back down to 0 on days with no messages
import json
import zipfile

import easygui
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import pylab

# -- Global Variables --
package_filepath = "package.zip"
channel_id = easygui.enterbox(msg="Please paste the user's channel id :>", title='User ID', default='', strip=True, image=None, root=None)
graph_title = 'Message Data for ' + easygui.enterbox(msg="✨ What's their nickname? ✨", title='Nickname', default='', strip=True, image=None, root=None)
json_filepath = f"messages/" + "c" + channel_id + "/messages.json"

x_values = [] # X = Timestamp
y_values = [] # Y = Message Count

# Formatting hell!
plt.rcParams["font.family"] = "Arial Rounded MT Bold"
# Nord Colors :>
bg_color = '#2e3440'
line_color = '#5e81ac'
face_color = "#3b4252"
tick_color = '#8fbcbb'
label_color = '#88c0d0'
line_width_px = 2;
window_size = (13, 7)
# -- Global Variables --

# Import and Extract that zipfile. This makes a new folder and saves it to the location that this file is run from
with zipfile.ZipFile(package_filepath, 'r') as zip_ref:
    zip_ref.extract(json_filepath)

# Get contents of json from that given person
with open(json_filepath, 'r', encoding="utf8") as file:
        data = json.load(file)

# Fill the arrays with our values
for message in data:
    timestamp = message["Timestamp"][:10]
    
    if len(x_values) == 0:
        x_values.append(message["Timestamp"][:10])
        y_values.append(1)
        continue

    if x_values[len(x_values) - 1] == timestamp:
        y_values[len(x_values) - 1] += 1
        continue
    
    x_values.append(message["Timestamp"][:10])
    y_values.append(1)

# Understanding from here gets partially thrown out of the window
x_values = np.asarray(x_values, dtype='datetime64[s]')

fig, ax = plt.subplots(layout='constrained', figsize=window_size, facecolor=(bg_color))  # TODO: UNDERSTAND THIS LINE
fig = pylab.gcf() # TODO: UNDERSTAND THIS LINE

# Create the Line itself 
ax.plot(x_values, y_values, color=line_color, lw=line_width_px)

# Name our Graph
fig.canvas.manager.set_window_title(graph_title)
plt.title(graph_title, loc='center', color=label_color)

# Hide the "box" around the graph
ax.spines.left.set_visible(False)
ax.spines.right.set_visible(False)
ax.spines.top.set_visible(False)
ax.spines.bottom.set_visible(False)

# -- X Axis --
ax.set_facecolor(face_color)
ax.tick_params(color=tick_color, which='both', labelcolor=label_color) 

ax.xaxis.set_major_formatter(mdates.DateFormatter('%d'))
ax.xaxis.set_minor_locator(ticker.MultipleLocator(2))

# Secondary Axis (Months)
# TODO: UNDERSTAND ALL OF THIS BC RUHMIT DID IT
sec = ax.secondary_xaxis(location=-0.03)
sec.xaxis.set_major_locator(mdates.MonthLocator(bymonthday=1))
sec.xaxis.set_major_formatter(mdates.DateFormatter('  %b'))

sec.tick_params('x', length=0, labelcolor=tick_color)
sec.spines['bottom'].set_linewidth(0) 
# -- X Axis --

# Y Axis
plt.ylabel("Message Count", color=label_color)

# Display graph
plt.show()