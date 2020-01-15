from skm_pyutils.py_plot import ColorManager
import seaborn as sns

if __name__ == "__main__":
    sns.set_style("white")
    cm = ColorManager(400, "sns", sns_style="Blues")
    cm.test_plot()
