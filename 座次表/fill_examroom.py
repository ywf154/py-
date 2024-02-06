import openpyxl
wb = openpyxl.load_workbook('座次表模板制作（2023级）.xlsx')
S_moban = wb['模板']
S_stu = wb['学生库']
# 创建以考场开头的三维数组
Students = []  # 【考场，【（学号1，姓名1，班级1）、（学号2，姓名2，班级2）】】
for row in S_stu.iter_rows(values_only=True):
    exroom = row[0]
    student_info = row[1:]
    existing_exroom = next((item for item in Students if item[0] == exroom), None)
    if existing_exroom is None:
        # 如果该考场记录不存在，则创建一个新的考场记录
        new_exroom = [exroom, [student_info]]
        Students.append(new_exroom)
    else:
        existing_exroom[1].append(student_info)
for row in Students:
    exroom = row[0]
    students = row[1]
    # 复制模板表并重命名为考场号
    copied_sheet = wb.copy_worksheet(S_moban)
    copied_sheet.title = exroom
    copied_sheet['H3'].value = exroom
    # 创建学号对应的单元格对象的一维数组
    tableId = []
    for col_range in ['B5:B36', 'E5:E36', 'H5:H36']:
        for cell in wb[exroom][col_range]:
            tableId.append(cell)
    # 创建姓名对应的单元格对象的一维数组
    tableName = []
    for col_range in ['C5:C36', 'F5:F36', 'I5:I36']:
        for cell in wb[exroom][col_range]:
            tableName.append(cell)
    # 填入班级标题集合
    groupSet = set()
    for index, student in enumerate(students):
        # 遍历row[1]:【（学号1，姓名1，班级1）、（学号2，姓名2，班级2）】填入table中
        tableName[index][0].value = students[index][1]
        tableId[index][0].value = students[index][0]
        # 填入班级
        groupSet.add(students[index][2])
    # 生成班级字符串
    groupStr = '、'.join(str(i) for i in groupSet)
    # 班级填入单元格B3
    copied_sheet['B3'].value = groupStr
wb.save('座次表.xlsx')
wb.close()
