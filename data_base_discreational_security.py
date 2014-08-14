
import wx 
import Image
######################################################################
import ctypes  # An included library with Python install.
import wx.grid
import re
from dbHW1 import fetchData
from dbHW1 import insertData
from dbHW1 import getConnector
class gridTable(wx.grid.PyGridTableBase):
    def __init__(self,rows,cols):
        wx.grid.PyGridTableBase.__init__(self)
        self.rows = rows
        self.cols = cols
        self.odd = wx.grid.GridCellAttr()
        self.data = {}#[[]*self.cols for i in xrange(self.rows)]
        self.rowLabels = ['First Name','Last Name','Age','Salary','SSN','General','Tech', 'Finance', 'Hr']
        self.odd.SetBackgroundColour("sky blue")
        self.odd.SetFont(wx.Font(10,wx.SWISS,wx.NORMAL,wx.NORMAL))
        self.even = wx.grid.GridCellAttr()
        self.even.SetBackgroundColour("sea green")
        self.even.SetFont(wx.Font(10,wx.SWISS,wx.NORMAL,wx.NORMAL))
        return
    def IsEmptyCell(self,row,col):
        return self.data.get((row,col))
    def GetColLabelValue(self,row):
        return self.rowLabels[row]
    def SetCellSize(self,row,col,width,height):
        self.Set
        return
    def GetValue(self,row,col):
        value = self.data.get((row,col))
        if(value is not None):
            return value
        else:
            return ''
    def GetNumberRows(self):
        return self.rows
    def GetNumberCols(self):
        return self.cols
    def SetValue(self,row,col,value):
        self.data[(row,col)] = value
        return
    def DeleteRows(self,row,numRows =1):
        
        if(row <= self.GetNumberRows()):
            print(str(row) + " "+str(self.GetNumberRows()))
            #del self.data[(row,1)]
            return True
        else:
            return False 
    def GetAttr(self,row,col,kind):
        attr = [self.even, self.odd][row%2]
        attr.IncRef()
        return attr
    def AppendRows(self,numRows = 1):
        return (self.GetNumberRows() + numRows) <=100
class createGrid():
    headerList = ['id','userName','first name','last name','age','salar','ssn','gen','tech','finance','hr']
    def __init__(self,container,rows,cols):
        self.grid = wx.grid.Grid(container)
        self.grid.CreateGrid(rows,cols)
        self.grid.SetColSize(0,125)
        self.grid.SetColSize(1,125)
        self.grid.SetColSize(2,125)
        self.grid.SetColSize(3,125)
        self.grid.SetColSize(5,125)
        self.grid.SetColSize(6,125)
        self.grid.SetColSize(7,125)
        self.grid.SetColSize(8,125)
        self.grid.SetColSize(9,125)
        self.grid.SetColSize(10,125)
        for i in range(0,cols):
            self.grid.SetColLabelValue(i,self.headerList[i])
        return
    def getGrid(self):
        return  self.grid
    def addItem(self,rowNumber,itemList):
        for i in range(len(itemList)):
            self.grid.SetCellValue(rowNumber,i,"%s" % (itemList[i]))
        return
        
def Mbox(title, text, style):
    ctypes.windll.user32.MessageBoxA(0, text, title, style)

mainFrame = None
#conn = None
class TabPanel(wx.Panel):
    
        """
       This will be the first notebook tab
       """
        ischecked_finance = False
        ischecked_gen=False
        ischecked_tech=False
        ischecked_hr=False
     #----------------------------------------------------------------------
        def __init__(self, parent,page_number):
            wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
            self.parent=parent
            if(page_number == 1):
                self.tab_page_one()
            elif(page_number == 2):
                self.tab_page_two()
            elif(page_number == 3):
                self.tab_page_three()
            elif(page_number == 4):
                self.tab_page_four()
            else:
                self.tab_page_five()
            return
        def insert_execute(self,event):
            global conn
            first_name = self.text_first_name.GetValue()
            last_name = self.text_last_name.GetValue()
            ssn = self.text_ssn.GetValue()
            salary = self.text_salary.GetValue()
            age = self.text_age.GetValue()
            
            #   result = dlg.ShowModal()
            # dlg.Destroy()
            #if result == wx.ID_OK:
            #   self.mainF.Enable(True)
            #  self.Destroy()
            matchFname = re.search('[a-zA-Z]+', first_name,re.I)
            if(matchFname == None):
                dlg = wx.MessageDialog(self,
               "Enter Valid First Name",
               "Confirm Exit", wx.OK|wx.ICON_QUESTION)
                result = dlg.ShowModal()
                dlg.Destroy()
                return
            matchLname = re.search('[a-zA-Z]+', last_name,re.I)
            if(matchLname == None):
                dlg = wx.MessageDialog(self,
               "Enter Valid Last Name",
               "Confirm Exit", wx.OK|wx.ICON_QUESTION)
                result = dlg.ShowModal()
                dlg.Destroy()
                return
            matchAge = re.search('[0-9]{1,3}',age.strip())
            print(str(matchAge))
            if(matchAge == None):
                dlg = wx.MessageDialog(self,
               "Enter Valid Age",
               "Confirm Exit", wx.OK|wx.ICON_QUESTION)
                result = dlg.ShowModal()
                dlg.Destroy()
                return
            matchSSN = re.search('[0-9]{3}-[0-9]{3}-[0-9]{4}',ssn.strip())
            if(matchSSN == None):
                dlg = wx.MessageDialog(self,
               "Enter Valid SSN",
               "Confirm Exit", wx.OK|wx.ICON_QUESTION)
                result = dlg.ShowModal()
                dlg.Destroy()
                return
            matchSalary = re.search('[0-9]{3,7}',salary.strip())
            if(matchSalary == None):
                dlg = wx.MessageDialog(self,
               "Enter Valid Salary",
               "Confirm Exit", wx.OK|wx.ICON_QUESTION)
                result = dlg.ShowModal()
                dlg.Destroy()
                return
            if(self.ischecked_finance == False and self.ischecked_gen == False and self.ischecked_hr == False and self.ischecked_tech == False):
                dlg = wx.MessageDialog(self,
               "Select AtLeast one Compartments",
               "Confirm Exit", wx.OK|wx.ICON_QUESTION)
                result = dlg.ShowModal()
                dlg.Destroy()
                return
            self.text_first_name.SetValue("")
            self.text_last_name.SetValue("")
            self.text_ssn.SetValue("")
            self.text_salary.SetValue("")
            self.text_age.SetValue("")
            list_data = []
            list_data.append(first_name)
            list_data.append(last_name)
            list_data.append(age)
            list_data.append(salary)
            list_data.append(ssn)
            list_data.append(self.ischecked_gen)
            list_data.append(self.ischecked_tech)
            list_data.append(self.ischecked_finance)
            list_data.append(self.ischecked_hr)
            list_data.append(self.parent.objectToWork.userName)
            print(str(list_data[5]) + " "+ str(list_data[6]) +" "+ str(list_data[7]) +" "+ str(list_data[8]))
            conn = getConnector(machine = 'localhost',username = 'root',passwd = 'ztwitasd4',port =3306,databaseName='twitter_sabbir')
            success = insertData('information',conn,list_data)
            if(success == 1):
                self.showDialog("Successfully inserted Information")
            else:
                self.showDialog("DataBase Error cannot insert Data Try Again")
            return
        def OnSelect(self,e):
            print("here we are executing")
            strings = e.GetString()
            if(strings == 'Insert'):
                self.execute.Enable(True)
            else:
                self.execute.Enable(False)
            if(strings == 'Select'):
                self.button_select.Enable(True)
            else:
                self.button_select.Enable(False)
            return
        def Show_Finance(self,event):
            ob = event.GetEventObject()
            self.ischecked_finance = ob.GetValue()
            return
        def Show_Gen(self,event):
            ob = event.GetEventObject()
            self.ischecked_gen = ob.GetValue()
            return
        def Show_Tech(self,event):
            ob = event.GetEventObject()
            self.ischecked_tech = ob.GetValue()
            return
        def Show_Hr(self,event):
            ob = event.GetEventObject()
            self.ischecked_hr = ob.GetValue()
            return
        def select_execute(self,event):
            fn = self.check_first_name.GetValue()
            ln = self.check_last_name.GetValue()
            ssn = self.check_ssn.GetValue()
            salary = self.check_salary.GetValue()
            age = self.check_age.GetValue()
            if(fn==False and ln==False and ssn==False and salary == False):
                self.showDialog("Select at Least one Field")
                return
            compartment = self.check_compartments.GetValue()
            list_list = []
            dict_list = {0:0,1:0,2:0,3:0,4:0,5:0,6:0,7:0,8:0,9:0,10:0}
            i = 0
            if(fn == True):
                list_list.append('firstName')
                dict_list[2] = 1
            if(ln==True):
                list_list.append('lastName')
                dict_list[3] =  1
            if(age ==True):
                list_list.append('age')
                dict_list[4] =  1
            if(salary==True):
                list_list.append('salary')
                dict_list[5] =  1
            if(ssn ==True):
                list_list.append('ssn')
                dict_list[6] = 1
            if(compartment == True):
                dict_list[7] =  1
                dict_list[8] =  1
                dict_list[9] =  1
                dict_list[10] = 1
                list_list.append('Dept1')
                list_list.append('Dept2')
                list_list.append('Dept3')
                list_list.append('Dept4')
            conn = getConnector(machine = 'localhost',username = 'root',passwd = 'ztwitasd4',port =3306,databaseName='twitter_sabbir')
            if(len(list_list) != 0):
                dataOb =  fetchData(tableName='information', con=conn,auth= 0)
            if(dataOb == None):
                self.showDialog("No data Available to Display")
                return
            #self.list_item.Clear()
            #self.list_item.Append(self.list_items[0])
            auth_list = self.parent.objectToWork.data[0][2:]
            row_number = 0
            self.init_gridI()
            for data in dataOb.data:
                #zipper = zip(list_list,data)
                #tempStr = ""
                temp_list_op = data[7:]
                if(self.matchAccess(auth_list, temp_list_op) ==False):
                    continue
                col_number = 0
                for elem in range(2,len(data)):
                    if(dict_list[elem] == 1):
                        self.tableI.SetValue(row_number,col_number,data[elem])
                    else:
                        self.tableI.SetValue(row_number,col_number,'None')
                    col_number += 1
                row_number += 1
                #self.list_item.Append(tempStr)
                # self.list_item.Append(temp_list)
                self.gridI.ForceRefresh()
            return
        def init_gridI(self):
            for i in range(0,self.gridI.GetNumberRows()):
                for j in range(0,self.gridI.GetNumberCols()):
                    self.tableI.SetValue(i,j,"")
            return
        def tab_page_one(self):
            gs = wx.GridSizer(1,3,5,15)
            gs_sub = wx.GridSizer(1,2,5,5)
            data = ['Insert','Select']
            self.execute = wx.Button(self,wx.ID_ANY,'Execute',size=(100,-1))
            self.execute.Enable(False)
            self.execute.Bind(wx.EVT_BUTTON,self.insert_execute)
            #exec_sizer = wx.BoxSizer(wx.HORIZONTAL)
            #exec_sizer.Add(self.execute,proportion=0,flag= wx.RIGHT_ALIGN|wx.Top|wx.RIGHT,border=5)
            execute_label = wx.StaticText(self,-1,'       ',size = (50,-1))
            sizer_execute = wx.BoxSizer(wx.HORIZONTAL)
            sizer_execute.Add(execute_label,proportion=0,flag=wx.EXPAND|wx.TOP|wx.RIGHT,border=5)
            sizer_execute.Add(self.execute,proportion=0,flag=wx.EXPAND|wx.TOP|wx.RIGHT|wx.ALIGN_RIGHT,border=5)
            gs_sub.AddMany([(execute_label,0,wx.EXPAND),(sizer_execute,0,wx.EXPAND)])
            self.cb = wx.ComboBox(self,choices = data,size=(150,-1),style = wx.CB_READONLY|wx.ALIGN_RIGHT)
            self.cb.Bind(wx.EVT_COMBOBOX,self.OnSelect)
            self.labelCb = wx.StaticText(self,-1,'Option',size=(50,-1))
            sizer_for_option = wx.BoxSizer(wx.HORIZONTAL)
            sizer_for_option.Add(self.labelCb,proportion=0,flag=wx.RIGHT|wx.TOP|wx.LEFT,border=10)
            sizer_for_option.Add(self.cb,proportion=0,flag=wx.RIGHT|wx.TOP,border=10)
            self.check_finance = wx.CheckBox(self,label = 'F')
            self.check_finance.SetValue(False)
            if(self.parent.objectToWork.data[0][4]==1):
                self.check_finance.Enable(True)
            else:
                self.check_finance.Enable(False)
            self.check_tech = wx.CheckBox(self,label='T')
            self.check_tech.SetValue(False)
            if(self.parent.objectToWork.data[0][3]==1):
                self.check_tech.Enable(True)
            else:
                self.check_tech.Enable(False)
            self.check_gen = wx.CheckBox(self,label ='G')
            self.check_gen.SetValue(False)
            if(self.parent.objectToWork.data[0][2] ==1):
                self.check_gen.Enable(True)
            else:
                self.check_gen.Enable(False)
            self.check_hr = wx.CheckBox(self,label='H')
            if(self.parent.objectToWork.data[0][5] ==1):
                self.check_hr.Enable(True)
            else:
                self.check_hr.Enable(False)
            self.check_finance.Bind(wx.EVT_CHECKBOX, self.Show_Finance)
            self.check_gen.Bind(wx.EVT_CHECKBOX, self.Show_Gen)
            self.check_tech.Bind(wx.EVT_CHECKBOX, self.Show_Tech)
            self.check_hr.Bind(wx.EVT_CHECKBOX, self.Show_Hr)
            self.check_hr.SetValue(False)
            sizer_check1 = wx.BoxSizer(wx.HORIZONTAL)
            sizer_check2 =wx.BoxSizer(wx.HORIZONTAL)
            sizer_check_ver = wx.BoxSizer(wx.VERTICAL)
            label_text_check = wx.StaticText(self,-1,'Compartments Choice',size=(75,-1))
            sizer_choice_horizontal = wx.BoxSizer(wx.HORIZONTAL)
            sizer_choice_ver = wx.BoxSizer(wx.VERTICAL)
            sizer_check1.Add(self.check_finance,proportion=0,flag=wx.EXPAND|wx.RIGHT,border=5)
            sizer_check1.Add(self.check_tech,proportion=0,flag=wx.EXPAND)
            sizer_check2.Add(self.check_gen,proportion=0,flag=wx.EXPAND|wx.RIGHT,border=4)
            sizer_check2.Add(self.check_hr,proportion=0,flag=wx.EXPAND)
            sizer_choice_ver.Add(sizer_check1,proportion=0,flag=wx.EXPAND|wx.RIGHT|wx.TOP,border=5)
            sizer_choice_ver.Add(sizer_check2,proportion=0,flag=wx.EXPAND|wx.RIGHT|wx.TOP,border=5)
            sizer_choice_horizontal.Add(label_text_check,proportion=0,flag=wx.EXPAND|wx.TOP|wx.RIGHT,border=5)
            sizer_choice_horizontal.Add(sizer_choice_ver,proportion=0,flag=wx.EXPAND|wx.TOP|wx.RIGHT,border=5)
            sizer_check_ver.Add(sizer_choice_horizontal,proportion=0,flag = wx.TOP,border=5)
            #sizer_check_ver.Add(sizer_check2,proportion=0,flag=wx.TOP,border = 5) 
            first_name_label = wx.StaticText(self,-1,'First Name',size=(75,-1))
            last_name_label = wx.StaticText(self,-1,'Last Name',size=(75,-1))
            age = wx.StaticText(self,-1,'Age',size=(75,-1))
            ssn = wx.StaticText(self,-1,'SSN',size=(75,-1))
            salary = wx.StaticText(self,-1,'Salary',size =(75,-1))
            self.text_first_name = wx.TextCtrl(self,wx.ID_ANY,"",size=(200,-1))
            self.text_last_name = wx.TextCtrl(self,-1,"",size=(200,-1))
            self.text_age = wx.TextCtrl(self,-1,"",size=(200,-1))
            self.text_ssn = wx.TextCtrl(self,-1,"",size=(200,-1))
            self.text_salary = wx.TextCtrl(self,-1,"",size = (200,-1))
            sizer_label_text1 = wx.BoxSizer(wx.HORIZONTAL)
            sizer_label_text1.Add(first_name_label,proportion=0,flag=wx.EXPAND|wx.RIGHT,border=5)
            sizer_label_text1.Add(self.text_first_name,proportion=0,flag=wx.EXPAND|wx.RIGHT,border=5)
            sizer_label_text2 = wx.BoxSizer(wx.HORIZONTAL)
            sizer_label_text2.Add(last_name_label,proportion=0,flag = wx.EXPAND|wx.RIGHT,border=5)
            sizer_label_text2.Add(self.text_last_name,proportion=0,flag = wx.EXPAND|wx.RIGHT,border=5)
            sizer_label_text3 = wx.BoxSizer(wx.HORIZONTAL)
            sizer_label_text3.Add(age,proportion=0,flag = wx.EXPAND|wx.RIGHT,border=5)
            sizer_label_text3.Add(self.text_age,proportion=0,flag = wx.EXPAND|wx.RIGHT,border=5)
            sizer_label_text4 = wx.BoxSizer(wx.HORIZONTAL)
            sizer_label_text4.Add(ssn,proportion=0,flag = wx.EXPAND|wx.RIGHT,border=5)
            sizer_label_text4.Add(self.text_ssn,proportion=0,flag = wx.EXPAND|wx.RIGHT,border=5)
            sizer_label_text5 = wx.BoxSizer(wx.HORIZONTAL)
            sizer_label_text5.Add(salary,proportion=0,flag = wx.EXPAND|wx.RIGHT,border=5)
            sizer_label_text5.Add(self.text_salary,proportion=0,flag = wx.EXPAND|wx.RIGHT,border=5)
            sizer_check_ver.Add(sizer_label_text1,proportion=0,flag= wx.TOP,border=5)
            sizer_check_ver.Add(sizer_label_text2,proportion=0,flag= wx.TOP,border=5)
            sizer_check_ver.Add(sizer_label_text3,proportion=0,flag= wx.TOP,border=5)
            sizer_check_ver.Add(sizer_label_text4,proportion=0,flag= wx.TOP,border=5)
            sizer_check_ver.Add(sizer_label_text5,proportion=0,flag= wx.TOP,border=5)
            sizer_check_ver.Add(gs_sub,proportion=0,flag=wx.TOP,border=5)
            stat_box = wx.StaticBox(self,label='For Select Operation',size=(300,200))
            self.button_select = wx.Button(self,wx.ID_ANY,'Execute',size=(75,-1))
            self.button_select.Bind(wx.EVT_BUTTON,self.select_execute)
            self.button_select.Enable(False)
            self.check_first_name = wx.CheckBox(self,label='First Name')
            self.check_last_name = wx.CheckBox(self,label='Last Name')
            self.check_age = wx.CheckBox(self,label='Age')
            self.check_salary= wx.CheckBox(self,label='Salary')
            self.check_ssn = wx.CheckBox(self,label='SSN')
            self.check_compartments = wx.CheckBox(self,label='Compartments')
            sizer_select_super = wx.BoxSizer(wx.VERTICAL)
            sizer_select = wx.StaticBoxSizer(stat_box, wx.VERTICAL)
            sizer_select_super.Add(sizer_select,proportion=0,flag=wx.EXPAND|wx.TOP|wx.RIGHT|wx.LEFT,border =5)
            sizer_select.Add(self.check_first_name,proportion=0,flag=wx.EXPAND|wx.TOP|wx.RIGHT|wx.LEFT,border =5)
            sizer_select.Add(self.check_last_name,proportion=0,flag=wx.EXPAND|wx.TOP|wx.RIGHT|wx.LEFT,border =5)
            sizer_select.Add(self.check_age,proportion=0,flag=wx.EXPAND|wx.TOP|wx.RIGHT|wx.LEFT,border =5)
            sizer_select.Add(self.check_salary,proportion=0,flag=wx.EXPAND|wx.TOP|wx.RIGHT|wx.LEFT,border =5)
            sizer_select.Add(self.check_ssn,proportion=0,flag=wx.EXPAND|wx.TOP|wx.RIGHT|wx.LEFT,border =5)
            sizer_select.Add(self.check_compartments,proportion=0,flag=wx.EXPAND|wx.TOP|wx.RIGHT|wx.LEFT,border =5)
            sizer_select.Add(self.button_select,proportion=0,flag=wx.TOP|wx.RIGHT|wx.ALIGN_RIGHT,border=5)
            gs.AddMany([(sizer_for_option,0,wx.EXPAND),(sizer_check_ver,0,wx.EXPAND),(sizer_select_super,0,wx.EXPAND)])
            self.list_items = ['first_name        last_name        age        salary        ssn    General    Tech    Finance    Hr']
            #self.list_item = wx.ListBox(self,wx.ID_ANY,size=(200,400),choices = self.list_items,style = wx.LB_SINGLE)
            stat_box2 = wx.StaticBox(self,wx.ID_ANY,label='Display Selected Data',size=(600,225))
            sizer_display = wx.StaticBoxSizer(stat_box2, wx.VERTICAL)
            self.gridI = wx.grid.Grid(self)
            self.tableI = gridTable(100,8)
            self.gridI.SetTable(self.tableI,True)
            #self.table.SetValue(1,1,'sabbir')
            #self.table.SetValue(2,2,'Cold Play')
            self.gridI.SetColSize(0,150)
            self.gridI.SetColSize(1,150)
            self.gridI.SetColSize(2,150)
            self.gridI.SetColSize(3,150)
            self.gridI.SetColSize(4,150)
            #self.grid.DeleteRows( 2,1)
            #self.grid.ForceRefresh()
            sizer_display.Add(self.gridI,proportion=0,flag= wx.EXPAND|wx.TOP|wx.BOTTOM|wx.LEFT|wx.RIGHT,border=0)
            sizer_for_panels = wx.BoxSizer(wx.VERTICAL)
            sizer_for_panels.Add(gs,proportion = 0, flag = wx.EXPAND|wx.TOP|wx.BOTTOM|wx.LEFT|wx.RIGHT,border = 5)
            sizer_for_panels.Add(sizer_display,proportion=0,flag=wx.EXPAND|wx.TOP|wx.BOTTOM|wx.LEFT|wx.RIGHT,border=5)
            self.SetSizer(sizer_for_panels)
            return
        def matchAccess(self,l1,l2):
            notzero = 0
            for check in l1:
                if(check == 1):
                    notzero += 1
            if(notzero == 0):
                self.showDialog("You can not access any of the information you are blogged")
                return False
            if(l2[0] == 1):
                return True
            for elem in range(0,len(l1)-1):
                if(l1[elem] == 1):
                    if(l1[elem] == l2[elem]):
                        return True
            return False
        def select_event_handler(self,event):
            self.data_list = self.parent.objectToWork.data[0][2:]
            print(self.data_list)
            con = getConnector(username = 'root', passwd='ztwitasd4', machine='localhost',databaseName= 'twitter_sabbir',port= 3306)
            operator = con.cursor()
            stringTo = 'select * from information'
            operator.execute(stringTo)
            self.dict_feature = {2:0,3:0,4:0,5:0,6:0}
            if(self.check_first_name_del.GetValue() == True):
                self.dict_feature[2] = 1
            if(self.check_last_name_del.GetValue() == True):
                self.dict_feature[3] = 1
            if(self.check_age_del.GetValue() == True):
                self.dict_feature[4] = 1
            if(self.check_salary_del.GetValue() == True):
                self.dict_feature[5] = 1
            if(self.check_ssn_del.GetValue() == True):
                self.dict_feature[6] = 1
            data = operator.fetchall()
            print(data)
            self.parentList = []
            if(len(data) ==0):
                self.showDialog("There is no data to display")
                return None
            for row in data:
                tempList= []
                for col in row:
                    tempList.append(col)
                self.parentList.append(tempList)
            self.addToGrid(self.grid_ob)
            operator.close()
            con.close()      
            return
        def addToGrid(self,grids):
            row_number = 0
            for elem in self.parentList:
                tempList = elem[7:]
                print(tempList)
                if(self.matchAccess(self.data_list,tempList) == False):
                    continue
                for col in range(0,len(elem)):
                    if(self.dict_feature.get(col,None) != None):
                        if(self.dict_feature[col] == 0):
                                elem[col] = 'None'
                grids.addItem(row_number,elem)
                row_number += 1
            return
        def tab_page_two(self):
            fgs = wx.FlexGridSizer(1,3,5,15)
            stat_box1 = wx.StaticBox(self,wx.ID_ANY,'Select Options',size=(300,200))
            stat_box2 = wx.StaticBox(self,wx.ID_ANY,'Delete Data Source',size=(300,200))
           # sizer = wx.BoxSizer(wx.VERTICAL)
           # sizerh = wx.BoxSizer(wx.HORIZONTAL)
            label2 = wx.StaticText(self,-1,'Select Data to Populate Grid',size=(180,-1),style = wx.ALIGN_RIGHT)
            self.button_select_populate = wx.Button(self,wx.ID_ANY,'Execute',size=(100,-1))
            self.button_select_populate.Bind(wx.EVT_BUTTON,self.select_event_handler)
            self.button_select_and_del = wx.Button(self,wx.ID_ANY,'Delete',size=(100,-1))
            self.check_first_name_del = wx.CheckBox(self,wx.ID_ANY,label = 'First Name')
            self.check_last_name_del = wx.CheckBox(self,wx.ID_ANY,label = 'Last Name')
            self.check_age_del = wx.CheckBox(self,wx.ID_ANY,label = 'Age')
            self.check_salary_del = wx.CheckBox(self,wx.ID_ANY,label = 'Salary')
            self.check_ssn_del = wx.CheckBox(self,wx.ID_ANY,label = 'SSN')
            sizer_select = wx.StaticBoxSizer(stat_box1,wx.VERTICAL)
            sizer_select_del = wx.StaticBoxSizer(stat_box2,wx.VERTICAL)
            sizer_select.Add(label2,proportion=0,flag=wx.TOP|wx.BOTTOM|wx.RIGHT,border=5)
            sizer_select.Add(self.check_first_name_del,proportion=0,flag=wx.TOP|wx.BOTTOM|wx.RIGHT,border=5)
            sizer_select.Add(self.check_last_name_del,proportion=0,flag=wx.TOP|wx.BOTTOM|wx.RIGHT,border=5)
            sizer_select.Add(self.check_age_del,proportion=0,flag=wx.TOP|wx.BOTTOM|wx.RIGHT,border=5)
            sizer_select.Add(self.check_salary_del,proportion=0,flag=wx.TOP|wx.BOTTOM|wx.RIGHT,border=5)
            sizer_select.Add(self.check_ssn_del,proportion=0,flag=wx.TOP|wx.BOTTOM|wx.RIGHT,border=5)
            sizer_select.Add(self.button_select_populate,proportion=0,flag=wx.TOP|wx.BOTTOM|wx.RIGHT|wx.ALIGN_RIGHT,border=5)
            label1 = wx.StaticText(self,-1,'Select a Field To Delete From Grid',size=(180,-1),style = wx.ALIGN_RIGHT)
            self.grid_ob = createGrid(self,50,11)
            self.grid_del = self.grid_ob.getGrid()
            
            ver_box = wx.BoxSizer(wx.HORIZONTAL)
            sizer_select_del.Add(label1,proportion = 0, flag = wx.BOTTOM|wx.TOP|wx.LEFT|wx.RIGHT,border=5)
            sizer_select_del.Add(self.grid_del,proportion=1,flag=wx.BOTTOM|wx.TOP|wx.LEFT|wx.RIGHT,border=5)
            sizer_select_del.Add(self.button_select_and_del,proportion=0,flag=wx.BOTTOM|wx.TOP|wx.LEFT|wx.RIGHT|wx.ALIGN_RIGHT,border=5)
            self.button_select_and_del.Bind(wx.EVT_BUTTON,self.del_event_handler)
            fgs.AddMany([(sizer_select,0,wx.EXPAND),(sizer_select_del,0,wx.EXPAND)])
            fgs.AddGrowableCol(1,2)
            ver_box.Add(fgs,proportion=1,flag = wx.EXPAND|wx.BOTTOM|wx.LEFT|wx.RIGHT|wx.TOP,border = 15)
            #txtOne = wx.TextCtrl(self, wx.ID_ANY, "",size = (180,-1))  
           # button1 = wx.Button(self,wx.ID_ANY,'Add')
           # button2 = wx.Button(self,wx.ID_ANY,'Add')
            #sizerh.Add(label1,proportion=1,flag = wx.RIGHT,border=5)
            #sizerh.Add(txtOne,proportion=1,flag = wx.LEFT|wx.ALIGN_CENTER, border = 5)
            #sizerh.Add(button1,proportion=1,flag = wx.RIGHT|wx.LEFT|wx.ALIGN_RIGHT, border = 5)
           # txtTwo = wx.TextCtrl(self, wx.ID_ANY, "",size=(180,-1))
           # sizer = wx.BoxSizer(wx.VERTICAL)
           # sizer.Add(sizerh, 0, wx.ALL, 5)
           # sizer.Add(txtTwo, 0, wx.ALL, 5)    
            self.SetSizer(ver_box)
            return
        def del_event_handler(self,event):
            row_number = self.grid_del.GetSelectedRows()
            print(row_number)
            item_to_del = self.parentList[row_number[0]]
            conn = getConnector(machine='localhost', passwd='ztwitasd4', username='root', databaseName='twitter_sabbir', port=3306)
            operator = conn.cursor()
            print(str(item_to_del[0]))
            string_To_execute = 'delete from information where id = '+ str(item_to_del[0]) 
            try:
                operator.execute(string_To_execute)
                conn.commit()
                success = 1
                print('execution done')
            except Exception:
                print(Exception.message)
                success = 0
                conn.rollback()
            if(success == 1):
                self.showDialog("Data Successfully Deleted")
            else:
                self.showDialog("May be you are not permitted to Delete this information")
                return
            del self.parentList[row_number[0]]
            self.grid_del.DeleteRows(row_number[0],1)
            self.grid_del.AppendRows(numRows = 1)
            
            #self.addToGrid()
            operator.close()
            conn.close()
            return
             
            
        def tab_page_three(self):
            gs = wx.GridSizer(1,3,5,5)
            stat_box1 = wx.StaticBox(self,wx.ID_ANY,'Select Options',size=(300,200))
            stat_box2 = wx.StaticBox(self,wx.ID_ANY,'Where Options',size = (300,200))
            self.check_first_name_per = wx.CheckBox(self,wx.ID_ANY,label = 'First Name')
            self.check_last_name_per = wx.CheckBox(self,wx.ID_ANY,label = 'Last Name')
            self.check_age_per = wx.CheckBox(self,wx.ID_ANY,label = 'Age')
            self.check_salary_per = wx.CheckBox(self,wx.ID_ANY,label = 'Salary')
            self.check_ssn_per = wx.CheckBox(self,wx.ID_ANY,label = 'SSN')
            sizer_select = wx.StaticBoxSizer(stat_box1,wx.VERTICAL)
            sizer_select.Add(self.check_first_name_per,proportion=0,flag=wx.TOP|wx.BOTTOM|wx.RIGHT,border=5)
            sizer_select.Add(self.check_last_name_per,proportion=0,flag=wx.TOP|wx.BOTTOM|wx.RIGHT,border=5)
            sizer_select.Add(self.check_age_per,proportion=0,flag=wx.TOP|wx.BOTTOM|wx.RIGHT,border=5)
            sizer_select.Add(self.check_salary_per,proportion=0,flag=wx.TOP|wx.BOTTOM|wx.RIGHT,border=5)
            sizer_select.Add(self.check_ssn_per,proportion=0,flag=wx.TOP|wx.BOTTOM|wx.RIGHT,border=5)
            self.text_first_name_per = wx.TextCtrl(self,wx.ID_ANY,"",size=(200,-1))
            self.text_last_name_per = wx.TextCtrl(self,-1,"",size=(200,-1))
            self.text_age_per = wx.TextCtrl(self,-1,"",size=(200,-1))
            self.text_ssn_per = wx.TextCtrl(self,-1,"",size=(200,-1))
            self.text_salary_per = wx.TextCtrl(self,-1,"",size = (200,-1))
            first_name_label = wx.StaticText(self,-1,'First Name',size=(75,-1))
            last_name_label = wx.StaticText(self,-1,'Last Name',size=(75,-1))
            age = wx.StaticText(self,-1,'Age',size=(75,-1))
            ssn = wx.StaticText(self,-1,'SSN',size=(75,-1))
            salary = wx.StaticText(self,-1,'Salary',size =(75,-1))
            self.button_select_per = wx.Button(self,wx.ID_ANY,'Execute',size=(75,-1))
            sizer_label_text1_per = wx.BoxSizer(wx.HORIZONTAL)
            sizer_label_text1_per.Add(first_name_label,proportion=0,flag=wx.RIGHT|wx.TOP|wx.BOTTOM|wx.LEFT,border=5)
            sizer_label_text1_per.Add(self.text_first_name_per,proportion=0,flag=wx.RIGHT|wx.TOP|wx.BOTTOM|wx.LEFT,border=5)
            sizer_label_text2_per = wx.BoxSizer(wx.HORIZONTAL)
            sizer_label_text2_per.Add(last_name_label,proportion=0,flag = wx.RIGHT|wx.TOP|wx.BOTTOM|wx.LEFT,border=5)
            sizer_label_text2_per.Add(self.text_last_name_per,proportion=0,flag = wx.RIGHT|wx.TOP|wx.BOTTOM|wx.LEFT,border=5)
            sizer_label_text3_per = wx.BoxSizer(wx.HORIZONTAL)
            sizer_label_text3_per.Add(age,proportion=0,flag = wx.RIGHT|wx.TOP|wx.BOTTOM|wx.LEFT,border=5)
            sizer_label_text3_per.Add(self.text_age_per,proportion=0,flag = wx.RIGHT|wx.TOP|wx.BOTTOM|wx.LEFT,border=5)
            sizer_label_text4_per = wx.BoxSizer(wx.HORIZONTAL)
            sizer_label_text4_per.Add(ssn,proportion=0,flag = wx.RIGHT|wx.TOP|wx.BOTTOM|wx.LEFT,border=5)
            sizer_label_text4_per.Add(self.text_ssn_per,proportion=0,flag = wx.EXPAND|wx.RIGHT|wx.TOP|wx.BOTTOM|wx.LEFT,border=5)
            sizer_label_text5_per = wx.BoxSizer(wx.HORIZONTAL)
            sizer_label_text5_per.Add(salary,proportion=0,flag = wx.RIGHT|wx.TOP|wx.BOTTOM|wx.LEFT,border=5)
            sizer_label_text5_per.Add(self.text_salary_per,proportion=0,flag = wx.RIGHT|wx.TOP|wx.BOTTOM|wx.LEFT,border=5)
            sizer_ver = wx.StaticBoxSizer(stat_box2,wx.VERTICAL)
            sizer_ver.Add(sizer_label_text1_per)
            sizer_ver.Add(sizer_label_text2_per)
            sizer_ver.Add(sizer_label_text3_per)
            sizer_ver.Add(sizer_label_text4_per)
            sizer_ver.Add(sizer_label_text5_per)
            box_sizer = wx.BoxSizer(wx.VERTICAL)
            stat_box3 = wx.StaticBox(self,wx.ID_ANY,'Select Compartments',size = (250,200))
            sizer_ver_for_compartments = wx.StaticBoxSizer(stat_box3,wx.VERTICAL)
            self.check_technology_per = wx.CheckBox(self,wx.ID_ANY,label = 'Technology')
            self.check_humanresource_per = wx.CheckBox(self,wx.ID_ANY,label = 'Human Resource')
            self.check_general_per = wx.CheckBox(self,wx.ID_ANY,label = 'General')
            self.check_finance_per = wx.CheckBox(self,wx.ID_ANY,label = 'Finance')
            #sizer_ver_for_compartments = wx.StaticBoxSizer(stat_box1,wx.VERTICAL)
            sizer_ver_for_compartments.Add(self.check_technology_per,proportion=0,flag = wx.RIGHT|wx.TOP|wx.BOTTOM|wx.LEFT, border=5)
            sizer_ver_for_compartments.Add(self.check_humanresource_per,proportion=0,flag=wx.RIGHT|wx.TOP|wx.BOTTOM|wx.LEFT,border = 5)
            sizer_ver_for_compartments.Add(self.check_general_per,proportion=0,flag=wx.RIGHT|wx.TOP|wx.BOTTOM|wx.LEFT,border=5)
            sizer_ver_for_compartments.Add(self.check_finance_per,proportion=0,flag=wx.RIGHT|wx.TOP|wx.BOTTOM|wx.LEFT,border=5)
            stat_box_execute = wx.BoxSizer(wx.HORIZONTAL)
            stat_box_execute.Add(self.button_select_per,wx.ID_ANY,flag =wx.EXPAND|wx.TOP|wx.ALIGN_RIGHT|wx.BOTTOM|wx.RIGHT,border=5)
            gs.AddMany([(sizer_select,0,wx.EXPAND),(sizer_ver,0,wx.EXPAND),(sizer_ver_for_compartments,0,wx.EXPAND)])
            gs1 = wx.GridSizer(1,3,5,5)
            box_sizer.Add(gs,proportion=0,flag = wx.EXPAND|wx.TOP|wx.BOTTOM|wx.LEFT|wx.RIGHT,border=5)
            stat_box_list = wx.StaticBox(self,wx.ID_ANY, label='List of Data',size = (400,200))
            stat_box_list_sizer = wx.StaticBoxSizer(stat_box_list,wx.VERTICAL)
            #box_sizer.Add(stat_box_execute,proportion=0,flag=wx.EXPAND|wx.TOP|wx.BOTTOM|wx.RIGHT,border=5)
            gs1.AddMany([(wx.StaticText(self),wx.EXPAND),(wx.StaticText(self),wx.EXPAND),(stat_box_execute,0,wx.EXPAND)])
            box_sizer.Add(gs1,proportion=0,flag=wx.EXPAND|wx.LEFT|wx.TOP|wx.BOTTOM|wx.RIGHT,border=5)
            self.grid = wx.grid.Grid(self)
            self.table = gridTable(100,5)
            self.grid.SetTable(self.table,True)
            self.table.SetValue(1,1,'sabbir')
            self.table.SetValue(2,2,'Cold Play')
            self.grid.SetColSize(0,150)
            self.grid.SetColSize(1,150)
            self.grid.SetColSize(2,150)
            self.grid.SetColSize(3,150)
            self.grid.SetColSize(4,150)
            self.grid.DeleteRows( 2,1)
            self.grid.ForceRefresh()
            stat_box_list_sizer.Add(self.grid,proportion=1,flag=wx.EXPAND|wx.TOP|wx.BOTTOM|wx.LEFT|wx.RIGHT,border =1)
            box_sizer.Add(stat_box_list_sizer,proportion=1,flag=wx.EXPAND|wx.TOP|wx.BOTTOM|wx.LEFT|wx.RIGHT,border = 1)
            self.SetSizer(box_sizer)
            
            return
        def getSetVal(self,setVal):
            permit_list2 = self.list_of_users.GetChecked()
            if(len(permit_list2) == 0):
                self.showDialog("Select At least One data recored")
                return
            #print(permit_list)
            print(permit_list2)
            tech = self.check_technology_per_usr.GetValue()
            hr = self.check_humanresource_per_usr.GetValue()
            gen = self.check_general_per_usr.GetValue()
            finance = self.check_finance_per_usr.GetValue()
            if(tech==False and hr==False and gen==False and finance==False):
                self.showDialog("Select At least One compartments")
                return
            con = getConnector(username='root', passwd='ztwitasd4', machine='localhost', databaseName='twitter_sabbir', port=3306)
            operator = con.cursor()
            for item in permit_list2:
                string_to = self.list_of_data_per[item]
                get_id = string_to.split('\t')
                tempS1 = re.search('\'[0-9]*\'', get_id[0])
                tempL = tempS1.group().split('\'')
                print(get_id)
                if(tech== True):
                    stringToexec = 'update information set Dept2 = ' + str(setVal)+' where id = ' +tempL[1]
                    print(stringToexec)
                    result = self.call_for_execution(stringToexec,operator,con)
                    if(result == 0): 
                        operator.close()
                        con.close()
                        self.showDialog("Couldn't commit there is a problem press Ok")
                        return
                if(gen == True):
                    stringToexec = 'update information set Dept1 = ' + str(setVal)+' where id = ' +tempL[1]
                    result = self.call_for_execution(stringToexec,operator,con)
                    if(result == 0): 
                        self.showDialog("Couldn't commit there is a problem press Ok")
                        operator.close()
                        con.close()
                        return
                if(hr == True):
                    stringToexec = 'update information set Dept4 = ' + str(setVal)+' where id = ' +tempL[1]
                    result = self.call_for_execution(stringToexec,operator,con)
                    if(result == 0): 
                        self.showDialog("Couldn't commit there is a problem press Ok")
                        operator.close()
                        con.close()
                        return
                if(finance ==True):
                    stringToexec = 'update information set Dept3 = ' + str(setVal)+' where id = ' +tempL[1]
                    result = self.call_for_execution(stringToexec,operator,con)
                    if(result == 0): 
                        self.showDialog("Couldn't commit there is a problem press Ok")
                        operator.close()
                        con.close()
                        return
                    
            self.showDialog("Successfully Updated")
            operator.close()
            con.close()
            self.get_list_of_data()
            self.list_of_users.Clear()
            self.check_technology_per_usr.SetValue(False)
            self.check_general_per_usr.SetValue(False)
            self.check_finance_per_usr.SetValue(False)
            self.check_humanresource_per_usr.SetValue(False)
            for elem in self.list_of_data_per:
                self.list_of_users.Append(elem)
            return
        def permit_grant(self,event):
            #permit_list = self.list_of_users.GetSelections()
            self.getSetVal(True)
            return
        def showDialog(self,statement):
            dlg = wx.MessageDialog(self,
               statement,
               "Confirm", wx.OK|wx.ICON_QUESTION)
            result = dlg.ShowModal()
            dlg.Destroy()
            if result == wx.ID_OK:
                pass
                # conn.close()
                
            return
        def call_for_execution(self,stringToexec,operator,con):
            success = 0
            try:
                operator.execute(stringToexec)
                con.commit()
                success = 1
            except Exception:
                print(Exception.message)
                con.rollback()
                success = 0
            return success
        def permit_revoke(self,event):
            self.getSetVal(False)
            return
        def get_list_of_data(self):
            con = getConnector(machine = 'localhost', username = 'root', passwd = 'ztwitasd4', databaseName='twitter_sabbir', port=3306)
            operator = con.cursor()
            stringToexecute = 'select * from information'
            operator.execute(stringToexecute)
            data = operator.fetchall()
            print(data)
            self.list_of_data_per = []
            dict_feature_name = {0:'id',1:'username',2:'first name',3:'last name',4:'age',5:'salary',6:'ssn',7:'gen',8:'tech',9:'finance',10:'hr'}
            if(len(data) ==0):
                return None
            for row in data:
                tempList= ''
                i1 = 0
                for col in row:
                    tempList += str((dict_feature_name[i1],str(col)))+'\t'
                    i1 += 1
                self.list_of_data_per.append(tempList)
            operator.close()
            con.close()
            return
        def tab_page_four(self):
            # last_name_label = wx.StaticText(self,-1,'Select an User from List and Then Select Access Level',size=(200,-1))
            stat_box_super = wx.StaticBox(self,wx.ID_ANY,'Select a Record from List and Then Select Access Level',size = (250,200))
            stat_box_sizer_super = wx.StaticBoxSizer(stat_box_super,wx.HORIZONTAL)
            sizer = wx.BoxSizer(wx.VERTICAL)
            #sizer.Add(last_name_label,proportion=0,flag = wx.EXPAND|wx.TOP|wx.LEFT|wx.BOTTOM,border =10)
            stat_box3 = wx.StaticBox(self,wx.ID_ANY,'Select Compartments',size = (250,200))
            self.button_select_and_per = wx.Button(self,wx.ID_ANY,'Grant',size=(100,-1))
            self.button_select_and_rev = wx.Button(self,wx.ID_ANY,'Revoke',size=(100,-1))
            self.button_select_and_per.Bind(wx.EVT_BUTTON,self.permit_grant)
            self.button_select_and_rev.Bind(wx.EVT_BUTTON,self.permit_revoke)
            hbsizer = wx.BoxSizer(wx.HORIZONTAL)
            hbsizer.Add(self.button_select_and_per,proportion=0,flag=wx.LEFT|wx.RIGHT|wx.TOP|wx.BOTTOM,border=5)
            hbsizer.Add(self.button_select_and_rev,proportion=0,flag=wx.LEFT|wx.RIGHT|wx.TOP|wx.BOTTOM,border=5)
            sizer_ver_for_compartments = wx.StaticBoxSizer(stat_box3,wx.VERTICAL)
            self.check_technology_per_usr = wx.CheckBox(self,wx.ID_ANY,label = 'Technology')
            self.check_humanresource_per_usr = wx.CheckBox(self,wx.ID_ANY,label = 'Human Resource')
            self.check_general_per_usr = wx.CheckBox(self,wx.ID_ANY,label = 'General')
            self.check_finance_per_usr = wx.CheckBox(self,wx.ID_ANY,label = 'Finance')
            #sizer_ver_for_compartments = wx.StaticBoxSizer(stat_box1,wx.VERTICAL)
            sizer_ver_for_compartments.Add(self.check_technology_per_usr,proportion=0,flag = wx.RIGHT|wx.TOP|wx.BOTTOM|wx.LEFT, border=5)
            sizer_ver_for_compartments.Add(self.check_humanresource_per_usr,proportion=0,flag=wx.RIGHT|wx.TOP|wx.BOTTOM|wx.LEFT,border = 5)
            sizer_ver_for_compartments.Add(self.check_general_per_usr,proportion=0,flag=wx.RIGHT|wx.TOP|wx.BOTTOM|wx.LEFT,border=5)
            sizer_ver_for_compartments.Add(self.check_finance_per_usr,proportion=0,flag=wx.RIGHT|wx.TOP|wx.BOTTOM|wx.LEFT,border=5)
            sizer_ver_for_compartments.Add(hbsizer,flag = wx.RIGHT|wx.TOP|wx.BOTTOM|wx.wx.LEFT,border=5)
            self.get_list_of_data()
            self.list_of_users = wx.CheckListBox(self,wx.ID_ANY,(-1,-1),(400,180),self.list_of_data_per,wx.LB_MULTIPLE|wx.LB_HSCROLL|wx.LB_NEEDED_SB)
            list_box_sizer = wx.BoxSizer(wx.HORIZONTAL)
            list_box_sizer.Add(self.list_of_users,proportion=0,flag=wx.TOP|wx.LEFT,border=5)
            gs = wx.FlexGridSizer(1,3,5,25)
            gs.AddMany([(list_box_sizer,0,wx.EXPAND),(sizer_ver_for_compartments,0,wx.EXPAND),(wx.StaticText(self),wx.EXPAND)])
            gs.AddGrowableCol(0,2)
            sizer.Add(gs,proportion=0,flag = wx.TOP|wx.LEFT|wx.BOTTOM,border=10)
            hor_box_sizer = wx.BoxSizer(wx.HORIZONTAL)
            stat_box_sizer_super.Add(sizer,proportion=1,flag =wx.EXPAND| wx.TOP|wx.LEFT|wx.BOTTOM|wx.RIGHT,border=15)
            hor_box_sizer.Add(stat_box_sizer_super,proportion=1,flag =wx.EXPAND| wx.TOP|wx.LEFT|wx.BOTTOM|wx.RIGHT,border=15)
            self.SetSizer(hor_box_sizer)
            return
        def get_list_of_data_usr(self):
            con = getConnector(machine = 'localhost', username = 'root', passwd = 'ztwitasd4', databaseName='twitter_sabbir', port=3306)
            operator = con.cursor()
            stringToexecute = 'select * from userInfo'
            operator.execute(stringToexecute)
            data = operator.fetchall()
            print(data)
            self.list_of_data_per_usr = []
            dict_feature_name = {0:'userName',1:'password',2:'Gen',3:'Tech',4:'Finance',5:'Hr',6:'Role'}
            if(len(data) ==0):
                return None
            for row in data:
                tempList= ''
                i1 = 0
                for col in row:
                    if(i1 == 1):
                        tempList =tempList + str((dict_feature_name[i1],str('*****')))+'\t'
                        i1 += 1
                    else:
                        tempList = tempList + str((dict_feature_name[i1],str(col)))+'\t'
                        i1 += 1
                self.list_of_data_per_usr.append(tempList)
            operator.close()
            con.close()
            return
        def getSetVal_usr(self,setVal):
            permit_list2 = self.list_of_users_per.GetChecked()
            if(len(permit_list2) == 0):
                self.showDialog("Select At least One data recored")
                return
            #print(permit_list)
            print(permit_list2)
            tech = self.check_technology_per_usr2.GetValue()
            hr = self.check_humanresource_per_usr2.GetValue()
            gen = self.check_general_per_usr2.GetValue()
            finance = self.check_finance_per_usr2.GetValue()
            role = self.check_role_per.GetValue()
            if(tech==False and hr==False and gen==False and finance==False and role == False):
                self.showDialog("Select At least One compartments")
                return
            con = getConnector(username='root', passwd='ztwitasd4', machine='localhost', databaseName='twitter_sabbir', port=3306)
            operator = con.cursor()
            for item in permit_list2:
                string_to = self.list_of_data_per_usr[item]
                get_id = string_to.split('\t')
                tempS1 =  get_id[0].split(',')
                tempL = tempS1[1].split('\'')
                print(tempL)
                if(tech== True):
                    stringToexec = 'update userInfo set Dept2 = ' + str(setVal)+' where userName = "' +tempL[1]+'"'
                    print(stringToexec)
                    result = self.call_for_execution(stringToexec,operator,con)
                    if(result == 0): 
                        operator.close()
                        con.close()
                        self.showDialog("Couldn't commit there is a problem press Ok")
                        return
                if(gen == True):
                    stringToexec = 'update userInfo set Dept1 = ' + str(setVal)+' where userName = "' +tempL[1]+'"'
                    result = self.call_for_execution(stringToexec,operator,con)
                    if(result == 0): 
                        self.showDialog("Couldn't commit there is a problem press Ok")
                        operator.close()
                        con.close()
                        return
                if(hr == True):
                    stringToexec = 'update userInfo set Dept4 = ' + str(setVal)+' where userName = "' +tempL[1]+'"'
                    result = self.call_for_execution(stringToexec,operator,con)
                    if(result == 0): 
                        self.showDialog("Couldn't commit there is a problem press Ok")
                        operator.close()
                        con.close()
                        return
                if(finance ==True):
                    stringToexec = 'update userInfo set Dept3 = ' + str(setVal)+' where userName = "' +tempL[1]+'"'
                    result = self.call_for_execution(stringToexec,operator,con)
                    if(result == 0): 
                        self.showDialog("Couldn't commit there is a problem press Ok")
                        operator.close()
                        con.close()
                        return
                if(role ==True):
                    stringToexec = 'update userInfo set Role = ' + str(setVal)+' where userName = "' +tempL[1]+'"'
                    result = self.call_for_execution(stringToexec,operator,con)
                    if(result == 0): 
                        self.showDialog("Couldn't commit there is a problem press Ok")
                        operator.close()
                        con.close()
                        return
                    
            self.showDialog("Successfully Updated")
            operator.close()
            con.close()
            self.get_list_of_data_usr()
            self.list_of_users_per.Clear()
            self.check_technology_per_usr2.SetValue(False)
            self.check_general_per_usr2.SetValue(False)
            self.check_finance_per_usr2.SetValue(False)
            self.check_humanresource_per_usr2.SetValue(False)
            for elem in self.list_of_data_per_usr:
                self.list_of_users_per.Append(elem)
            return
        def permit_grant_usr(self,event):
            self.getSetVal_usr(True)
            return
        def permit_revoke_usr(self,event):
            self.getSetVal_usr(False)
            return
        def tab_page_five(self):
            stat_box_super = wx.StaticBox(self,wx.ID_ANY,'Select an User from List and Then Select Access Level',size = (250,200))
            stat_box_sizer_super = wx.StaticBoxSizer(stat_box_super,wx.HORIZONTAL)
            sizer = wx.BoxSizer(wx.VERTICAL)
            #sizer.Add(last_name_label,proportion=0,flag = wx.EXPAND|wx.TOP|wx.LEFT|wx.BOTTOM,border =10)
            stat_box3 = wx.StaticBox(self,wx.ID_ANY,'Select Compartments',size = (250,200))
            self.button_select_and_per_usr = wx.Button(self,wx.ID_ANY,'Grant',size=(100,-1))
            self.button_select_and_rev_usr = wx.Button(self,wx.ID_ANY,'Revoke',size=(100,-1))
            self.button_select_and_per_usr.Bind(wx.EVT_BUTTON,self.permit_grant_usr)
            self.button_select_and_rev_usr.Bind(wx.EVT_BUTTON,self.permit_revoke_usr)
            hbsizer = wx.BoxSizer(wx.HORIZONTAL)
            hbsizer.Add(self.button_select_and_per_usr,proportion=0,flag=wx.LEFT|wx.RIGHT|wx.TOP|wx.BOTTOM,border=5)
            hbsizer.Add(self.button_select_and_rev_usr,proportion=0,flag=wx.LEFT|wx.RIGHT|wx.TOP|wx.BOTTOM,border=5)
            sizer_ver_for_compartments = wx.StaticBoxSizer(stat_box3,wx.VERTICAL)
            self.check_technology_per_usr2 = wx.CheckBox(self,wx.ID_ANY,label = 'Technology')
            self.check_humanresource_per_usr2 = wx.CheckBox(self,wx.ID_ANY,label = 'Human Resource')
            self.check_general_per_usr2 = wx.CheckBox(self,wx.ID_ANY,label = 'General')
            self.check_finance_per_usr2 = wx.CheckBox(self,wx.ID_ANY,label = 'Finance')
            self.check_role_per = wx.CheckBox(self,wx.ID_ANY,label = 'Role')
            #sizer_ver_for_compartments = wx.StaticBoxSizer(stat_box1,wx.VERTICAL)
            sizer_ver_for_compartments.Add(self.check_technology_per_usr2,proportion=0,flag = wx.RIGHT|wx.TOP|wx.BOTTOM|wx.LEFT, border=5)
            sizer_ver_for_compartments.Add(self.check_humanresource_per_usr2,proportion=0,flag=wx.RIGHT|wx.TOP|wx.BOTTOM|wx.LEFT,border = 5)
            sizer_ver_for_compartments.Add(self.check_general_per_usr2,proportion=0,flag=wx.RIGHT|wx.TOP|wx.BOTTOM|wx.LEFT,border=5)
            sizer_ver_for_compartments.Add(self.check_finance_per_usr2,proportion=0,flag=wx.RIGHT|wx.TOP|wx.BOTTOM|wx.LEFT,border=5)
            sizer_ver_for_compartments.Add(self.check_role_per,proportion=0,flag=wx.RIGHT|wx.TOP|wx.BOTTOM|wx.LEFT,border=5)
            sizer_ver_for_compartments.Add(hbsizer,flag = wx.RIGHT|wx.TOP|wx.BOTTOM|wx.wx.LEFT,border=5)
            self.get_list_of_data_usr()
            self.list_of_users_per = wx.CheckListBox(self,wx.ID_ANY,(-1,-1),(400,180),self.list_of_data_per_usr,wx.LB_MULTIPLE|wx.LB_HSCROLL|wx.LB_NEEDED_SB)
            list_box_sizer = wx.BoxSizer(wx.HORIZONTAL)
            list_box_sizer.Add(self.list_of_users_per,proportion=0,flag=wx.TOP|wx.LEFT,border=5)
            gs = wx.FlexGridSizer(1,3,5,25)
            gs.AddMany([(list_box_sizer,0,wx.EXPAND),(sizer_ver_for_compartments,0,wx.EXPAND),(wx.StaticText(self),wx.EXPAND)])
            gs.AddGrowableCol(0,2)
            sizer.Add(gs,proportion=0,flag = wx.TOP|wx.LEFT|wx.BOTTOM,border=10)
            hor_box_sizer = wx.BoxSizer(wx.HORIZONTAL)
            stat_box_sizer_super.Add(sizer,proportion=1,flag =wx.EXPAND| wx.TOP|wx.LEFT|wx.BOTTOM|wx.RIGHT,border=15)
            hor_box_sizer.Add(stat_box_sizer_super,proportion=1,flag =wx.EXPAND| wx.TOP|wx.LEFT|wx.BOTTOM|wx.RIGHT,border=15)
            self.SetSizer(hor_box_sizer)
            return
   ########################################################################


class NotebookDemo(wx.Notebook):
    def __init__(self, parent,objectToWork):
        wx.Notebook.__init__(self, parent, id=wx.ID_ANY, style=wx.BK_DEFAULT
                              #wx.BK_TOP 
                              #wx.BK_BOTTOM
                               #wx.BK_LEFT
                               #wx.BK_RIGHT
                               )
 
        self.objectToWork = objectToWork
        tabOne = TabPanel(self,1)
        tabOne.SetBackgroundColour("Gray")
        self.AddPage(tabOne, "Data Insertion")
 
        # Show how to put an image on one of the notebook tabs,
        # first make the image list:
        #  il = wx.ImageList(16, 16)
        # idx1 = il.Add(Image.Smiles.GetBitmap())
        #self.AssignImageList(il)
  
           # now put an image on the first tab we just created:
        #self.SetPageImage(0, idx1)
   
           # Create and add the second tab
        tabTwo = TabPanel(self,2)
        tabTwo.SetBackgroundColour("Gray")
        self.AddPage(tabTwo, "Data Deletion")
   
           # Create and add the third tab
        tabThree = TabPanel(self,3)
        tabThree.SetBackgroundColour('Gray')
        self.AddPage(tabThree, "Data Filtering")
        if(self.objectToWork.data[0][6]== 1):
            self.tabFour = TabPanel(self,4)
            self.tabFour.SetBackgroundColour('Gray')
            self.AddPage(self.tabFour,'Permission Record')
        if(self.objectToWork.data[0][6] == 1):
            self.tabFive = TabPanel(self,5)
            self.tabFive.SetBackgroundColour('Gray')
            self.AddPage(self.tabFive,'Permission User')
        self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.OnPageChanged)
        self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGING, self.OnPageChanging)
                    
    def OnPageChanged(self, event):
            old = event.GetOldSelection()
            new = event.GetSelection()
            sel = self.GetSelection()
            print 'OnPageChanged,  old:%d, new:%d, sel:%d\n' % (old, new, sel)
            self.tabFour.get_list_of_data()
            self.tabFour.list_of_users.Clear()
            for elem in self.tabFour.list_of_data_per:
                self.tabFour.list_of_users.Append(elem)
            #self.get
            event.Skip()
          
    def OnPageChanging(self, event):
            old = event.GetOldSelection()
            new = event.GetSelection()
            sel = self.GetSelection()
            print 'OnPageChanging, old:%d, new:%d, sel:%d\n' % (old, new, sel)
            event.Skip()
     
     
     ########################################################################
class DemoFrame(wx.Frame):
    def __init__(self,mainF,objectToWork):
        wx.Frame.__init__(self, mainF, wx.ID_ANY,"Main Gui",size=(900,600)
                               )
        panel = wx.Panel(self)
        self.mainF= mainF
        self.objectToWork = objectToWork
        notebook = NotebookDemo(panel,self.objectToWork)
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(notebook, 1, wx.ALL|wx.EXPAND, 5)
        panel.SetSizer(sizer)
        self.Layout()
  
        self.Show()
    def OnClose(self, event):
        print('Exiting Demo Frame')
        dlg = wx.MessageDialog(self,
               "Do you really want to close this application?",
               "Confirm Exit", wx.OK|wx.CANCEL|wx.ICON_QUESTION)
        result = dlg.ShowModal()
        dlg.Destroy()
        if result == wx.ID_OK:
            self.mainF.Enable(True)
           # conn.close()
            self.Destroy()
class mainFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self,None,wx.ID_ANY,'Log in',size = (600,400))
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        panel = wx.Panel(self)
        label1 = wx.StaticText(panel,-1,'User Name',size=(75,-1),style = wx.ALIGN_CENTER)
        self.userName = wx.TextCtrl(panel,-1,'',size= (180,-1),style=wx.TE_LEFT|wx.TE_NOHIDESEL)
        label2  =wx.StaticText(panel,-1,'Password',size=(75,-1),style = wx.ALIGN_CENTER)
        label3  =wx.StaticText(panel,-1,'         ',size=(75,-1),style = wx.ALIGN_CENTER)
        self.password = wx.TextCtrl(panel,-1,'',size = (180,-1),style = wx.TE_PASSWORD|wx.TE_LEFT)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizerh1 = wx.BoxSizer(wx.HORIZONTAL)
        sizerh2 = wx.BoxSizer(wx.HORIZONTAL)
        sizerv =wx.BoxSizer(wx.VERTICAL)
        sizerM = wx.BoxSizer(wx.HORIZONTAL)
        logIn = wx.Button(panel, label='Log In',size = (100,-1),style = wx.ALIGN_RIGHT)
        sizerh1.Add(label1,proportion =1 , flag =  wx.LEFT, border = 25)
        sizerh1.Add(self.userName,proportion=1,flag = wx.RIGHT|wx.EXPAND, border = 50)
        sizerh2.Add(label2,proportion =1,flag = wx.LEFT,border = 25)
        sizerh2.Add(self.password,proportion=1,flag=wx.RIGHT|wx.EXPAND,border = 50)
        sizer.Add(sizerh1,0,flag = wx.ALL|wx.ALIGN_CENTER,border =5)
        sizer.Add(sizerh2,0,flag = wx.ALL|wx.ALIGN_CENTER,border =5)
        sizerv.Add(sizer,0,flag = wx.ALIGN_CENTER|wx.TOP, border = 30)
        sizerM.Add(label3,0,flag =wx.RIGHT|wx.EXPAND,border =5)
        sizerM.Add(logIn,0,flag =wx.LEFT|wx.EXPAND,border = 180)
        sizerv.Add(sizerM,0,flag = wx.TOP|wx.ALIGN_CENTER,border = 5)
        logIn.Bind(wx.EVT_BUTTON,self.loggedIn)
        logIn.Enable(True)
        panel.SetSizer(sizerv)
        self.Layout()
        self.Show()
    def OnClose(self,event):
        self.Destroy()
        return
    def loggedIn(self,event):
        global mainFrame
        #global conn
        conn = getConnector(machine = 'localhost',username = 'root',passwd = 'ztwitasd4',port =3306,databaseName='twitter_sabbir')
        usernames = self.userName.GetValue()
        passwd = self.password.GetValue()
        if(len(usernames)==0 or len(passwd)==0):
            self.userName.SetValue("")
            self.password.SetValue("")
            Mbox('Waring',"Either Password or Username is Missing", wx.FONTFAMILY_DEFAULT)
            return
        print('userName: '+ usernames + 'password: ' + passwd)
        objectToWork = fetchData(tableName='userInfo',con=conn,username=usernames,passwd=passwd,auth=1)
        if(objectToWork != None):
            objectToWork.userName = self.userName.GetValue().strip()
        if(objectToWork == None):
            self.userName.SetValue("")
            self.password.SetValue("")
            Mbox('Waring',"There is no User of that Name", wx.FONTFAMILY_DEFAULT)
            return
        
        frame = DemoFrame(mainFrame,objectToWork)
        self.Enable(False)
        return
if __name__ == "__main__":
    app = wx.PySimpleApp()
    mainFrame = mainFrame()
    #frame = DemoFrame(mainF)
    app.MainLoop()