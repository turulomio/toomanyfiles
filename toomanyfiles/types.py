
class ExitCodes:
    Success=0
    MixedRoots=1
    MixedFilesDirectories=2
    NotDeveloped=3
    ArgumentError=4
    
    ##Younger files parameter bigger than max number of files
    YoungGTMax=5
    
    ConfigFileNotFound=6

class RemoveMode:
    RemainFirstInMonth=1
    RemainLastInMonth=2

    @staticmethod
    def from_string(s):
        if s=="RemainFirstInMonth":
            return RemoveMode.RemainFirstInMonth
        elif s=="RemainLastInMonth":
            return RemoveMode.RemainLastInMonth

class FileStatus:
    TooYoungToDelete=1
    OverMaxFiles=2
    Remain=3
    Delete=4

