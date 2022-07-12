from termcolor import colored


class Print_color:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    def yellow(self, text, fin: bool = False) -> None:
        return self.WARNING + text + self.ENDC

    def green(self, text):
        return self.OKGREEN + text + self.ENDC

    def red(self, text):
        return self.FAIL + text + self.ENDC

    def blue(self, text):
        return self.OKBLUE + text + self.ENDC

    def subline(self, text):
        return self.UNDERLINE + text + self.ENDC
