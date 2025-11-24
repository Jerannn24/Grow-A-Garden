# File: main.py

import sys
from PyQt5.QtWidgets import QApplication

# Import Controller
from controllers.AccountManager import AccountManager 

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    manager = AccountManager() 
    manager.show() 
    
    sys.exit(app.exec_())