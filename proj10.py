
from cards import Card, Deck

    ###########################################################
    #  CSE 231 project #10
    #
    #  creates deck and deals it in increasing order to begin game
    #  create functions for different possible moves from tableau/waste to foundation
    #    create function to check the win and display board after move
    #    user input string which corresponds to a move 
    #    loop until user inputs quit string
    #       call function based on user input string 
    #       declare if move is valid 
    #       display move
    #       reprompt for next move
    #    stop when user quits or game is won
    ###########################################################

MENU ='''Prompt the user for an option and check that the input has the 
       form requested in the menu, printing an error message, if not.
       Return:
    TT s d: Move card from end of Tableau pile s to end of pile d.
    TF s d: Move card from end of Tableau pile s to Foundation d.
    WT d: Move card from Waste to Tableau pile d.
    WF d: Move card from Waste to Foundation pile d.
    SW : Move card from Stock to Waste.
    R: Restart the game (after shuffling)
    H: Display this menu of choices
    Q: Quit the game        
    '''
def initialize():
    '''function creates deck, shuffles it and deals it into the tableau in increasing order.'''
    stock = Deck()
    stock.shuffle()
    foundation = [[],[],[],[]]
    waste = []
    columns = [[],[],[],[],[],[],[]]
    masterList = []
    # loop through columns 7 times/length of columns
    for x in range(len(columns)):
        # loop through length of columns starting at count of x
        for y in range(x, len(columns)):
            card = stock.deal()
            # check to see if it is the last card in the column if not flip the card
            if y == x:
                pass
            else:
                card.flip_card()
            # append card to index of column 
            columns[y].append(card)
    waste.append(stock.deal())
    return columns, stock, foundation, waste
    
    
def display(tableau, stock, foundation, waste):
    """ display the game setup """
    stock_top_card = "empty"
    found_top_cards = ["empty","empty","empty","empty"]
    waste_top_card = "empty"
    if len(waste):
        waste_top_card = waste[-1] 
    if len(stock):
        stock_top_card = "XX" #stock[-1]
    for i in range(4):
        if len(foundation[i]):
            found_top_cards[i] = foundation[i][-1]
    print()
    print("{:5s} {:5s} \t\t\t\t\t {}".format("stock","waste","foundation"))
    print("\t\t\t\t     ",end = '')
    for i in range(4):
        print(" {:5d} ".format(i+1),end = '')
    print()
    print("{:5s} {:5s} \t\t\t\t".format(str(stock_top_card), str(waste_top_card)), end = "")
    for i in found_top_cards:
        print(" {:5s} ".format(str(i)), end = "")
    print()
    print()
    print()
    print()
    print("\t\t\t\t\t{}".format("tableau"))
    print("\t\t ", end = '')
    for i in range(7):
        print(" {:5d} ".format(i+1),end = '')
    print()
    # calculate length of longest tableau column
    max_length = max([len(stack) for stack in tableau])
    for i in range(max_length):
        print("\t\t    ",end = '')
        for tab_list in tableau:
            # print card if it exists, else print blank
            try:
                print(" {:5s} ".format(str(tab_list[i])), end = '')
            except IndexError:
                print(" {:5s} ".format(''), end = '')
        print()
    print()
    

def stock_to_waste( stock, waste ):
    ''' deal stock to waste. If possible, return True if not return false'''
    # check if stock is not empty, if so deal stock to waste. 
    if stock.is_empty() == False:
        waste.append(stock.deal())
        return True
    else:
        return False
    
       
def waste_to_tableau( waste, tableau, t_num ):
    '''Deals waste to tableau taking into account the rules of the game and user input. uses Returns true if possible, false if not. '''
    # checks if waste is empty. if so return false
    if waste != []:
        # declare card, rank, and color
        waste_card = waste[-1]
        waste_card_rank = waste_card.rank()
        waste_color = waste_card.suit()
    else:
        return False
    # check if column is empty and if card rank is 13 if so, move card to user column
    if tableau[t_num] == [] and waste_card_rank == 13:
        tableau[t_num].append(waste_card)
        waste.pop()
        return True
    # checks if column is not empty
    if tableau[t_num] != []:
        # declare card, rank, and color
        column_card = tableau[t_num][-1]
        column_card_R = column_card.rank()
        column_card_color = column_card.suit()
        # checks if card rank is valid
        if waste_card_rank == (column_card_R -1):
            # checks if card color are not the same if so append card to column
            if (waste_color == 2 or waste_color ==3)and (column_card_color == 1 or column_card_color == 4):
                tableau[t_num].append(waste_card)
                waste.pop()
                return True
            # checks if card color are not the same if so append card to column
            elif(waste_color == 1 or waste_color ==4)and (column_card_color == 2 or column_card_color == 3):
                tableau[t_num].append(waste_card)
                waste.pop()
                return True
            else:
                return False

    return False

def waste_to_foundation( waste, foundation, f_num ):
    '''moves card from waste to foundation using user inputs and based on the games rules.'''
    # check if waste is empty. if true return false
    if waste != []:
        # declare card, rank, and suit
        waste_card = waste[-1]
        waste_card_rank = waste_card.rank()
        waste_suit = waste_card.suit()
    else:
        return False 
    # check if foundation is empty and waste card is ace. if so append to user foundation
    if foundation[f_num] == []:
        if waste_card_rank == 1:
            foundation[f_num].append(waste_card)
            waste.pop()
            return True
    else:
        # declare foundation card and its rank and suit
        foundation_card = foundation[f_num][-1]
        foundation_card_S = foundation_card.suit()
        foundation_card_R = foundation_card.rank()
        # check if waste card is one greater than foundation and if they are the same suit. if so append card to column
        if (foundation_card_R + 1) == waste_card_rank:
            if foundation_card_S == waste_suit:
                foundation[f_num].append(waste_card)
                waste.pop()
                return True
    return False

def tableau_to_foundation( tableau, foundation, t_num, f_num ):
    '''moves card from tableau to foundation using user inputs and based on the games rules.'''
    # declare card, rank, and suit
    tableau_card = tableau[t_num][-1]
    tableau_rank = tableau_card.rank()
    tableau_suit = tableau_card.suit()
    # try except to catch index error if user inputs out of range
    try:
        # check if foundation is empty and waste card is ace. if so append to user foundation
        if foundation[f_num] == []:
            if tableau_rank == 1:
                foundation[f_num].append(tableau_card)
                tableau[t_num].pop()
                # flips card if column exists and is not face up already
                if tableau[t_num] and not tableau[t_num][-1].is_face_up():
                    tableau[t_num][-1].flip_card()
                return True
            else:
                return False
        else:
            # declare foundation card and its rank and suit
            foundation_card = foundation[f_num][-1]
            foundation_card_S = foundation_card.suit()
            foundation_card_R = foundation_card.rank()
            #  check if tableau card is one greater than foundation and if they are the same suit. if so append card to column
            if (foundation_card_R + 1) == tableau_rank:
                if tableau_suit == foundation_card_S:
                    foundation[f_num].append(tableau_card)
                    tableau[t_num].pop()
                    # flips card if column exists and is not face up already
                    if tableau[t_num] and not tableau[t_num][-1].is_face_up():
                        tableau[t_num][-1].flip_card()
                    return True
    except IndexError:
        return False
    return False


def tableau_to_tableau( tableau, t_num1, t_num2 ):
    '''moves card from tableau to tableau using user inputs and based on the games rules.'''
    # checks if user column is empty
    if tableau[t_num1]!= []:
        # card 1 is the card chosen to move card 2 is the column destination of card 1
        # declare tableau card, rank, and suit
        tableau_card = tableau[t_num1][-1]
        tableau_rank = tableau_card.rank()
        tableau_color = tableau_card.suit()
        # check if uesr destination is empty if so check if king. If true append card to column
        if tableau[t_num2]==[]:
            if tableau_rank==13:
                tableau[t_num2].append(tableau_card)
                tableau[t_num1].pop()
                # flips card if column exists and is not face up already
                if tableau[t_num1] and not tableau[t_num1][-1].is_face_up():
                    tableau[t_num1][-1].flip_card()
                return True
            else:
                return False
        # declares column card, rank, and suit
        column_card = tableau[t_num2][-1]
        column_card_R = column_card.rank()
        column_card_color = column_card.suit()
        # checks if tableau card rank is less than destination
        if tableau_rank == (column_card_R -1):
            # checks if card color are not the same if so append card to column
            if (tableau_color == 2 or tableau_color ==3)and (column_card_color == 1 or column_card_color == 4):
                tableau[t_num2].append(tableau_card)
                tableau[t_num1].pop()
                if tableau[t_num1] and not tableau[t_num1][-1].is_face_up():
                    tableau[t_num1][-1].flip_card()
                return True
            elif(tableau_color == 1 or tableau_color ==4)and (column_card_color == 2 or column_card_color == 3):
                tableau[t_num2].append(tableau_card)
                tableau[t_num1].pop()
                # checks if card color are not the same if so append card to column
                if tableau[t_num1] and not tableau[t_num1][-1].is_face_up():
                    tableau[t_num1][-1].flip_card()
                return True
            else:
                return False
    
    return False
    
def check_win (stock, waste, foundation, tableau):
    '''cheks if user has won based on current state of game and rules'''
    # checks if stock is not empty
    if len(stock) != 0:
        return False
    # checks if waste is not empty
    if len(waste) != 0:
        return False
    # loops through tableau and checks if all colums are empty
    for lst in tableau:
        if len(lst) != 0:
            return False
    return True

def parse_option(in_str):
    '''Prompt the user for an option and check that the input has the 
           form requested in the menu, printing an error message, if not.
           Return:
        TT s d: Move card from end of Tableau pile s to end of pile d.
        TF s d: Move card from end of Tableau pile s to Foundation d.
        WT d: Move card from Waste to Tableau pile d.
        WF d: Move card from Waste to Foundation pile d.
        SW : Move card from Stock to Waste.
        R: Restart the game (after shuffling)
        H: Display this menu of choices
        Q: Quit the game        
        '''
    option_list = in_str.strip().split()
    
    opt_char = option_list[0][0].upper()
    
    if opt_char in 'RHQ' and len(option_list) == 1:  # correct format
        return [opt_char]
    
    if opt_char == 'S' and len(option_list) == 1:
        if option_list[0].upper() == 'SW':
            return ['SW']
    
    if opt_char == 'W' and len(option_list) == 2:
        if option_list[0].upper() == 'WT' or option_list[0].upper() == 'WF':
            dest = option_list[1] 
            if dest.isdigit():
                dest = int(dest)
                if option_list[0].upper() == 'WT' and (dest < 1 or dest > 7):
                    print("\nError in Destination")
                    return None
                if option_list[0].upper() == 'WF' and (dest < 1 or dest > 4):
                    print("\nError in Destination")
                    return None
                opt_str = option_list[0].strip().upper()
                return [opt_str,dest]
                               
    if opt_char == 'T' and len(option_list) == 3 and option_list[1].isdigit() \
        and option_list[2].isdigit():
        opt_str = option_list[0].strip().upper()
        if opt_str in ['TT','TF']:
            source = int(option_list[1])
            dest = int(option_list[2])
            # check for valid source values
            if opt_str in ['TT','TF'] and (source < 1 or source > 7):
                print("\nError in Source.")
                return None
            #elif opt_str == 'MFT' and (source < 0 or source > 3):
                #print("Error in Source.")
                #return None
            # source values are valid
            # check for valid destination values
            if (opt_str =='TT' and (dest < 1 or dest > 7)) \
                or (opt_str == 'TF' and (dest < 1 or dest > 4)):
                print("\nError in Destination")
                return None
            return [opt_str,source,dest]

    print("\nError in option:", in_str)
    return None   # none of the above


def main():   
    # initialilze game print meny and display game
    tableau, stock, foundation, waste = initialize()
    print(MENU)
    display(tableau, stock, foundation, waste)
    # prompt for user input and loop until user input is q
    user_option = input("\nInput an option (TT,TF,WT,WF,SW,R,H,Q): ")
    while user_option.lower() != 'q':
        option = parse_option(user_option)
        # checks if return is none if so reprompt
        if option == None:
            pass
        elif option[0] == 'TF':
            # call move and check if move is possible, if not print error statement reprompt
            move = tableau_to_foundation(tableau, foundation, option[1]-1,option[2]-1 )
            if  move == False:
                print("\nInvalid move!\n")
                # check if win conditions are met. print message and display board
            if check_win(stock, waste, foundation, tableau) == True:
                print('You won!')
                display(tableau, stock, foundation, waste)
                break
        elif option[0] == 'TT':
            # call move and check if move is possible, if not print error statement reprompt
            if  tableau_to_tableau(tableau,option[1]-1,option[2]-1) == False:
                print("\nInvalid move!\n")
            move = tableau_to_tableau(tableau,option[1]-1,option[2]-1)
            
        elif option[0] == 'WT':
            # call move and check if move is possible, if not print error statement reprompt
            if waste_to_tableau(waste, tableau, option[1]-1) == False:
                print("\nInvalid move!\n")
            move = waste_to_tableau(waste, tableau, option[1]-1)

        elif option[0] == 'WF':
            # call move and check if move is possible, if not print error statement reprompt
            if waste_to_foundation(waste, foundation, option[1]-1) == False:
                print("\nInvalid move!\n")
            else:
                waste_to_foundation(waste, foundation, option[1]-1)
            # check if win conditions are met. print message and display board
            if check_win(stock, waste, foundation, tableau) == True:
                print('You won!')
                display(tableau, stock, foundation, waste)
                break

        elif option[0] == 'SW':
            # call move and check if move is possible, if not print error statement reprompt
            move = stock_to_waste(stock, waste)
            if move == False:
                print("\nInvalid move!\n")
        # option restarts the game
        elif option == 'R':
            tableau, stock, foundation, waste = initialize()
            print(MENU)
            display(tableau, stock, foundation, waste)

        elif option == 'Q':
            break

        elif option == 'H':
            print('''Prompt the user for an option and check that the input has the 
           form requested in the menu, printing an error message, if not.
           Return:
        TT s d: Move card from end of Tableau pile s to end of pile d.
        TF s d: Move card from end of Tableau pile s to Foundation d.
        WT d: Move card from Waste to Tableau pile d.
        WF d: Move card from Waste to Foundation pile d.
        SW : Move card from Stock to Waste.
        R: Restart the game (after shuffling)
        H: Display this menu of choices
        Q: Quit the game        
        ''')


        display(tableau, stock, foundation, waste)
        user_option = input("\nInput an option (TT,TF,WT,WF,SW,R,H,Q): ")
if __name__ == '__main__':
     main()
