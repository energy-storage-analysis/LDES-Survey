import pandas as pd
import camelot

def concat_row_to_columns(df: pd.DataFrame, column_rows: int):
    """set the top column_rows rows to the column headers """
    df_out = df.copy()

    df_out, df_out.columns = df[1:] , df.iloc[0]
    df_out = df_out.reset_index(drop=True)

    #If we requested more than the first column, then concatenate those 
    #TODO: too hacky
    column_rows = column_rows - 1
    if column_rows > 0:
        rows = range(column_rows)
        for row in rows:
            df_out.columns = df_out.columns.astype(str) + ' ' + df_out.loc[row].fillna('').values.astype(str)
            df_out = df_out.drop(row)

    return df_out

from PyPDF2 import PdfFileReader

def get_pdf_size(pdf_path, page, page_rotate):
    """
    Get pdf width and height
    the page rotate can be manually set to 90. Normally this is picked up by looking at the pages "/Rotate" property but this doesn't always seem to work. 
    """
    input1 = PdfFileReader(open(pdf_path, 'rb'))
    media_box = input1.getPage(page).mediaBox
    print(media_box)
    pdf_width = float(media_box[2])-float(media_box[0])
    pdf_height = float(media_box[3])-float(media_box[1])


    if page_rotate == None:
        page_rotate = input1.getPage(page).get("/Rotate")

    if page_rotate == 90:
        pdf_width, pdf_height = pdf_height, pdf_width
        
    return pdf_width, pdf_height


#TODO: handle other angles and consolidate with page rotation. It seems that the camelot and page rotation is confusing things. This is sort of a hotfix and I don't really know what is going on. 
def rotate_table(t):
    """Manually rotate the tabula template before processing. """
    
    x2 = float(t['x2'])
    y2 = float(t['y2'])

    t['y2'] = x2
    t['x2'] = y2

    return t

def extract_table_area(t, pdf_height):
    """extracts tabula template dict to data suitable for camelot"""
    
    table_area = [
        float(t['x1']),
        pdf_height - float(t['y1']),
        float(t['x2']),
        pdf_height- float(t['y2'])
        ]
    # table_area = [str(int(s)) for s in table_area]
    table_area = ['{},{},{},{}'.format(*table_area)]
    return table_area

def extract_dfs(pdf_path, table_settings):
    dfs = []
    for setting in table_settings:
        print("table on page {}".format(setting['template']['page']))
        template = setting['template']
        page = template['page']

        page_rotate = setting['page_rotate'] if 'page_rotate' in setting else None

        pdf_width, pdf_height = get_pdf_size(pdf_path, page + 1, page_rotate) #assumes all heights are same as page 1

        #Hotfix to rotate table, see comment above funciton. 
        table_rotate = setting['table_rotate'] if 'table_rotate' in setting else None
        if table_rotate != None:
            template = rotate_table(template)

        table_area = extract_table_area(template, pdf_height)
        camelot_kwargs = setting['camelot_kwargs']
        # columns = camelot_kwargs['columns'] if 'columns' in camelot_kwargs else None

        try:
            tables = camelot.read_pdf(pdf_path, pages=str(page), table_areas= table_area, **camelot_kwargs)

            df = tables[0].df

            df = df.replace(to_replace='e(\d)', value=r'-\1', regex=True)
            df = df.replace('\(cid:3\)', 'deg', regex=True)
            df = df.replace('\(cid:1\)', '-', regex=True)

        #Set first row as column for all, then concat for others. This keeps compatibility with tabula
            if 'column_rows' in setting:
                column_rows = setting['column_rows']

                df = concat_row_to_columns(df, column_rows)

        except Exception as e:
            print(e)
            print("Error, skipping and returning blank dataframe")
            df = pd.DataFrame()

        dfs.append(df)

    return dfs

import re
def average_range(s):
    """
    searces for a string of the form "num1-num2" and averages the two numbers 
    """

    #https://stackoverflow.com/questions/4703390/how-to-extract-a-floating-number-from-a-string
    # num_regex = r"[-+]?(?:\d*\.\d+|\d+)"
    num_regex = "(\S+)"
    full_regex = r"{}[–-]{}".format(num_regex, num_regex)
    # re.compile(full_regex)
    m = re.search(full_regex, s)
    
    if m is None:
        return s
    else:
        f1 = float(m.groups()[0])
        f2 = float(m.groups()[1])

        return (f1 + f2)/2
