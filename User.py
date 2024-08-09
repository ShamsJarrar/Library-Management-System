from Transactions import Transaction
from Book import Book, Copy
from datetime import date
from dateutil.relativedelta import relativedelta

class User:
    def __init__(self, ID, password, name, phone_no, address, library, 
                 transaction_log, link_book):
        self.__userID = ID                          # generated integer once account is created
        self.__password = password                  # string entered by the user
        self.__name = name
        self.__phoneNo = phone_no                   # since it is a local library, the phone number format is unified (string)
        self.__address = address                    # since it is a local library, the address will only consist of the neighborhood area
        self.__borrowedBooks = {}                   # {'Book Name': Transaction_obj}
        self.__reservedBooks = []                   # list of reserved books
        self.__fines = 0                            # fines are calculated after returning the book
        self.__library = library                    # {'Book ISBN': book_obj}
        self.__transactionLog = transaction_log     # {Transc ID: trans_obj}
        self.__linkBook = link_book                 # {'Book Name': 'Book ISBN'}




    # Getter functions
    def get_ID(self):
        return self.__userID
    
    def get_name(self):
        return self.__name
    
    def get_address(self):
        return self.__address
    



    # Display functions
    def display_fine(self):
        print('Your total accumulated fines:', self.__fines)
    
    def display_reservedBooks(self):
        print('**Reserved Books**')
        if(len(self.__reservedBooks) == 0):
            print('You do not have any reserved books currently')
        else:
            for i in self.__reservedBooks:
                print(i)

    def display_borrowedBooks(self):
        print("**Borrowed Books**")
        if(len(self.__borrowedBooks) == 0):
            print('There are no borrowed books currently')
        else:
            for book in self.__borrowedBooks:
                print('Book Name:', book, end='\t')
                self.__borrowedBooks[book].calculate_dueDate()
    
    def display_info(self):
        print('**User Information**')
        print('Name:', self.__name)
        print('ID:', self.__userID)
        print('Phone:', self.__phoneNo)
        print('Address:', self.__address)
        print('Fines:', self.__fines)
        self.display_borrowedBooks()
        self.display_reservedBooks()


    # Information update functions
    def change_password(self):
        check = input('Please enter your old password: ')
        if(check == self.__password):
            self.__password = input('Please enter your new password: ')
        else:
            print('Unable to verify your identity, please visit IT department if you can not remember your password')
    
    def change_phoneNo(self):
        self.__phoneNo = input('Please enter your new phone number: ')
    
    def change_address(self):
        self.__address = input('Please enter your new address: ')
    



    # Operation functions
    # Function for the user to borrow a book
    def borrow_book(self, book_name, transID, returningDate, lateFine):
        if(book_name not in self.__linkBook):
            print('Book not available in the library')

        else:
            book_ISBN = self.__linkBook[book_name]
            book_obj = self.__library[book_ISBN]
            
            copies = book_obj.get_copies()                          # returns {'Copy ID' : Copy obj}
            trans = -1                                              # transaction object is created once copy is available
            
            for copyID in copies:
                if copies[copyID].get_status() == 'Available':      # if book is available, check is there is someone reservingt the book
                    waitList = book_obj.get_waitlist()

                    if(len(waitList) > 0):
                        if(waitList[0] != self.__userID):
                            book_obj.add_waitlist(self.__userID)
                            self.__reservedBooks.append(book_name)
                            print('Can not borrow the book, as the book is reserved.')
                            print('You have been added to the waitlist')
                        else:
                            book_obj.remove_from_waitlist()
                            self.__reservedBooks.remove(book_name)
                    
                    # book is available and not reserved, or it is the user's turn to borrow it
                    trans = Transaction(transID, book_ISBN, copyID, self.__userID, returningDate, lateFine)
                    copies[copyID].change_status('Borrowed', transID)
                    self.__transactionLog[transID] = trans
                    self.__borrowedBooks[book_name] = trans
            

            # no copies are availabe
            if (trans == -1):
                waitList.append(self.__userID)
                self.__reservedBooks.append(book_name)
                print('Can not borrow the book, as the book is reserved.')
                print('You have been added to the waitlist')

    # function to return book and add fine
    def return_book(self, book_name):
        trans_obj = self.__borrowedBooks[book_name]

        del self.__borrowedBooks[book_name]
        self.__fines += trans_obj.return_book()             # Function updates the fine according to returning date
        
        # change copy status
        copyID = trans_obj.get_copyID()
        book_ISBN = self.__linkBook[book_name]
        book_obj = self.__library[book_ISBN]
        book_copies = book_obj.get_copies()                 # {'Copy ID' : copy_obj}
        book_copies[copyID].change_status('Available')

    # function to check borrowed book due date
    def check_DueDate(self, book_name):
        if book_name in self.__borrowedBooks:
            trans_obj = self.__borrowedBooks[book_name]
            trans_obj.calculate_dueDate()
        else:
            print('Book was already returned')

    # function to pay fines
    def pay_fine(self):
        if(self.__fines == 0):
            print('All fines are paid')
        else:
            print('Total accumulated fines:', self.__fines)
            payment_amount = float(input('Please enter the amount you want to pay '))
            self.__fines -= payment_amount







# class to define library Member users
class Member(User):
    def __init__(self, ID, password, name, phone_no, address, library, 
                 transaction_log, link_book, membership_plan):
        super().__init__(ID, password, name, phone_no, address, library, transaction_log, link_book)
        self.__startDate = date.today()                                           # Membership Start date
        self.__endDate = date.today() + relativedelta(months=membership_plan)     # Calculates enddate according to membership plan
                                                                                  # Fees are expected to be paid instantly and not gradually




    # Membership Functions 
    # function that prints how many days are left until
    # the membership expires
    def days_left(self):
        if(date.today() <= self.__endDate):
            print((self.__endDate - date.today()).days, 'days left until membership expires')
        else:
            print('Membership already Expired!')
            print('Please renew your membership!')
    
    # function to renew memberhsip
    def renew_membership(self, membership_plan):
        self.__startDate = date.today()                                           
        self.__endDate = date.today() + relativedelta(years=membership_plan)




    # Addition to borrow function to check whether membership is expired or not
    # if it is expired, user can not borrow book
    def borrow_book(self, book_name, transID, returningDate, lateFine):
        if(date.today() > self.__endDate):
            print('Membership has expired!')
            print('Please renew your membership to be able to borrow books')
        else:
            super().borrow_book(book_name, transID, returningDate, lateFine)
    



    # Display Functions
    def display_info(self):
        super().display_info()
        print('Membership start date:', self.__startDate)
        print('Member end date:', self.__endDate)
    
    def view_books(self):
        for book in self.__library:
            self.__library[book].display_book_info()
        
        cop = input('Would you like to see available copies? y/n')
        while (cop == 'y'):
            book = input('Please enter book ISBN as displayed above')
            self.library[book].display_copies()
            cop = input('Would you like to see available copies? y/n')






# Class to define Admin users
# Admins can add and remove books to the library 
# Adds copies and remove copies
# View User details except for other admins
# View transaction log

# Admins can also borrow, reserve and return books

# for employee details, the feature can be added later for HR team
# to be able to add employee salary, start date, and all employee details
# but for this class, it is for library and member management
class Admin(User):
    def __init__(self, ID, password, name, phone_no, address, library, 
                 transaction_log, link_book):
        super().__init__(ID, password, name, phone_no, address, library, 
                 transaction_log, link_book) 
    



    # Book Copy Update operations
    def add_copy(self, book_ISBN, copy_id):
        book_obj = self.__library[book_ISBN]                        # self.__library = {'Book ISBN': book_obj}
        book_obj.add_copy(copy_id)

    def remove_copy(self, book_ISBN, copy_id):
        book_obj = self.__library[book_ISBN]
        book_obj.delete_copy(copy_id)

        if(len(book_obj.get_copies()) == 0):                        # if all copies were deleted, then
            book_name = self.__library[book_ISBN].get_name()        # the book isn't available anymore
            del self.__library[book_ISBN]                           # so it is deleted from library book list
            del self.__linkBook[book_name]




    # Book Update operations
    def add_book(self, ISBN, title, author, publisher, edition, category, copy_id):
        if(ISBN in self.__library):
            print('The book is already in the library')
        else:
            new_book = Book(ISBN, title, author, publisher, edition, category)
            new_book.add_copy(copy_id)
            self.__library[ISBN] = new_book
            self.__linkBook[title] = ISBN


    def remove_book(self, book_ISBN):
        book_name = self.__library[book_ISBN].get_name()        
        del self.__library[book_ISBN]                           
        del self.__linkBook[book_name]




    # Display Functions
    # Function to display member info for tracking purposes
    # User object is passed 
    def member_info(self, user_obj):                  
        user_obj.display_info()
    
    def view_books(self):
        for book in self.__library:
            self.__library[book].display_book_info()
        
        cop = input('Would you like to see available copies? y/n')
        while (cop == 'y'):
            book = input('Please enter book ISBN as displayed above')
            self.library[book].admin_display_copies()
            cop = input('Would you like to see available copies? y/n') 

    def view_transaction_log(self):
        for transID in self.__transactionLog:               # {Transc ID: trans_obj}
            print("*****************************")
            self.__transactionLog[transID].display_info()
    
    def view_waitList(self, book_ISBN):
        book_obj = self.__library[book_ISBN]
        book_obj.display_waitList()

