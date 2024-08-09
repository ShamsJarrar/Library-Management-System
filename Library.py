from User import *
import random

# Global Variables for use throughout the program
library = {}                # {'Book ISBN': book_obj} -> waitlist consists of user IDs inside the object
link_book = {}              # {'Book Name': 'Book ISBN'}, helps find book ISBN if search was done through book's name
user = {}                   # {'UserID': ['password', 'ADMIN/MEMBER', user_obj]}
transaction_log = {}        # {Transc ID: trans_obj}, transaction ID is generated randomly
lateFine = 2                # Number set by library as the standard fine for every late day

## Note can find additional function to initialize library with books
## without having to sign up first as admin below
## function name is Initialize library


#*****************************Main Interface*****************************
def main():
    choice = 'S'
    
    while (choice.upper() != 'E'):
        choice = input('Would you like to Login in (L) or Sign up (S)? L/S or E(Stop Run) ')
        print()

        if choice.upper() == 'S':
            Sign_Up()
        
        elif choice.upper() == 'L':
            Login()
    
    print('Thank you for using our software')


def Sign_Up():
    print("******************Sign Up******************")
    tpe = input('Would you like to Sign Up as an Admin (A) or Member (M)? A/M ')

    if tpe.upper() == 'A':
        print('Please enter the following information: ')
        user_ID = input('UserID: ')
        while (user_ID in user):
            print('UserID already taken. Try another ID.')
            user_ID = input('UserID: ')
        
        password = input('Password: ')
        name = input('Name: ')
        phone_no = input('Phone No.: ')
        address = input('Address (neighborhood): ')

        new_admin = Admin(user_ID, password, name, phone_no, address, library, 
                 transaction_log, link_book, user)
        
        user[user_ID] = [password, 'ADMIN', new_admin]
        print('You have successfully registered, please proceed to Login page')


    elif tpe.upper() == 'M':
        print('Please enter the following information: ')
        user_ID = input('UserID: ')
        while (user_ID in user):
            print('UserID already taken. Try another ID.')
            user_ID = input('UserID: ')
        
        password = input('Password: ')
        name = input('Name: ')
        phone_no = input('Phone No.: ')
        address = input('Address (neighborhood): ')
        membership_plan = int(input('Please enter how many months to you want to join for (membership plan): '))

        new_member = Member(user_ID, password, name, phone_no, address, library, 
                 transaction_log, link_book, membership_plan)
        
        user[user_ID] = [password, 'MEMBER', new_member]
        print('You have successfully registered, please proceed to Login page')


def Login():
    print("******************Login******************")
    user_id = input('User ID: ')
    if (user_id not in user):
        print('Wrong User ID')
        return
    
    password = input('Password: ')
    while (password != user[user_id][0]):
        print('Wrong password!')
        password = input('Password: ')
    
    if(user[user_id][1] == 'ADMIN'):
        Admin_menu(user[user_id][2])
    else:
        Member_menu(user[user_id][2])
        



#*****************************Admin Interface*****************************
def Admin_menu(user_obj):
    print("******************Welcome Back******************")
    f = -1
    while (f != 4): 
        print("1. Library Management")
        print("2. Personal Library Access (Borrowing, Returning, etc)")
        print("3. Account Setting")
        print("4. Exit Admin Menu")

        f = int(input('Please enter the number that indicated the function you want to proceed with '))
        print()

        if f == 1:
            Library_Management(user_obj)
        
        elif f == 2:
            Access(user_obj)
        
        elif f == 3:
            Account(user_obj)

    
    print('GOOD BYE!')


#*****************************Member Interface*****************************
def Member_menu(user_obj):
    print("******************Welcome Back******************")
    f = -1
    while (f != 3): 
        print("1. Library Access")
        print("2. Account Setting")
        print("3. Exit Member Menu")

        f = int(input('Please enter the number that indicated the function you want to proceed with '))
        print()

        if f == 1:
            Access(user_obj)
        
        elif f == 2:
            Account(user_obj)

    print('GOOD BYE!')




def Library_Management(user_obj):
    option = -1
    while (option != 9):
        print('******************Library Management******************')
        print('1. Add Book')
        print('2. Remove Book')
        print('3. Add Copy')
        print('4. Remove Copy')
        print('5. View Member Information')
        print('6. View Books')
        print('7. View Transaction Log')
        print('8. View Book Waitlist')
        print('9. Exit')
        
        option = int(input('Please enter the number that indicated the option you want to proceed with '))
        print()

        if option == 1:
            print('Please enter the following information: ')
            ISBN = input('ISBN = ')
            title = input('Title = ')
            author = input('Author = ')
            publisher = input('Publisher = ')
            edition = input('Edition = ')
            category = input('Category = ')
            copy_id = input('Copy ID = ')
            user_obj.add_book(ISBN, title, author, publisher, edition, category, copy_id)
            
        
        elif option == 2:
            book_ISBN = input('Please enter the book ISBN you wish to delete ')
            user_obj.remove_book(book_ISBN)
            
        
        elif option == 3:
            print('Please enter the following information: ')
            book_ISBN = input('ISBN = ')
            copy_id = input('Copy ID = ')
            user_obj.add_copy(book_ISBN, copy_id)
            
        
        elif option == 4:
            print('Please enter the following information: ')
            book_ISBN = input('Valid Book ISBN = ')
            copy_id = input('Valid Copy ID = ')
            user_obj.remove_copy(book_ISBN, copy_id)
        
        elif option == 5:
            user_ID = input('Please enter member ID: ')
            user_obj.member_info(user_ID)
            print()
        
        elif option == 6:
            user_obj.view_books()
            print()
        
        elif option == 7:
            user_obj.view_transaction_log()
            print()
        
        elif option == 8:
            book_ISBN = input('Please enter book ISBN: ')
            user_obj.view_waitList(book_ISBN)


def Access(user_obj):
    option = -1
    while (option != 10):
        print('******************Library Access******************')
        print('1. View Books')
        print('2. Borrow Book')
        print('3. Return Book')
        print('4. Check Book Due Date')
        print('5. Pay fines')
        print('6. View fines')
        print('7. View Reserved Books')
        print('8. View Borrowed Books')
        print('9. My information')
        print('10. Exit')

        option = int(input('Please enter the number that indicated the option you want to proceed with '))
        print()
        
        if option == 1:
            user_obj.view_books()
            print()

        elif option == 2:
            print('Please enter the following information: ')
            book_name = input('Please enter book name as listed in library ')
            print('Please enter date you intend on returning the book: ')
            day = int(input('Day: '))
            month = int(input("Month: "))
            year = int(input('Year: '))
            returningDate = date(year, month, day)

            while (returningDate < date.today()):
                print('Invalid returning date, please enter a date in the future!')
                day = int(input('Day: '))
                month = int(input("Month: "))
                year = int(input('Year: '))
                returningDate = date(year, month, day)


            trans_ID = random.randint(1, 10000)         # Number changed according to how many transactions are expected to occur
            while (trans_ID in transaction_log):
                trans_ID = random.randint(1, 10000)
                                   
            user_obj.borrow_book(book_name, trans_ID, returningDate, lateFine)
        

        elif option  == 3:
            book_name = input('Please enter book name as listed in library ')
            user_obj.return_book(book_name)
        
        elif option == 4:
            book_name = input('Please enter book name as listed in library ')
            user_obj.check_DueDate(book_name)
        
        elif option == 5:
            user_obj.pay_fine()
        
        elif option == 6:
            user_obj.display_fine()
        
        elif option == 7:
            user_obj.display_reservedBooks()
        
        elif option == 8:
            user_obj.display_borrowedBooks()
        
        elif option == 9:
            user_obj.display_info()


def Account(user_obj):
    option = -1
    while (option != 4):
        print('******************Account Setting******************')
        print("1. Change Password")
        print("2. Change Registered Phone Number")
        print("3. Change Registered Address")
        print("4. Exit")
    
        option = int(input('Please enter the number that indicated the option you want to proceed with '))
        print()

        if option == 1:
            user_obj.change_password()
        
        elif option == 2:
            user_obj.change_phoneNo()
        
        elif option == 3:
            user_obj.change_address()




def initialize():
    more = -1
    while(more != 'n'):
        print('Please fill following book info')
        ISBN = input('ISBN = ')
        title = input('Title = ')
        author = input('Author = ')
        publisher = input('Publisher = ')
        edition = input('Edition = ')
        category = input('Category = ')
        copy_id = input('Copy ID = ')

        if(ISBN in library):
            print('The book is already in the library')
        else:
            new_book = Book(ISBN, title, author, publisher, edition, category)
            new_book.add_copy(copy_id)
            library[ISBN] = new_book
            link_book[title] = ISBN
        
        print(f'{title} has been successfully added to the library')

        more = input('Would you like to enter more books? y/n ')


main()