# Need to import Book object
# Import Transaction
# Import Admin and Member
# Import SignUp or Login

books = {}              # {'Book ISBN': book_obj} -> waitlist consists of user IDs inside the object
link_book = {}          # {'Book Name': 'Book ISBN'}, helps find book ISBN if search was done through book's name
user = {}               # {User #ID: ['password', 'admin/member', user_obj]}
transaction_log = {}    # {Transc ID: trans_obj}

# counters to generate userIDs and transc IDS
userID_CNT = 0
transc_CNT = 0

# Add user login/Sign up

# Admin Interface
# Member Interface

# Transactions area created outside the user class to be saved in trasaction log
# set library fine