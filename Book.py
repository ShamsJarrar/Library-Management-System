# class that saves book copy details
class Copy:
    def __init__(self, ID):
        self.__copyID = ID              # Book copy indetifier (string)
        self.__status = "Available"     # States whether book is borrowed or available
        self.__transcID = -1            # If the book is borrowed, it connects it to a transaction
                                        # that contains all user details
    


    # Getter Functions
    def get_copyID(self):
        return self.__copyID
    
    def get_status(self):
        return self.__status
    
    def get_transcID(self):
        return self.__transcID
    

    # Update Functions
    # Function to change book status through new_status = Available or Borrowed
    def change_status(self, new_status, transID = -1):        # If Borrowed, transID is given
        self.__status = new_status
        self.__transcID = transID


    # Display Functions
    # Function to display copy information and availability
    def display_info(self):        
        print('Copy ID:', self.__copyID)
        print('\t Status:', self.__status)
    
    # Admin display includes which transaction the copy is a part of if borrowed
    def admin_display(self):       
        print('Copy ID:', self.__copyID)
        print('\t Status:', self.__status)
        if(self.__status == "Borrowed"):
            print('\t Transaction ID:', self.__transcID)










# class that defines a book object to store all necessary book details
class Book:
    def __init__(self, ISBN, title, author, publisher, edition, category):
        self.__ISBN = ISBN              # Book's ISBN (string)
        self.__title = title
        self.__author = author    
        self.__publisher = publisher
        self.__edition = edition        # string that indicates the book edition (1st, 2nd, etc)
        self.__category = category
        self.__copies = {}              # a dictionay that stores all copies of the book through creating a copy object {'Copy ID' : copy_obj}
        self.__waitlist = []            # stores UserIDs that reserved the book                     
    


    # Getter Functions
    def get_copies(self):
        return self.__copies
    
    def get_waitlist(self):
        return self.__waitlist

    def get_name(self):
        return self.__title



    # Update Copy Functions
    # function that takes a string of the new copy's ID and adds it to copies dictionary
    def add_copy(self, copy_id):
        if(copy_id in self.__copies):
            print("Copy is already added to the system")
        self.__copies[copy_id] = Copy(copy_id)
    
    # function that takes a string of the copyID if to be deleted
    def delete_copy(self, copy_id): 
        del self.__copies[copy_id]

    # function that changes copy status if borrowed or returned by taking strings
    def change_copy_status(self, copy_id, new_status, trans_id = -1):
        if (copy_id not in self.__copies):
            print('Wrong copy ID!')
            return
        self.__copies[copy_id].change_status(new_status, trans_id)
    


    # Update waitlist functions
    def add_waitlist(self, userID):
        self.__waitlist.append(userID)
    
    def remove_from_waitlist(self, user_ID):
        self.__waitlist.remove(user_ID)



    # Display functions
    # function that prints all of the book's information
    def display_book_info(self):
        print('ISBN:', self.__ISBN)
        print('Title:', self.__title)
        print('Author:', self.__author)
        print('Publisher:', self.__publisher)
        print('Edition:', self.__edition)
        print('Category:', self.__category)
    
    # function that prints all copies information and status to members
    def display_copies(self):
        for key in self.__copies:
            self.__copies[key].display_info()
    
    # function that prints all copies information with transaction ids for admins
    def admin_display_copies(self):
        for key in self.__copies:
            self.__copies[key].admin_display()
    
    #function to print waitlist for admins
    def display_waitList(self):
        cnt = 1
        for user in self.__waitlist:
            print(cnt, '.', user, 'user')
            cnt += 1
        if len(self.__waitlist) == 0:
            print('Waitlist is empty!')




# Functions test
# books ={}
# books['12345'] = Book('12345', 'Something', 'Shams', 'Penguin', '1st', 'Drama')
# books['12345'].add_copy('1')
# books['12345'].add_copy('2')
# books['12345'].add_copy('3')
# books['12345'].change_copy_status('1', 'Borrowed', 1)
# books['12345'].delete_copy('3')
# books['12345'].display_book_info()
# print('Member display')
# books['12345'].display_copies()
# print('Admin display')
# books['12345'].admin_display_copies()
# books['12345'].add_waitlist(555)
# books['12345'].display_waitList()
# books['12345'].remove_from_waitlist(555)
# books['12345'].display_waitList()