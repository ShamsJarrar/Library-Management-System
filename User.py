from Transactions import Transaction
from datetime import date

class User:
    def __init__(self, ID, password, name, phone_no, address):
        self.__userID = ID                  # generated integer once account is created
        self.__password = password          # string entered by the user
        self.__name = name
        self.__phoneNo = phone_no           # since it is a local library, the phone number format is unified (string)
        self.__address = address            # since it is a local library, the address will only consist of the neighborhood area
        self.__borrowedBooks = {}           # {'Book Name': Transaction_obj}
        self.__reservedBooks = []           # list of reserved books
        self.__fines = 0                    # fines are calculated after returning the book


    def get_ID(self):
        return self.__userID
    
    def get_name(self):
        return self.__name
    
    def get_address(self):
        return self.__address
    

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


    # Admin users can view certain user details for contact reasons
    def admin_display(self):
        print('**User Information**')
        print('Name:', self.__name)
        print('ID:', self.__userID)
        print('Phone:', self.__phoneNo)
        print('Address:', self.__address)
        print('Fines:', self.__fines)
        self.display_borrowedBooks()
        self.display_reservedBooks()


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
    

    # function to add borrowed book with its following transaction object which soters all transaction details
    # and delete book from reserved list
    # Transactions are created outside of the object
    # the purpose of the following function is just to record borrowed books for the user
    def borrow_book(self, book_name, transc_obj):
        self.__borrowedBooks[book_name] = transc_obj
        
        if(book_name in self.__reservedBooks):
            self.__reservedBooks.remove(book_name)
    
    
    # function to add reserved book to list
    def reserve_book(self, book_name):
        self.__reservedBooks.append(book_name)
    
    
    # function to return book and add fine
    def return_book(self, book_name): 
        self.__fines += self.__borrowedBooks[book_name].return_book()
        del self.__borrowedBooks[book_name]
    

    # function to pay fines
    def pay_fine(self):
        if(self.__fines == 0):
            print('All fines are paid')
        else:
            print('Total accumulated fines:', self.__fines)
            payment_amount = float(input('Please enter the amount you want to pay '))
            self.__fines -= payment_amount


# Functions test
# user = User(123, 'something', 'someone', '123456', 'Hawaii')
# transaction = Transaction(1, '12345', '1', 123, date(2024, 9, 9), 2)
# user.borrow_book('AGGGTM', transaction)
# user.reserve_book('Yellow')
# user.admin_display()
# user.return_book('AGGGTM')
# transaction.display_info()
# user.admin_display()

