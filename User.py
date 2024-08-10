from Transactions import Transaction
from Book import Book, Copy
from datetime import date
from dateutil.relativedelta import relativedelta

class User:
    def __init__(self, ID, password, name, phone_no, address, library, 
                 transaction_log, link_book):
        self.__userID = ID                          # string entered by the user
        self.__password = password                  # string entered by the user
        self.__name = name
        self.__phoneNo = phone_no                   # since it is a local library, the phone number format is unified (string)
        self.__address = address                    # since it is a local library, the address will only consist of the neighborhood area
        self._borrowedBooks = {}                   # {'Book Name': Transaction_obj}
        self._reservedBooks = []                   # list of reserved books ['Book name']
        self._fines = 0                            # fines are calculated after returning the book
        self._library = library                    # {'Book ISBN': book_obj}
        self._transactionLog = transaction_log     # {Transc ID: trans_obj}
        self._linkBook = link_book                 # {'Book Name': 'Book ISBN'}




    # Getter functions
    def get_ID(self):
        return self.__userID
    
    def get_name(self):
        return self.__name
    
    def get_address(self):
        return self.__address
    
    def get_password(self):
        return self.__password



    # Display functions
    def display_fine(self):
        print('Your total accumulated fines:', self._fines)
    
    def display_reservedBooks(self):
        print('**Reserved Books**')
        if(len(self._reservedBooks) == 0):
            print('You do not have any reserved books currently')
        else:
            for i in self._reservedBooks:
                print(i)

    def display_borrowedBooks(self):
        print("**Borrowed Books**")
        if(len(self._borrowedBooks) == 0):
            print('There are no borrowed books currently')
        else:
            for book in self._borrowedBooks:
                print('Book Name:', book, end='\t')
                self._borrowedBooks[book].calculate_dueDate()
    
    def display_info(self):
        print('**User Information**')
        print('Name:', self.__name)
        print('ID:', self.__userID)
        print('Phone:', self.__phoneNo)
        print('Address:', self.__address)
        print('Fines:', self._fines)
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
        if(book_name not in self._linkBook):
            print('Book not available in the library')

        else:
            book_ISBN = self._linkBook[book_name]
            book_obj = self._library[book_ISBN]
            
            copies = book_obj.get_copies()                          # returns {'Copy ID' : Copy obj}
            trans = -1                                              # transaction object is created once copy is available
            
            for copyID in copies:
                if copies[copyID].get_status() == 'Available':      
                    waitList = book_obj.get_waitlist()

                    if(len(waitList) > 0):                                                  # if the book is available, check if there is someone reserving the book
                        if(waitList[0] != self.__userID):
                            if(book_name in self._reservedBooks):                           # It means the user has already reserved the book previously
                                print('Book has already been previously reserved by you')   
                                print('Your turn has not come yet in the waitlist!')
                                return
                            else:
                                book_obj.add_waitlist(self.__userID)
                                self._reservedBooks.append(book_name)
                                print('Can not borrow the book, as the book is reserved.')
                                print('You have been added to the waitlist')
                            
                            break
                        else:
                            book_obj.remove_from_waitlist(self.__userID)
                            self._reservedBooks.remove(book_name)
                    
                    # book is available and not reserved, or it is the user's turn to borrow it
                    trans = Transaction(transID, book_ISBN, copyID, self.__userID, returningDate, lateFine)
                    copies[copyID].change_status('Borrowed', transID)
                    self._transactionLog[transID] = trans
                    self._borrowedBooks[book_name] = trans
                    break
            

            # no copies are availabe
            if (trans == -1):
                if(book_name in self._reservedBooks):
                    print('Book has already been previously reserved by you.')
                    print('The book is still not available')
                else:
                    book_obj.add_waitlist(self.__userID)
                    self._reservedBooks.append(book_name)
                    print('Can not borrow the book, as the book is reserved.')
                    print('You have been added to the waitlist')

    # function to return book and add fine
    def return_book(self, book_name):
        if(book_name not in self._borrowedBooks):
            print('Book was not borrowed')
            return
        
        trans_obj = self._borrowedBooks[book_name]

        del self._borrowedBooks[book_name]
        self._fines += trans_obj.return_book()             # Function updates the fine according to returning date
                                                            # and updates transaction status to 'Returned'
        # change copy status
        copyID = trans_obj.get_copyID()
        book_ISBN = self._linkBook[book_name]
        book_obj = self._library[book_ISBN]
        book_obj.change_copy_status(copyID, 'Available')

        print('Book has been returned')

    # function to check borrowed book due date
    def check_DueDate(self, book_name):
        if(book_name not in self._borrowedBooks):
            print('Book was not borrowed')
            return
        
        if book_name in self._borrowedBooks:
            trans_obj = self._borrowedBooks[book_name]
            trans_obj.calculate_dueDate()
        else:
            print('Book was already returned')

    def reserve_book(self, book_name):
        if(book_name in self._reservedBooks):
            print('Book has already been previously reserved by you')

        else:
            book_ISBN = self._linkBook[book_name]
            book_obj = self._library[book_ISBN]

            if len(book_obj.get_waitlist()) == 0:
                copies = book_obj.get_copies()
                for copy in copies:
                    if copies[copy].get_status() == 'Available':
                        print('There is a copy available, no need to reserve')
                        return

            book_obj.add_waitlist(self.__userID)
            self._reservedBooks.append(book_name)
    
    def delete_reservation(self, book_name):
        if(book_name not in self._reservedBooks):
            print('Book was not reserved by you')

        else:
            book_ISBN = self._linkBook[book_name]
            book_obj = self._library[book_ISBN]

            book_obj.remove_from_waitlist(self.__userID)
            self._reservedBooks.remove(book_name)

    # function to pay fines
    def pay_fine(self):
        if(self._fines == 0):
            print('All fines are paid')
        else:
            print('Total accumulated fines:', self.__fines)
            payment_amount = float(input('Please enter the amount you want to pay '))
            if(payment_amount > self._fines):
                print('You are paying much more than the intended amount')
                return
            
            self._fines -= payment_amount

    








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
        self.__endDate = date.today() + relativedelta(months=membership_plan)



    # Addition to borrow function to check whether membership is expired or not
    # if it is expired, user can not borrow book
    # and to view books
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
        if len(self._library) == 0:
            print('Library is empty!')
            return
        
        for book in self._library:
            print("******************************")
            self._library[book].display_book_info()
            print()
        
        cop = input('Would you like to see available copies? y/n ')
        while (cop == 'y'):
            book = input('Please enter book ISBN as displayed above ')
            if(book in self._library):
                self._library[book].display_copies()
            else:
                print('Wrong ISBN')
                
            print()
            cop = input('Would you like to see available copies? y/n ')






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
                 transaction_log, link_book, user):
        super().__init__(ID, password, name, phone_no, address, library, 
                 transaction_log, link_book) 
        self.__users = user                          # {'User #ID': ['admin/member', user_obj]}
    


    # Book Copy Update operations
    def add_copy(self, book_ISBN, copy_id):
        if (book_ISBN not in self._library):
            print('Invalid ISBN')
            return
        book_obj = self._library[book_ISBN]                        # self.__library = {'Book ISBN': book_obj}
        book_obj.add_copy(copy_id)
        print('Copy has been added')

    def remove_copy(self, book_ISBN, copy_id):
        if(book_ISBN not in self._library):
            print('Book does not exist')
            return

        book_obj = self._library[book_ISBN]
        copies = book_obj.get_copies()
        if(copy_id not in copies):
            print('Copy ID does not exist')
            return
        
        if(copies[copy_id].get_status() == 'Borrowed'):
            print('Copy is borrowed! Can not delete')
            return

        book_obj.delete_copy(copy_id)
        print('Copy has been removed')

        if(len(copies) == 0):                                      # if all copies were deleted, then
            book_name = self._library[book_ISBN].get_name()        # the book isn't available anymore
            del self._library[book_ISBN]                           # so it is deleted from library book list
            del self._linkBook[book_name]
            print('Book has been removed, as no more copies are left')



    # Book Update operations
    def add_book(self, ISBN, title, author, publisher, edition, category, copy_id):
        if(ISBN in self._library):
            print('The book is already in the library')
        else:
            new_book = Book(ISBN, title, author, publisher, edition, category)
            new_book.add_copy(copy_id)
            self._library[ISBN] = new_book
            self._linkBook[title] = ISBN
        
        print(f'{title} has been successfully added to the library')


    def remove_book(self, book_ISBN):
        if(book_ISBN not in self._library):                     
            print('Book is already not in the library')
            return
        
        copies = self._library[book_ISBN].get_copies()                          
        for copy in copies:
            if(copies[copy].get_status() == 'Borrowed'):                        # checks is there is a borrowed copy or not
                print('There is a copy borrowed! Book can not be deleted')      # if there is, book can not be deleted from the system
                return
        
        del self._library[book_ISBN]
        print('Book has been deleted \n')                
                                                                    



    # Display Functions
    # Function to display member info for tracking purposes
    # User object is passed 
    def member_info(self, user_ID):
        if(self.__users[user_ID][0] == 'ADMIN'):
            print('Can not access other admins info')
            return
        
        if(user_ID not in self.__users):
            print('User ID not found')
            return

        user_obj = self.__users[user_ID][1]          
        user_obj.display_info()
    
    def view_books(self):
        if len(self._library) == 0:
            print('Library is empty!')
            return

        for book in self._library:
            print("******************************")
            self._library[book].display_book_info()
            print()
        
        cop = input('Would you like to see available copies? y/n ')
        while (cop == 'y'):
            book = input('Please enter book ISBN as displayed above ')

            if(book in self._library):
                self._library[book].admin_display_copies()
            else:
                print('Book is not available in the library!')
            
            print()
            cop = input('Would you like to see available copies? y/n ') 

    def view_transaction_log(self):
        if(len(self._transactionLog) == 0):
            print('No transactions have been done yet!')
            return
        
        for transID in self._transactionLog:               # {Transc ID: trans_obj}
            print("*****************************")
            self._transactionLog[transID].display_info()
    
    def view_waitList(self, book_ISBN):
        if(book_ISBN not in self._library):
            print('Book not available in library')
            return
        
        book_obj = self._library[book_ISBN]
        book_obj.display_waitList()






# Functions test
# books = {}                  # {'Book ISBN' : book_obj}
# link_book = {}              # {'Book Name': 'Book ISBN'}
# user = {}                   # {User #ID: ['password', 'admin/member', user_obj]}
# transaction_log = {}        # {Transc ID: trans_obj}

# temporarily, there are set as counters for testing
# userID_CNT = 1
# transc_CNT = 1

# # the information is taken from the user
# admin1 = Admin(userID_CNT, 'PASSWORD', 'Jason', '+962 999999', 'Amman', books, transaction_log, link_book, user)
# user[userID_CNT] = ['PASSWORD', 'ADMIN', admin1]
# userID_CNT += 1

# admin1.add_book('1555', 'AGGGTM', 'P', 'Penguin', '1st', 'Drama', '1')
# admin1.add_book('8889', 'A book', 'P', 'Penguin', '2nd', 'Thriller', '9')
# admin1.view_books()

# print('****************')
# admin1.remove_book('8889')
# admin1.add_copy('1555', '2')
# admin1.remove_copy('1555', '1')
# admin1.view_books()
# admin1.display_info()

# print()
# print()
# print('********************************')
# member1 = Member(userID_CNT, 'Pass', 'Jack', '+962 7777777', 'Irbid', books, transaction_log, link_book, 3)
# user[userID_CNT] = ['Pass', 'MEMBER', member1]
# userID_CNT += 1

# print('Member1 membership date expiration')
# member1.days_left()
# print()
# member1.borrow_book('AGGGTM', transc_CNT, date(2024, 8, 10), 2)
# transc_CNT += 1
# print('admin1 trying to borrow the same book')
# admin1.borrow_book('AGGGTM', transc_CNT, date(2024, 8, 10), 2)
# transc_CNT += 1

# print('Admin information')
# admin1.display_info()
# print()
# print("Admin 1 viewing member1's info")
# admin1.member_info(2)

# print()
# print('Viewing books after reserving them')
# admin1.view_books()
# print()
# print('Viewing waitlist for book')
# admin1.view_waitList('1555')
# print()
# print('Viewing transaciton log')
# admin1.view_transaction_log()
# print()

# print('Member1 checking the due date for returning the book')
# member1.check_DueDate('AGGGTM')
# print()
# print('Returning the book')
# member1.return_book('AGGGTM')
# print()
# print("Viewing member1's info after returning")
# member1.display_info()
# print()
# print('Book statuses')
# admin1.view_books()
# print()
# print('Transaction log')
# admin1.view_transaction_log()