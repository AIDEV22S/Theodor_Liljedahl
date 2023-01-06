import PySimpleGUI as sg
import DataBase as db
db.createDatabase()
tableHeadings = ['id', 'First name', 'Last name', 'Adress', 'Postalnumber', 'Postaladress', 'Fees paid?']
def makeNewMemberWindow():
    newMemberWindowLayout = [
        [sg.Text('First name'), sg.Input(key='-NEWFIRSTNAME-')],
        [sg.Text('Last name'), sg.Input(key='-NEWLASTNAME-')],
        [sg.Text('Adress'), sg.Input(key='-NEWADRESS-')],
        [sg.Text('Postalnumber'), sg.Input(key='-NEWPOSTALNUMBER-')],
        [sg.Text('PostalAdress'), sg.Input(key='-NEWPOSTALADRESS-')],
        [sg.Checkbox('Fees paid', key='-NEWFEESPAID-')],
        [sg.Button('Add member', key='-ADDMEMBER-'), sg.Button('Cancel', key='-CANCEL-')]
    ]

    newMemberWindow = sg.Window('New Member', newMemberWindowLayout)
    while True:
        event, values = newMemberWindow.read()
        if event == sg.WINDOW_CLOSED or event == '-CANCEL-':
            newMemberWindow.close()
            break
        if event == '-ADDMEMBER-':
            db.insertMember(db.member(
               firstName=values['-NEWFIRSTNAME-'],
               lastName=values['-NEWLASTNAME-'],
               adress=values['-NEWADRESS-'],
               postalNumber=values['-NEWPOSTALNUMBER-'],
               postalAdress=values['-NEWPOSTALADRESS-'],
               feesPaid=values['-NEWFEESPAID-']))
            newMemberWindow.close()
            break

def searchMemberWindow():
    searchMemberWindowLayout = [
        [sg.Input(key='-SEARCHBAR-'), sg.Text('Search by:'), sg.Button('id', key='-IDSEARCH-'),
         sg.Button('First name', key='-FIRSTNAMESEARCH-'), sg.Button('Last Name', key='-LASTNAMESEARCH-'),
         sg.Button('Adress', key='-ADRESSSEARCH-')],
        [sg.Table([[]], headings=tableHeadings, key='-SEARCHTABLE-')],
        [sg.Button('Exit', key='-EXIT-')]
    ]

    searchMemberWindow = sg.Window('Search Members', layout=searchMemberWindowLayout)
    while True:
        event, values = searchMemberWindow.read()
        if event == '-IDSEARCH-' or event == '-FIRSTNAMESEARCH-' or event == '-LASTNAMESEARCH-' or event == '-ADRESSSEARCH-':
            searchMemberWindow['-SEARCHTABLE-'].update(values=db.searchMembers(values['-SEARCHBAR-'], searchtype=event))
            searchMemberWindow.refresh()
        if event == sg.WINDOW_CLOSED or event == '-EXIT-':
            searchMemberWindow.close()
            break

def confirmWindow():
    confirmWindowLayout = [
        [sg.Text('Are you sure?')],
        [sg.Button('DELETE', key='-DELETE-'), sg.Button('CANCEL', key='-CANCEL-')]
    ]
    confirmWindow = sg.Window('Confirm', confirmWindowLayout)
    while True:
        event, values = confirmWindow.read()
        if event == sg.WINDOW_CLOSED or event == '-CANCEL-':
            confirmWindow.close()
            return False
        if event == '-DELETE-':
            confirmWindow.close()
            return True

def deleteMemberWindow():
    deleteMemberWindowLayout = [
        [sg.Text('Enter the id of the member you want to delete')],
        [sg.Input(key='-DELETEINPUT-')],
        [sg.Button('Confirm', key='-CONFIRM-'), sg.Button('Cancel', key='-CANCEL-')]
    ]

    deleteMemberWindow = sg.Window('Delete Member', layout=deleteMemberWindowLayout)
    while True:
        event, values = deleteMemberWindow.read()
        if event == sg.WINDOW_CLOSED or event == '-CANCEL-':
            deleteMemberWindow.close()
            break
        if event == '-CONFIRM-':
            if confirmWindow() == True:
                db.deleteMember(values['-DELETEINPUT-'])
                deleteMemberWindow.close()
                break

def mainWindow():
    mainWindowLayout = [
        [sg.Table(db.getMemberList(), headings=tableHeadings, key='-MAINTABLE-')],
        [sg.Button('Search members', key='-SEARCH-'), sg.Button('Add new member', key='-ADDNEW-'), sg.Button('Remove member', key='-DELETE-')]
    ]

    mainWindow = sg.Window('Members List', mainWindowLayout)
    while True:
        event, values = mainWindow.read()
        if event == '-SEARCH-':
            searchMemberWindow()
        if event == '-ADDNEW-':
            makeNewMemberWindow()
            mainWindow['-MAINTABLE-'].update(values=db.getMemberList())
        if event == '-DELETE-':
            deleteMemberWindow()
            mainWindow['-MAINTABLE-'].update(values=db.getMemberList())
        if event == sg.WINDOW_CLOSED:
            break
mainWindow()