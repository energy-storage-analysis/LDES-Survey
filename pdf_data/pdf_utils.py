import pandas as pd

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

def get_pdf_size(pdf_path, page):
    """Get pdf width and height"""
    input1 = PdfFileReader(open(pdf_path, 'rb'))
    media_box = input1.getPage(page).mediaBox
    pdf_width = float(media_box[2])-float(media_box[0])
    pdf_height = float(media_box[3])-float(media_box[1])
    return pdf_width, pdf_height

def extract_tabula_template(t, pdf_height):
    """extracts tabula template dict to data suitable for camelot"""
    
    page = str(t['page'])

    table_area = [
        float(t['x1']),
        pdf_height - float(t['y1']),
        float(t['x2']),
        pdf_height- float(t['y2'])
        ]
    # table_area = [str(int(s)) for s in table_area]
    table_area = ['{},{},{},{}'.format(*table_area)]
    return page, table_area

