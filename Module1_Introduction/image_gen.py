import matplotlib.pyplot as plt
import numpy as np
import json

# # Your statistical data
with open('vocabulary_usage_frequencies.json', 'r') as f:
    data = json.load(f)

# Prepare data for plotting
words = list(data.keys())
explicit_counts = [data[word]["explicit_count"] for word in words]
implicit_counts = [data[word]["implicit_count"] for word in words]

x = np.arange(len(words))  # label locations
width = 0.35  # width of the bars

fig, ax = plt.subplots(figsize=(14, 6))
rects1 = ax.bar(x - width/2, explicit_counts, width, label='Explicit', color='skyblue')
rects2 = ax.bar(x + width/2, implicit_counts, width, label='Implicit', color='salmon')

# Add labels, title, and custom x-axis tick labels
ax.set_ylabel('Frequency')
ax.set_title('Explicit and Implicit Usage Frequencies of Vocabulary Words')
ax.set_xticks(x)
ax.set_xticklabels(words, rotation=45, ha='right')
ax.legend()

# Add value labels on top of bars
def autolabel(rects):
    for rect in rects:
        height = rect.get_height()
        if height > 0:
            ax.annotate('{}'.format(height),
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom')

autolabel(rects1)
autolabel(rects2)

fig.tight_layout()
plt.savefig('vocabulary_usage_frequencies.png', dpi=300)