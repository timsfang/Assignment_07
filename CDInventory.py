#------------------------------------------#
# Title: CDInventory.py
# Desc: Starter Script from Assignment 06 used for Assignment 07
# Change Log: (Who, When, What)
# DBiesinger, 2030-Jan-01, Created File
# TFang, 2021-Nov-20, Modified script to complete assignment todo's
# TFang, 2021-Nov-26, Script updated based on feedback from Laura Denney, TA:
#   'strFileName' replaced with 'file_name' within read_file and write_file functions
#   previous IO.user_input modified to separate I/O and DataProcessor
# TFang, 2021-Nov-28, Modified script to add exception handling and utilize binary data
#------------------------------------------#

# -- DATA -- #
import pickle
strChoice = '' # User input
lstTbl = []  # list of lists to hold data
dicRow = {}  # list of data row
strFileName = 'CDInventory.dat'  # data storage file
objFile = None  # file object
strID = '' # added as global variable for elif choice 'a'
strTitle = '' # added as global variable for elif choice 'a'
stArtist = '' # added as global variable for elif choice 'a'

# -- PROCESSING -- #
class DataProcessor:
    """Processing the data to remove from in-memory"""

    @staticmethod
    def delete_cd():
        """Function to delete CDs from in-memory table with user input identified by 'ID'
        
        Arg:
            None.
        
        Returns:
            None.
        """
        intRowNr = -1
        blnCDRemoved = False
        for row in lstTbl:
            intRowNr += 1
            if row['ID'] == intIDDel:
                del lstTbl[intRowNr]
                blnCDRemoved = True
                break
        if blnCDRemoved:
            print('The CD was removed')
        else:
            print('\nCould not find this CD!')

    @staticmethod
    def add_cd(strID, strTitle, stArtist):
        """Function to append CDs to im-memory table with user input from IO.user_input
        
        Arg:
            strID: identifier obtained from user, later converted to integer
            strTitle: name of CD title
            stArtist: name of CD artist
        
        Returns:
            None.
        """
        intID = int(strID)
        dicRow = {'ID': intID, 'Title': strTitle, 'Artist': stArtist}
        lstTbl.append(dicRow)


class FileProcessor:
    """Processing the data to and from text file"""

    @staticmethod
    def read_file(file_name, table):
        """Function to manage data ingestion from file to a list of dictionaries

        Reads the data from file identified by file_name into a 2D table
        (list of dicts) table one line in the file represents one dictionary row in table.
        
        Changed code to read binary file vs text file
        Added exception handling if *.dat file is not in local folder

        Args:
            file_name (string): name of file used to read the data from
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime

        Returns:
            None.
        """
        table.clear()  # this clears existing data and allows to load data from file
        try:
            with open(file_name, 'rb') as fileObj:  # code to pickle
                data = pickle.load(fileObj)
            return data
        except FileNotFoundError:  # exception trapped here
            print('*.dat file not found. Proceeding to Menu: \n')
        except EOFError:
            print('*.dat file is empty.')

    @staticmethod
    def write_file(file_name, table):
        """Function to save data to file
        
        Changed code to write binary file vs text file
        Writes the data from 2D table to file identified by file_name

        Args:
            file_name (string): name of file used to write the data to
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime

        Returns:
            None.
        """
        with open(file_name, 'wb') as fileObj:  # code to unpickle
            pickle.dump(table, fileObj)

        
# -- PRESENTATION (Input/Output) -- #
class IO:
    """Handling Input / Output"""

    @staticmethod
    def print_menu():
        """Displays a menu of choices to the user

        Args:
            None.

        Returns:
            None.
        """
        print('\nMenu\n\n[l] load Inventory from file\n[a] Add CD\n[i] Display Current Inventory')
        print('[d] delete CD from Inventory\n[s] Save Inventory to file\n[x] exit\n')

    @staticmethod
    def menu_choice():
        """Gets user input for menu selection

        Args:
            None.

        Returns:
            choice (string): a lower case sting of the users input out of the choices l, a, i, d, s or x
        """
        choice = ' '
        while choice not in ['l', 'a', 'i', 'd', 's', 'x']:
            choice = input('Which operation would you like to perform? [l, a, i, d, s or x]: ').lower().strip()
        print()  # Add extra space for layout
        return choice

    @staticmethod
    def show_inventory(table):
        """Displays current inventory table

        Args:
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime.

        Returns:
            None.
        """
        print('======= The Current Inventory: =======')
        print('ID\tCD Title (by: Artist)\n')
        for row in table:
            print('{}\t{} (by:{})'.format(*row.values()))
        print('======================================')

    @staticmethod
    def user_input(strID, strTitle, stArtist):
        """Function to ask user for input and appends input to 2D table data

        Obtains user input for CD ID, title, and artist, then appends info to 2D list of dictionaries

        Args:
            strID (string): identifier obtained from user, later converted to integer
            strTitle (string): name of CD title
            stArtist (string): name of CD artist

        Returns:
            None.            
        """
        strID = input('Enter ID: ').strip()
        strTitle = input('What is the CD\'s title? ').strip()
        stArtist = input('What is the Artist\'s name? ').strip()
        return strID, strTitle, stArtist

# 1. When program starts, read in the currently saved Inventory
FileProcessor.read_file(strFileName, lstTbl)
# 2. start main loop
while True:
    # 2.1 Display Menu to user and get choice
    IO.print_menu()
    strChoice = IO.menu_choice()
    # 3. Process menu selection
    # 3.1 process exit first
    if strChoice == 'x':
        break
    # 3.2 process load inventory
    if strChoice == 'l':
        print('WARNING: If you continue, all unsaved data will be lost and the Inventory re-loaded from file.')
        strYesNo = input('type \'yes\' to continue and reload from file. otherwise reload will be canceled: ')
        if strYesNo.lower() == 'yes':
            print('\nreloading... Done. Returning to Menu: \n')
            data = FileProcessor.read_file(strFileName, lstTbl)  # unpickled info assigned to variable named data in order for choice 'i' to work
        else:
            input('canceling... Inventory data NOT reloaded. Press [ENTER] to continue to the menu.')
        continue  # start loop back at top.
    # 3.3 process add a CD
    elif strChoice == 'a':
        # 3.3.1 Ask user for new ID, CD Title and Artist and unpack for use in separate append function
        strID, strTitle, stArtist = IO.user_input(strID, strTitle, stArtist)
        # 3.3.2 Add CD to the table
        try:
            DataProcessor.add_cd(strID, strTitle, stArtist)
        except ValueError:  # exception trapped here
            print('\nID entry was not a number. CD could not be added.')
        IO.show_inventory(lstTbl)
        print('Please enter a number as ID. Returning to Menu: \n')
        continue  # start loop back at top.
    # 3.4 process display current inventory
    elif strChoice == 'i':
        try:
            IO.show_inventory(data)
        except NameError:  # exception trapped here
            IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.5 process delete a CD
    elif strChoice == 'd':
        # 3.5.1 get Userinput for which CD to delete
        # 3.5.1.1 display Inventory to user
        IO.show_inventory(lstTbl)
        # 3.5.1.2 ask user which ID to remove 
        try:
            intIDDel = int(input('Which ID would you like to delete? ').strip())
        except ValueError:  # exception trapped here
            print('\nID entry was not a number. CD could not be deleted.')
            IO.show_inventory(lstTbl)
            print('Please enter a number as ID. Returning to Menu: \n')
        # 3.5.2 search thru table and delete CD
        else:
            DataProcessor.delete_cd()
            IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.6 process save inventory to file
    elif strChoice == 's':
        # 3.6.1 Display current inventory and ask user for confirmation to save
        IO.show_inventory(lstTbl)
        strYesNo = input('Save this inventory to file? [y/n] ').strip().lower()
        # 3.6.2 Process choice
        if strYesNo == 'y':
            # 3.6.2.1 save data
            FileProcessor.write_file(strFileName, lstTbl)
        else:
            input('The inventory was NOT saved to file. Press [ENTER] to return to the menu.')
        continue  # start loop back at top.
    # 3.7 catch-all should not be possible, as user choice gets vetted in IO, but to be save:
    else:
        print('General Error')