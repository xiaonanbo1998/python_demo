import threading
import random


class WindowThread(threading.Thread):

    def __init__(self,name,lock):
        threading.Thread.__init__(self,name=name)
        self.name = name
        self.tickts = 0
        self.lock = lock

    def run(self):
        global tickt_count

        while tickt_count > 0:

            print('%s notice:There has %d tickts remain ' %(self.name,tickt_count))

            self.lock.acquire()
            if tickt_count > 0:
                if tickt_count > 2:
                    number = random.randint(1,2)
                else:
                    number = 1
                tickt_count -= number
                self.tickts += number

                print('%s have buy %d tickt,the remain tickt\'t count is %d .Already buy %d \n'
                      % (self.name, number, tickt_count, self.tickts))
            self.lock.release()


        print('%s notice:There is no tickt can sold! Already sold %d'%(self.name,self.tickts))


tickt_count = 10

lock = threading.Lock()

window1 = WindowThread('window1',lock)
window2 = WindowThread('window2',lock)
window3 = WindowThread('window3',lock)

window1.start()
window2.start()
window3.start()
window1.join()
window2.join()
window3.join()

print('tickt count ',tickt_count)
