import matplotlib.pyplot as plt

def annotate_points(df, x_col, y_col, text_col=None, ax=None):
    """
    Adds text annotations based on the x and y positions of a dataframe
    if text_col is None then the index is displayed
    """

    if ax==None:
        ax=plt.gca()

    texts = []
    for idx, row in df.iterrows():
        x = row[x_col]
        y = row[y_col]

        display_text = row[text_col] if text_col != None else idx

        txt= ax.text(x, y, "${}$".format(display_text))
        texts.append(txt)

    return texts