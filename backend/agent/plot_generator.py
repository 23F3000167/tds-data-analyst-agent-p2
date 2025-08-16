import matplotlib.pyplot as plt
import io
import base64

def generate_plot(data_dict):
    df = list(data_dict.values())[0]  # assume first file
    df = df.dropna(subset=["Rank", "Peak"])

    plt.figure()
    plt.scatter(df["Rank"], df["Peak"])
    m, b = np.polyfit(df["Rank"], df["Peak"], 1)
    plt.plot(df["Rank"], m * df["Rank"] + b, linestyle='dotted', color='red')
    plt.xlabel("Rank")
    plt.ylabel("Peak")
    
    buffer = io.BytesIO()
    plt.savefig(buffer, format="png", dpi=150)
    buffer.seek(0)
    img_base64 = base64.b64encode(buffer.read()).decode("utf-8")
    return f"data:image/png;base64,{img_base64}"
