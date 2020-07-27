from skm_pyutils.py_plot import ColorManager, GroupManager
import seaborn as sns

if __name__ == "__main__":
    sns.set_style("white")

    l = ["CLA"] * 8 + ["ACC"] * 4 + ["RSC"] * 4 + ["hi"] * 4 + ["bye"] * 4 + ["k"] * 4
    gm = GroupManager(l)
    gm.test_plot()
    # cm = ColorManager(400, "sns", sns_style="Blues")
    # cm.test_plot()
