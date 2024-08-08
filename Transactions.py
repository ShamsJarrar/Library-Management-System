from datetime import date

# object to save transaction details
class Transaction:
    def __init__(self, ID, bookID, copyID, userID, returning_date, late_fine):
        self.__ID = ID                          # integer to specify transaction ID
        self.__bookISBN = bookID                # Information about the book involved in the transaction
        self.__bookCopyID = copyID
        self.__userID = userID                  # User ID involved in transaction
        self.__borrowDate = date.today()        # the date the transation actually occured
        self.__returningDate = returning_date   # the date the user is supposed to return the book
        self.__actual_returned_date = -1        # the date the user actually returned the book
        self.__fine = 0
        self.__status = 'Borrow'
        self.__fineValue = late_fine            # factor to multiply with for every late day
    
    # when transaction occurs, other functions change the status of the copy of the book
    # the purpose of the class is the log all transactions
    # and connect user details with book details and transaction details
    # and to be able to calculate fines

    def get_ID(self):
        return self.__ID
    
    def get_bookISBN(self):
        return self.__bookISBN
    
    def get_copyID(self):
        return self.__bookCopyID
    
    def get_userID(self):
        return self.__userID
    
    def get_status(self):
        return self.__status
    
    def get_fine(self):
        return self.__fine
    
    # this function is for displaying info for admins for purposes of tracking
    def display_info(self):
        print('Transaction ID:', self.__ID)
        print('Book ISBN:', self.__bookISBN)
        print('Copy ID:', self.__bookCopyID)
        print('User ID:', self.__userID)
        print('Borrow date:', self.__borrowDate)
        print('Returning date:', self.__returningDate)
        print('Status:', self.__status)
        if(self.__status == 'Returned'):
            print('Returned date:', self.__actual_returned_date)
            print('Fine:', self.__fine)
    

    #function to calculate how many days are left to return the borrowed book
    def calculate_dueDate(self):
        if(self.__status == 'Returned'):
            print('Book was returned')
        else:
            if(date.today() < self.__returningDate):
                print((self.__returningDate - date.today()).days, 'days left')
            else:
                print((date.today() - self.__returningDate).days, 'days overdue')
    

    # function to change status of the transaction and calculate the fine for the user based
    # on the difference between the actual returningDate and the day the user was supposed to originall return
    # the function return the fine value so that it is changed also changed in the user's objects too

    def return_book(self):
        self.__status = 'Returned'
        self.__actual_returned_date = date.today()

        # for testing purposes
        # self.__actual_returned_date = date(2024, 9, 19)

        if(self.__actual_returned_date > self.__returningDate):
            self.__fine = (self.__actual_returned_date - self.__returningDate).days * self.__fineValue
        
        return self.__fine



# Function Tests
# transactions = {}
# transactions[1] = Transaction(1, '12345', '1', 123, date(2024, 9, 9), 2)
# transactions[1].display_info()
# transactions[1].calculate_dueDate()
# print(transactions[1].return_book())
# print(transactions[1].get_status())
