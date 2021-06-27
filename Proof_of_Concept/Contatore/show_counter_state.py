import gdb

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    WHITE = '\033[37m'
    YELLOW ='\033[33m'
    RED = '\033[31m'

class CounterCheck(gdb.Command):
    def __init__(self):
        # This registers our class as "CounterCheck"
        super(CounterCheck, self).__init__("CounterCheck", gdb.COMMAND_USER)

    def _Print(self,arg0,N):
        Timestamp = arg0["Timestamp"]
        Timestamp = Timestamp[N]
        frequency = 2**N
        print(bcolors.OKGREEN + "### PRINTING THE STATUS OF COUNTER WITH COUNTING FREQUENCY " + str(frequency) + " Hz ###" + bcolors.WHITE)
        executionTime = Timestamp/frequency
        if frequency == 1:
            s = int(arg0["s"][N])
            m = int(arg0["m"][N])
            h = int(arg0["h"][N])
            print(bcolors.OKCYAN + "\tWorking frequency of the current counter: " + str(frequency) + " Hz " + bcolors.WHITE + "\n\tExecution time of the current counter: " + str(executionTime) +
                " s"+ bcolors.YELLOW +"\n\tRecorded time(H:m:s): " +str(h)+":"+str(m)+":"+str(s) + bcolors.WHITE + "\n\tCounter ticks: " + str(Timestamp))
        else:
            print(bcolors.OKCYAN + "\tWorking frequency of the current counter: " + str(frequency) + " Hz " + bcolors.WHITE + "\n\tExecution time of the current counter: " + str(executionTime) + "s\n\tCounter ticks: " + str(Timestamp))
        print(bcolors.ENDC)
    def _CounterCheck(self, arg0, arg1):
        if arg1 == None:
            N = arg0["N"]
            self._Print(arg0,N)
        elif arg1 == "all":
            for x in range(0,11):
                self._Print(arg0,x)
        else:
            N = int(arg1)
            self._Print(arg0,N)

    def invoke(self, args, from_tty):
        argv = gdb.string_to_argv(args)
        if len(argv)==1:
            #print("First parameter: " + argv[0])
            arg0 = gdb.parse_and_eval(argv[0])
            self._CounterCheck(arg0, None)
        elif len(argv)==2:
            #print("First parameter: " + argv[0])
            #print("Second parameter: " + argv[1])
            arg0 = gdb.parse_and_eval(argv[0])
            arg1 = argv[1]
            self._CounterCheck(arg0, arg1)
        else:
            print("No parameter given")
            return
    def complete(self, text, word):
        return gdb.COMPLETE_SYMBOL

# This registers our class to the gdb runtime at "source" time.
CounterCheck()
