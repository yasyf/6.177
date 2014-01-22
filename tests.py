### Here Be Test Functions ###
import time, sys, traceback

def test_warmup():
    import runAnt as P
    print '=== Problem 1 ===\n'
    try:
        a1 = P.operate(10, 2)
        print 'Test 1: operate(10, 2) ==> ' + str(a1)
        if a1 == 64:
            print 'PASSED'
        else:
            print 'FAILED'
        a2 = P.operate(2, 3)
        print 'Test 2: operate(2, 3) ==> ' + str(a2)
        if a2 == 5:
            print 'PASSED'
        else:
            print 'FAILED'
    except NotImplementedError:
        print 'No solution provided for Problem 1.'
    except Exception:
        a, b, c = sys.exc_info()
        traceback.print_exception(a, b, c, limit=1, file=sys.stdout)

    print '\n=== Problem 2 ===\n'
    l1 = ['25maroon', 'ComBInE', 'apple', '0315']
    list1 = l1[:]
    try:
        a1 = P.fix_strings(l1)
        print "Test 1: fix_strings(['25maroon', 'ComBInE', 'apple', '0315']) \n==> " + str(a1)
        if a1 == ['31', 'Ppl', 'Ombin', '5Maroo'] and l1 == list1:
            print 'PASSED'
        else:
            print 'FAILED'
        l2 = ['QQQ', '0a0', 'Winner.']
        list2 = l2[:]
        a2 = P.fix_strings(l2)
        print "Test 2: fix_strings(['QQQ', '0a0', 'Winner.']) \n==> " + str(a2)
        if a2 == ['Inner', 'A', 'Q'] and l2 == list2:
            print 'PASSED'
        else:
            print 'FAILED'
    except NotImplementedError:
        print 'No solution provided for Problem 2.'
    except Exception:
        a, b, c = sys.exc_info()
        traceback.print_exception(a, b, c, limit=1, file=sys.stdout)

    print '\n=== Problem 3 ===\n'

    class TestCar(object):
        def __init__(self, name, color):
            self.__name = name
            self.__color = color
            # This dict saves trips in the format (miles, miles_per_gallon).
            self.__trips = {
                "ski trip": (101, 28),
                "groceries": (15, 18),
                "leisure": (3, 9),
                "apple store": (17, 22),
                "airport": (93, 30),
                "canada": (1337, 26),
                "engine check": (0, 0)
            }
            self.__combination = None

        def get_color(self):
            return self.__color

        def change_color(self, color):
            self.__color = color

        def get_name(self):
            return self.__name

        def new_name(self, name):
            self.__name = name

        def get_combination(self):
            return self.__combination

        def combine_trips(self, reduce_function):
            self.__combination = reduce_function(self.__trips)

    testCar = TestCar('Moriarty', 'Sherlock')
    try:
        if not P.modify(testCar) == True:
            print "FAILED: modify() did not return true."
        elif not testCar.get_name() == 'Python':
            print "FAILED: car.get_name() ==> " + testCar.get_name()
        elif not testCar.get_color() == 'Ruby':
            print "FAILED: car.get_color() ==> " + testCar.get_color()
        elif not (testCar.get_combination() > 60.065 and testCar.get_combination() < 60.075):
            print "FAILED: car.get_combination() ==> " + str(testCar.get_combination())
        else:
            print "PASSED"
    except NotImplementedError:
        print 'No solution provided for Problem 3.'
    except Exception:
        a, b, c = sys.exc_info()
        traceback.print_exception(a, b, c, limit=1, file=sys.stdout)


def test_part_two(size=10):
    import runAnt as P
    P.pygame.init()
    window_size = [size * P.WIDTH + 20, size * P.HEIGHT + 20]
    screen = P.pygame.display.set_mode(window_size)
    P.pygame.display.set_caption("Langton's Ant")
    board = P.Board(size)
    moveCount = 0
    clock = P.pygame.time.Clock()
    P.draw_grid(screen,board.size)
    P.pygame.display.flip()
    time.sleep(2)
    P.pygame.quit()

def test_part_three(size=10):
    import runAnt as P
    P.pygame.init()
    window_size = [size * P.WIDTH + 20, size * P.HEIGHT + 20]
    screen = P.pygame.display.set_mode(window_size)
    P.pygame.display.set_caption("Langton's Ant")
    board = P.Board(size)
    moveCount = 0
    clock = P.pygame.time.Clock()
    for sprite in board.squares:
        g = P.pygame.sprite.Group(sprite)
        g.draw(screen)
        P.pygame.display.flip()
        time.sleep(.05)
    P.draw_grid(screen,board.size)
    P.pygame.display.flip()
    time.sleep(1.5)
    P.pygame.quit()
