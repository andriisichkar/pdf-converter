from utils.sys_helpers import fix_sys_streams
from gui import AppGUI

if __name__ == "__main__":
    fix_sys_streams()
    
    app = AppGUI()
    app.run()