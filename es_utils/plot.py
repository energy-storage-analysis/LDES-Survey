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


from adjustText import  get_bboxes, get_midpoint
from matplotlib.text import Text

def adjust_text_after(fig, ax, alter_name, texts, x, y):
    """
    This function can be called after automatically setting text labels with adjustText package to manually set a given labels postion
    """
    text_strings = [t.get_text().strip("$") for t in texts]
    text_pos = text_strings.index(alter_name)

    text_obj = texts[text_pos]
    
    if x != None: text_obj.set_x(x)
    if y != None: text_obj.set_y(y)
    r = fig.canvas.renderer
    bbox = get_bboxes([text_obj] , r, (1, 1), ax)[0]
    cx, cy = get_midpoint(bbox)

    #TODO: This is a hacky way to try and find the corresponding arrow to the text box 
    child_slot_alter = len(texts)+text_pos
    children_text_only = [c for c in ax.get_children() if isinstance(c, Text)]
    arrow = children_text_only[child_slot_alter]
    arrow.set_x(cx)
    arrow.set_y(cy)