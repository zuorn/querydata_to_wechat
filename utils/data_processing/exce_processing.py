import pandas as pd
from openpyxl.styles import PatternFill, Border, Side
from openpyxl import load_workbook


def exce_processing(file_path):
    """
    读取excel文件，冻结首行，并将列名填充单元格颜色为绿色，设置自适应列宽，所有数据单元格设置所有框线
    """
    # 读取Excel文件
    df = pd.read_excel(file_path)
    
    # 冻结首行
    df.to_excel(file_path, index=False, header=True, freeze_panes=(1,1))

    # 加载工作簿
    wb = load_workbook(file_path)
    ws = wb.active

    # 将列名填充单元格颜色为绿色
    for col in ws.iter_cols(min_row=1, max_row=1):
        for cell in col:
            cell.fill = PatternFill(start_color='CCFFCC', end_color='CCFFCC', fill_type='lightUp')

    # 设置自适应列宽
    for column_cells in ws.columns:
        length = max(len(str(cell.value)) for cell in column_cells)
        ws.column_dimensions[column_cells[0].column_letter].width = length + 2

    # 设置所有数据单元格的框线
    for row in ws.iter_rows(min_row=2):
        for cell in row:
            cell.border = Border(left=Side(style='thin'), 
                                 right=Side(style='thin'), 
                                 top=Side(style='thin'), 
                                 bottom=Side(style='thin'))

    wb.save(file_path)

# if __name__ == '__main__':
#     exce_processing('output/任务1.xlsx')