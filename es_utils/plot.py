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

def get_text_index_from_name(text_strings, text_string):
    
    text_index = text_strings.index(text_string)
    return text_index

def adjust_text_after(fig, ax, alter_name, texts, x, y):
    """
    This function can be called after automatically setting text labels with adjustText package to manually set a given labels postion
    Takes in axes coordinates to place text labels at
    """

    text_strings = [t.get_text().strip("$") for t in texts]

    axis_to_data = (ax.transAxes + ax.transData.inverted()).transform
    trans_to_data = ax.transData.inverted().transform

    x, y = axis_to_data((x,y))

    if alter_name not in text_strings:
        print("Didn't find {} in texts, skipping".format(alter_name))
    else:

        text_index = get_text_index_from_name(text_strings, alter_name)
        text_obj = texts[text_index]
        
        if x != None: text_obj.set_x(x)
        if y != None: text_obj.set_y(y)
        r = fig.canvas.renderer
        bbox = get_bboxes([text_obj] , r, (1, 1), ax)[0]
        cx, cy = get_midpoint(bbox)

        cx, cy=trans_to_data(get_midpoint(bbox))

        #TODO: This is a hacky way to try and find the corresponding arrow to the text box 
        child_slot_alter = len(texts)+text_index
        children_text_only = [c for c in ax.get_children() if isinstance(c, Text)]
        arrow = children_text_only[child_slot_alter]
        arrow.set_x(cx)
        arrow.set_y(cy)



from adjustText import get_renderer
def draw_arrows(texts, arrowprops, ax, orig_xy, *args, **kwargs):

    r = get_renderer(ax.get_figure())
    bboxes = get_bboxes(texts, r, (1, 1), ax)
    # kwap = kwargs.pop('arrowprops')

    trans_to_data = ax.transData.inverted().transform

    arrows = []
    for j, (bbox, text) in enumerate(zip(bboxes, texts)):
        ap = {'patchA':text} # Ensure arrow is clipped by the text
        ap.update(arrowprops)
        # ap.update(kwap) # Add arrowprops from kwargs

        xy = trans_to_data(orig_xy[j])
        # xy = orig_xy[j]
        xytext=trans_to_data(get_midpoint(bbox))

        arrow = ax.annotate("", # Add an arrow from the text to the point
                    xy = (xy),
                    xytext=xytext,
                    arrowprops=ap,
                    *args, **kwargs)
        arrows.append(arrow)

    return arrows


from adjustText import get_text_position

import pandas as pd

def gen_text_position_fix_csv(df_text_pos, texts, ax):

    text_strings = [t.get_text().strip("$") for t in texts]

    trans_to_data = ax.transAxes.inverted().transform
    
    for i, text in enumerate(texts):
        t_x, t_y = get_text_position(text, ax)
        a_x, a_y = trans_to_data((t_x, t_y))

        text_idx = text_strings[i]

        df_text_pos.loc[text_idx,'x'] = a_x 
        df_text_pos.loc[text_idx,'y'] = a_y
        df_text_pos.loc[text_idx,'ha'] = text.get_ha() 
        df_text_pos.loc[text_idx,'va'] = text.get_va()

    return df_text_pos

def combine_fix_pos(df_SM, df_text_position):
    df1 = df_SM.reset_index()[['display_text']]
    df_text_position = pd.merge(df1, df_text_position, on='display_text').set_index('display_text')
    # df_text_position['fix'] = ''
    # df_text_position = df_text_position.sort_values('y', ascending=False)
    # df_text_position = df_text_position.round(4)
    return df_text_position

def get_text_position_data(text, ax):
    x, y = text.get_position()
    x = ax.convert_xunits(x)
    y = ax.convert_yunits(y)
    # t_x, t_y = text.get_transform().transform((x, y))
    t_x, t_y = x , y
    return (t_x, t_y)


def prepare_fixed_texts(texts, fix_positions, ax):
    # form the lists of fixed texts, adjustable texts, and their original xy positions. Having to do weird things to keep the order in the lists matching, probably a better way to handle this.
    texts_fix = []
    orig_xy_fixed = []

    axis_to_data = ax.transAxes + ax.transData.inverted()

    for name, row in fix_positions.iterrows():

        if row['fix'] != 'y':
            continue

        text_strings = [t.get_text().strip("$") for t in texts]

        if name not in text_strings:
            print("Didn't find {} in texts, skipping".format(name))
            continue

        index = get_text_index_from_name(text_strings, name)
        text_to_fix = texts.pop(index)
        orig_xy_fixed.append(get_text_position(text_to_fix, ax=ax))
        
        fix_tup= (row['x'],row['y'])

        

        fix_tup_data = axis_to_data.transform(fix_tup)

        text_to_fix.set_va(row['va'])
        text_to_fix.set_ha(row['ha'])

        text_to_fix.set_x(fix_tup_data[0])
        text_to_fix.set_y(fix_tup_data[1])



        texts_fix.append(text_to_fix)

    orig_xy = [get_text_position(text, ax=ax) for text in texts]
    return texts, texts_fix, orig_xy, orig_xy_fixed


def gen_legend_figure(style_dict, title, style_type='linestyle', figsize=(0.75,0.75)):
    fig = plt.figure("Line plot")
    legendFig = plt.figure("Legend plot {}".format(title), figsize=figsize)
    ax = fig.add_subplot(111)

    lns = []
    for info_val, info_style in style_dict.items():
        if style_type == 'linestyle':
            line1, = ax.plot([0], [0], c="black", lw=1, linestyle=info_style)
        elif style_type == 'color':
            line1, = ax.plot([0], [0], c=info_style, lw=1)
        else:
            raise ValueError("Style type must be 'linestyle' or 'color'")
        lns.append(line1)

    legendFig.legend(lns, style_dict.keys(), loc='center', title=title)

    legendFig.tight_layout()
    return legendFig