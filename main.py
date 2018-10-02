#!/usr/bin/env python3
from PyQt5 import QtWidgets,uic
import TransactionManager
import DataCenter
import json
import sys
import os


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

base2,form2=uic.loadUiType(resource_path('PollCreator.ui'))
base3,form3=uic.loadUiType(resource_path('PollManager.ui'))
base4,form4=uic.loadUiType(resource_path('Stats.ui'))

class PollCreator(base2,form2):
    def __init__(self):
        super(base2,self).__init__()
        self.setupUi(self)
        self.setFixedSize(800,600)
        self.addopt.clicked.connect(self.addOptions)
        self.modifyopt.clicked.connect(self.modifyOptions)
        self.deleteopt.clicked.connect(self.deleteOptions)
        self.FinalBtn.clicked.connect(self.finalizePoll)
    def addOptions(self):
        text,ok = QtWidgets.QInputDialog.getText(self,"Option Entry","Enter your option value: ", QtWidgets.QLineEdit.Normal, "")
        if ok:
            self.OptionsArea.addItem(text)
    def modifyOptions(self):
        for item in self.OptionsArea.selectedItems():
            text,ok = text,ok = QtWidgets.QInputDialog.getText(self,"Modify Entry","Enter your new option value: ", QtWidgets.QLineEdit.Normal, "")
            if ok:
                item.setText(text)
    def deleteOptions(self):
        item = self.OptionsArea.takeItem(self.OptionsArea.currentRow())
        item = None
    def finalizePoll(self):
        question = self.InputQuestion.toPlainText()
        if len(question)<=5:
            self.error_dialog = QtWidgets.QErrorMessage()
            self.dlg.status.setText("Length Error: Length of Question can't be less than 5")
            return

        self.to_addr=TransactionManager.getPollAdress().decode().strip('\n')
        self.optionString = [question,] + [str(self.OptionsArea.item(i).text()) for i in range(self.OptionsArea.count())]+[self.to_addr]

        print(self.optionString)
        choice = QtWidgets.QMessageBox.question(QtWidgets.QWidget(),"Confirm Transaction","Do you want to post the poll to block chain ?",QtWidgets.QMessageBox.Yes|QtWidgets.QMessageBox.No)
        if choice==QtWidgets.QMessageBox.Yes:
            try:
                poll_id = TransactionManager.writeDatatoBlockchain('*'.join(self.optionString),self.to_addr,0.3)
                #poll_id = "12345"
                print('*'.join(self.optionString))
                QtWidgets.QMessageBox(QtWidgets.QMessageBox.Information,"Transaction Success","Poll posted to block chain!",QtWidgets.QMessageBox.Ok).exec_()
                QtWidgets.QMessageBox(QtWidgets.QMessageBox.Information,"Poll id Information","Share this id with your audience so that they can vote!"+"\nId: "+poll_id,QtWidgets.QMessageBox.Ok).exec_()
                DataCenter.write(poll_id,"*".join(self.optionString))
                print(DataCenter.readAll())
            except Exception as e:
                print(e)
                self.error_dialog = QtWidgets.QErrorMessage()
                self.error_dialog.setWindowTitle('Network Error')
                self.error_dialog.showMessage("Error in sending Poll! Please Try again")

class PData:
    def __init__(self,row):
        self.pid = row[0]
        self.pques = row[1].split('*')[0]
        self.popt = row[1].split('*')[1:-1]
        self.paddr = row[1].split('*')[-1]
    def __str__(self):
        if len(self.pques)>50:
            self.pques = "{:.50}".format(self.pques)+'...'
        return self.pques+" "*(125-len(self.pques))+"{:.10}".format(self.pid)+"..."


class PollManager(base3,form3):
    def __init__(self):
        super(base3,self).__init__()
        self.setupUi(self)
        self.setFixedSize(800,600)
        self.loadData()
        self.GetResult.clicked.connect(self.showPollStats)
        self.deleteBtn.clicked.connect(self.removeEntry)

    def loadData(self):
        data = DataCenter.readAll()
        self.dataList = []
        for row in data:
            # print(row)
            # pid = row[0]
            # pques = row[1].split('*')[0]
            # pdata = pques+' '*(80-len(pques))+pid
            pdata = PData(row)
            self.dataList.append(pdata)
            self.PollList.addItem(str(pdata))

    def removeEntry(self):
        id = self.dataList[self.PollList.currentRow()].pid
        DataCenter.delete(id)
        item = self.PollList.takeItem(self.PollList.currentRow())
        item = None

    def showPollStats(self):
        pdata = self.dataList[self.PollList.currentRow()]
        print(pdata.paddr)
        self.pollStats = PollStats(pdata)
        self.pollStats.show()

class PollStats(base4,form4):
    def __init__(self,pdata):
        super(base4,self).__init__()
        self.setupUi(self)
        self.setFixedSize(800,600)
        self.pdata = pdata
        self.pidTE.setText(self.pdata.pid)
        self.pQuesTE.setText("Poll Question: "+self.pdata.pques)
        self.pidTE.setReadOnly(True)
        self.pQuesTE.setReadOnly(True)
        self.loadStats()
    def loadStats(self):
        #DataCenter.removeStats(self.pdata.pid)
        #return
        prev_data = DataCenter.readStats(self.pdata.pid)
        if not prev_data:
            data = TransactionManager.updateVotings(poll_addr=self.pdata.paddr)
            countings =  dict(zip(self.pdata.popt,[0]*len(self.pdata.popt)))
            i = 0
            for option in data:
                if option in self.pdata.popt:
                    countings[option]+=1
                i+=1
            prev_data = str(countings)+"*"+str(i)
            print(prev_data)
            DataCenter.writeStats(self.pdata.pid,self.pdata.paddr,prev_data)
        else:
            ind = int(prev_data[0].split('*')[-1])
            data = TransactionManager.updateVotings(poll_addr=self.pdata.paddr,ind = ind)
            #countings =  json.loads(prev_data[0].split('*')[0].replace("'","\""))
            countings =  dict(zip(self.pdata.popt,[0]*len(self.pdata.popt)))
            i = 0
            for option in data:
                if option in self.pdata.popt:
                    countings[option]+=1
                i+=1
            prev_data = str(countings)+"*"+str(i)
            print(prev_data)
            DataCenter.updateStats(self.pdata.pid,prev_data)
        percentages = []
        total = sum(countings.values())
        if total == 0:
            for key in countings:
                self.garb = QtWidgets.QProgressBar()
                self.garb.setFormat(key + u' %p%')
                self.garb.setValue(0)
                self.PHolder.addWidget(self.garb)
        else:
            for key in countings:
                self.garb = QtWidgets.QProgressBar()
                self.garb.setFormat(key + u' %p%')
                self.garb.setValue((countings[key]/total)*100)
                self.PHolder.addWidget(self.garb)


class VoteCause:
    def __init__(self):
        self.app = QtWidgets.QApplication([])
        self.dlg = uic.loadUi(resource_path("main.ui"))
        self.dlg.poll_id.setFocus()
        self.dlg.poll_retrieve.clicked.connect(self.getPollData)
        self.dlg.creator_window.triggered.connect(self.openPollWindow)
        self.dlg.poll_manager.triggered.connect(self.openPollManager)
        self.dlg.VoteButton.clicked.connect(self.finalizeChoice)
        self.dlg.show()
        self.app.exec_()
    def getPollData(self):
        self.error_dialog = QtWidgets.QErrorMessage()
        self.dlg.status.setText("Please wait while we retireve results!")
        self.dlg.pollChoiceList.clear()
        self.dlg.poll_id.setReadOnly(True)
        txid = self.dlg.poll_id.text()
        if not len(txid):
             self.error_dialog.setWindowTitle('Wrong Poll id')
             self.error_dialog.showMessage('Please enter a vailid poll id!')
        else:
            try:
                poll_data = TransactionManager.readUnitFromBlockchain(txid)
                #poll_data='This is a Sample Question*Tarun*ASD*iwie2is*aisdasdsadasdsadasxczx*1*2*3*4*5*6*7*8'
            except:
                self.error_dialog.setWindowTitle('Network Error')
                self.error_dialog.showMessage('Make sure you are connected to FLO Core and have entered correct poll id')
                self.dlg.poll_id.setReadOnly(False)
                return
            poll_data = poll_data.split('*')
            self.to_addr  = poll_data[-1]
            self.dlg.status.setText(poll_data[0])
            self.addCheckbox(poll_data[1:-1])

    def addCheckbox(self,poll_data):
        for choice in poll_data:
            self.dlg.pollChoiceList.addItem(choice)
        #self.groupBox.setLayout(self.dlg.pollLayout)
        self.dlg.VoteButton.setEnabled(True)
        self.dlg.poll_id.setReadOnly(False)

    def finalizeChoice(self):
        option=self.dlg.pollChoiceList.currentItem().text()
        choice = QtWidgets.QMessageBox.question(QtWidgets.QWidget(),"Confirm your vote ?","Are you sure you want to confirm your vote to "+option,QtWidgets.QMessageBox.Yes|QtWidgets.QMessageBox.No)
        if choice==QtWidgets.QMessageBox.Yes:
            try:
                TransactionManager.writeDatatoBlockchain(option,self.to_addr,0.3)
                QtWidgets.QMessageBox(QtWidgets.QMessageBox.Information,"Transaction Success","Successfully casted your vote onto the Blockchain",QtWidgets.QMessageBox.Ok).exec_()

            except Exception as e:
                print(e)
                self.error_dialog = QtWidgets.QErrorMessage()
                self.dlg.status.setText("Error in sending Vote! Please Try again")
        else:
            return

    def openPollWindow(self):
        self.pollWindow = PollCreator()
        self.pollWindow.show()

    def openPollManager(self):
        self.pollMgr = PollManager()
        self.pollMgr.show()

VoteCause()
