from urllib import request

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
from flask import Flask, send_file, render_template

app = Flask(__name__)
print("Hello, world!!")
x = 5 + 5
print(x)

a = np.array([2, 3, 4])
print(a.mean())


import numpy as np
import matplotlib.pyplot as plt

# Reproducibility
np.random.seed(42)

# Underlying true function
x_true = np.linspace(0, 10, 400)
y_true = np.sin(x_true)

fig, axes = plt.subplots(1, 2, figsize=(12, 4))

# =========================================================
# Aleatoric Uncertainty
# Same function + noisy observations everywhere
# =========================================================
ax = axes[0]

# Data sampled across entire domain
x = np.linspace(0, 10, 80)
y = np.sin(x) + np.random.normal(0, 0.35, size=len(x))

# Plot
ax.plot(x_true, y_true, color="black", linewidth=2)
ax.scatter(x, y, alpha=0.7, s=25)
ax.set_title("Aleatoric Uncertainty")
ax.text(5, -2.7, "Noise in the observations → data uncertainty ", ha="center", fontsize=11)

# Styling
ax.set_xticks([])
ax.set_yticks([])

# =========================================================
# Epistemic Uncertainty
# Missing data regions
# =========================================================
ax = axes[1]

# Data only in some regions
x_left = np.linspace(0, 3.5, 30)
x_right = np.linspace(6.5, 10, 30)
x_sparse = np.concatenate([x_left, x_right])
y_sparse = np.sin(x_sparse) + np.random.normal(0, 0.1, size=len(x_sparse))

# Plot true function
ax.plot(x_true, y_true, color="black", linewidth=2)

# Plot observed points
ax.scatter(x_sparse, y_sparse, alpha=0.7, s=25)

# Highlight unknown region
ax.axvspan(3.5, 6.5, alpha=0.15)
ax.text(5, -1.7, "Lack of data → model uncertainty", ha="center", fontsize=11)
ax.set_title("Epistemic Uncertainty")

# Styling
ax.set_xticks([])
ax.set_yticks([])

# Clean look
for ax in axes:
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

plt.tight_layout()
plt.savefig("/workspaces/py-container/plot3.svg")
plt.close()
@app.route("/")
def hello():
    print(request.url_root)
    print(request.script_root)
    return render_template('index.html')

@app.route("/bye")
def bye():
    return "Please leave"

@app.route("/plot")
def plot():
    # generate the plot
    x = np.linspace(0, 2 * np.pi, 100)
    y = np.sin(x)

    plt.figure()
    plt.plot(x, y)
    plt.title("Sine Wave")
    plt.xlabel("x")
    plt.ylabel("sin(x)")

    # save it to a memory buffer instead of a file
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    plt.savefig("/workspaces/py-container/plot2.png")
    buf.seek(0)
    plt.close()


    return send_file(buf, mimetype="image/png")


if __name__ == "__main__":
    app.run( port=5000) # Sets hosts