# File: main.py

import sys
from PyQt5.QtWidgets import QApplication

# Import Controller
from controllers.AccountManager import AccountManager # <-- Import Controller baru

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    # Hanya inisialisasi dan jalankan Controller (AccountManager)
    manager = AccountManager() 
    manager.show() 
    
    sys.exit(app.exec_())