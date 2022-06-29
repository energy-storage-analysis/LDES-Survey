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

def adjust_text_after(fig, ax, alter_name, texts, x, y):
    text_strings = [t.get_text().strip("$") for t in texts]
    text_pos = text_strings.index(alter_name)

    text_obj = texts[text_pos]
    
    if x != None: text_obj.set_x(x)
    if y != None: text_obj.set_y(y)
    r = fig.canvas.renderer
    bbox = get_bboxes([text_obj] , r, (1, 1), ax)[0]
    cx, cy = get_midpoint(bbox)

    child_slot_alter = len(texts)+1+text_pos
    arrow = ax.get_children()[child_slot_alter]
    arrow.set_x(cx)
    arrow.set_y(cy)