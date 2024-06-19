

def print_board(a,b,c):
    print (a)
    print (b)
    print (c)

def checkhor(d):
    #this function receives a 3x3 matrix list ,checks all the rows in a matrix and return true if any row has 3 identical elements

    for item in d:
        if item==['X','X','X']:
            print ("X wins checkhor!")
            return True
        if item == ['O','O','O']:
            print ("O wins!")
            return True, 'O'
    return False
    

def checkver (e):
    #this function receives a 3x3 matrix list ,checks all the columns in a matrix and return true if any col has 3 identical elements
    if ((e[0][0]==e[1][0]==e[2][0]=='X') or (e[0][1]==e[1][1]==e[2][1]=='X') or (e[0][2]==e[1][2]==e[2][2]=='X')):
        print ("X wins checkver!")
        return True
    if ((e[0][0]==e[1][0]==e[2][0]=='O') or (e[0][1]==e[1][1]==e[2][1]=='O') or (e[0][2]==e[1][2]==e[2][2]=='O')):
        print ("O wins!")
        return True
    return False

def checkdiag (f):
    #this function receives a 3x3 matrix list ,checks both diagonals and return true if any diag has 3 identical elements
    if (f[0][0]==f[1][1]==f[2][2]=='X') or (f[0][2]==f[1][1]==f[2][0]=='X'):
        print ("X wins! checkdiag")
        return True
    if (f[0][0]==f[1][1]==f[2][2]=='O') or (f[0][2]==f[1][1]==f[2][0]=='O'):
        print ("O wins!")
        return True
    return False

def check_tictactoe (g):
    #this function receives a 3x3 matrix list and checks for a tictactoe completion
    if checkhor(g):
        return True
    if checkver(g):
        return True
    if checkdiag(g):
        return True


def startgame ():
    control_list=[['','',''],['','',''],['','','']]

    boardcell00isbusy=False
    boardcell01isbusy=False
    boardcell02isbusy=False
    boardcell10isbusy=False
    boardcell11isbusy=False
    boardcell12isbusy=False
    boardcell20isbusy=False
    boardcell21isbusy=False
    boardcell22isbusy=False

    boardcell00="___|"
    boardcell01="___"
    boardcell02="|___"
    boardcell10="___|"
    boardcell11="___"
    boardcell12="|___"
    boardcell20="   |"
    boardcell21="   "
    boardcell22="|  "
    boardcell00X="_X_|"
    boardcell01X="_X_"
    boardcell02X="|_X_"
    boardcell10X="_X_|"
    boardcell11X="_X_"
    boardcell12X="|_X_"
    boardcell20X=" X |"
    boardcell21X=" X "
    boardcell22X="| X "
    boardcell00O="_O_|"
    boardcell01O="_O_"
    boardcell02O="|_O_"
    boardcell10O="_O_|"
    boardcell11O="_O_"
    boardcell12O="|_O_"
    boardcell20O=" O |"
    boardcell21O=" O "
    boardcell22O="| O "
    board_row1 = boardcell00+boardcell01+boardcell02
    board_row2 = boardcell10+boardcell11+boardcell12
    board_row3 = boardcell20+boardcell21+boardcell22
    isXturn=False
    isOturn=False
    first=True
    gameison=True
    while gameison:
        hor= int (input ("please enter an horizontal coord betwen 0-2:"))
        ver= int (input ("please enter a vertical coord betwen 0-2:"))
        char= input ("please enter an option X or O:")
        if ((char=="X") or (char=='x')) and isOturn:
            print ("Wrong input: It is O turn!")
            continue
        if ((char=="O") or (char=='o')) and isXturn:
            print ("Wrong input: It is X turn!")
            continue
        if not ((char=="X") or (char=='x') or (char=="O") or (char=='o')):
            print ("Invalid input, please enter an X or an O")
            continue
        if first:
            if ((char=="X") or (char=='x')):
                isXturn=True
                first=False
            elif ((char=="O") or (char=='o')):
                isOturn=True
                first=False
        if hor ==0:
            if ver ==0:
                if boardcell00isbusy:
                    print ("cell is busy")
                    continue
                elif ((char=="X") or (char=='x')) and isXturn:
                    board_row1= boardcell00X+board_row1[len(boardcell00X):]
                    control_list[0][0]='X'
                    boardcell00isbusy=True
                    isOturn=True
                    isXturn=False
                elif ((char=="O") or (char=='o')) and isOturn:
                    board_row1= boardcell00O+board_row1[len(boardcell00O):]
                    control_list[0][0]='O'
                    boardcell00isbusy=True
                    isOturn=False
                    isXturn=True
            elif ver==1:
                if boardcell01isbusy:
                    print ("cell is busy")
                    continue
                elif ((char=="X") or (char=='x')) and isXturn:
                    board_row1= board_row1[0:len(boardcell00):]+boardcell01X+board_row1[len(boardcell01)+len(boardcell01X)+1::]
                    control_list[0][1]='X'
                    boardcell01isbusy=True
                    isOturn=True
                    isXturn=False
                elif ((char=="O") or (char=='o')) and isOturn:
                    board_row1= board_row1[0:len(boardcell00):]+boardcell01O+board_row1[len(boardcell01)+len(boardcell01O)+1::]
                    control_list[0][1]='O'
                    boardcell01isbusy=True
                    isOturn=False
                    isXturn=True
            elif ver==2:
                if boardcell02isbusy:
                    print ("cell is busy")
                    continue
                elif ((char=="X") or (char=='x')) and isXturn:
                    board_row1= board_row1[:len(boardcell00)+len (boardcell01)]+boardcell02X
                    control_list[0][2]='X'
                    boardcell02isbusy=True
                    isOturn=True
                    isXturn=False
                elif ((char=="O") or (char=='o')) and isOturn:
                    board_row1= board_row1[:len(boardcell00)+len (boardcell01)]+boardcell02O
                    control_list[0][2]='O' 
                    boardcell02isbusy=True
                    isOturn=False
                    isXturn=True
            else:
                print ("please insert vertical between 0,1,2 ")
        elif hor ==1:
            if ver ==0:
                if boardcell10isbusy:
                    print ("cell is busy")
                    continue
                elif ((char=="X") or (char=='x')) and isXturn:
                    board_row2=boardcell10X+board_row2[len(boardcell10X):]
                    control_list[1][0]='X'
                    boardcell10isbusy=True
                    isOturn=True
                    isXturn=False
                elif ((char=="O") or (char=='o')) and isOturn:
                    board_row2=boardcell10O+board_row2[len(boardcell10O):]
                    control_list[1][0]='O'
                    boardcell10isbusy=True
                    isOturn=False
                    isXturn=True
            elif ver==1:
                if boardcell11isbusy:
                    print ("cell is busy")
                    continue
                if ((char=="X") or (char=='x')) and isXturn:
                    board_row2= board_row2[0:len(boardcell10):]+boardcell11X+board_row2[len(boardcell11)+len(boardcell11X)+1::]
                    control_list[1][1]='X'
                    boardcell11isbusy=True
                    isOturn=True
                    isXturn=False
                elif ((char=="O") or (char=='o')) and isOturn:
                    board_row2= board_row2[0:len(boardcell10):]+boardcell11O+board_row2[len(boardcell11)+len(boardcell11O)+1::]
                    control_list[1][1]='O'
                    boardcell11isbusy=True
                    isOturn=False
                    isXturn=True
            elif ver==2:
                if boardcell12isbusy:
                    print ("cell is busy")
                    continue
                if ((char=="X") or (char=='x')) and isXturn:
                    board_row2= board_row2[:len(boardcell10)+len (boardcell11)]+boardcell12X
                    control_list[1][2]='X'
                    boardcell12isbusy=True
                    isOturn=True
                    isXturn=False
                elif ((char=="O") or (char=='o')) and isOturn:
                    board_row2= board_row2[:len(boardcell10)+len (boardcell11)]+boardcell12O
                    control_list[1][2]='O' 
                    boardcell12isbusy=True
                    isOturn=False
                    isXturn=True
            else:
                print ("please insert vertical between 0,1,2 ")
        elif hor==2:
            if ver ==0:
                if boardcell20isbusy:
                    print ("cell is busy")
                    continue
                if ((char=="X") or (char=='x')) and isXturn:
                    board_row3=boardcell20X+board_row3[len(boardcell20X):]
                    control_list[2][0]='X'
                    boardcell20isbusy=True
                    isOturn=True
                    isXturn=False
                elif ((char=="O") or (char=='o')) and isOturn:
                    board_row3=boardcell20O+board_row3[len(boardcell20O):]
                    control_list[2][0]='O'
                    boardcell20isbusy=True
                    isOturn=False
                    isXturn=True
            elif ver==1:
                if boardcell21isbusy:
                    print ("cell is busy")
                    continue
                if ((char=="X") or (char=='x')) and isXturn:
                    board_row3= board_row3[0:len(boardcell20):]+boardcell21X+board_row3[len(boardcell21)+len(boardcell21X)+1::]
                    control_list[2][1]='X'
                    boardcell21isbusy=True
                    isOturn=True
                    isXturn=False
                elif ((char=="O") or (char=='o')) and isOturn:
                    board_row3= board_row3[0:len(boardcell20):]+boardcell21O+board_row3[len(boardcell21)+len(boardcell21O)+1::]
                    control_list[2][1]='O'
                    boardcell21isbusy=True
                    isOturn=False
                    isXturn=True
            elif ver==2:
                if boardcell22isbusy:
                    print ("cell is busy")
                    continue
                if ((char=="X") or (char=='x')) and isXturn:
                    board_row3= board_row3[:len(boardcell20)+len (boardcell21)]+boardcell22X
                    control_list[2][2]='X'
                    boardcell22isbusy=True
                    isOturn=True
                    isXturn=False
                elif ((char=="O") or (char=='o')) and isOturn:
                    board_row3= board_row3[:len(boardcell20)+len (boardcell21)]+boardcell22O
                    control_list[2][2]='O'
                    boardcell22isbusy=True
                    isOturn=False
                    isXturn=True
            else:
                print ("please insert vertical between 0,1,2 ")
        else:
            print ("please insert horizontal between 0,1,2 ")
        #print (control_list)
        print_board (board_row1,board_row2,board_row3)
        if check_tictactoe (control_list):
            print ("game over")
            gameison==False
            break
        if (boardcell00isbusy==True) and (boardcell01isbusy==True) and (boardcell02isbusy==True) and (boardcell10isbusy==True) and (boardcell11isbusy==True) and (boardcell12isbusy==True) and (boardcell20isbusy==True) and (boardcell21isbusy==True) and (boardcell22isbusy==True):
            print ("Deuce: game over")
            gameison==False
            break
        #keep = input ("keep playing?")   
        #if (keep =='y') or (keep == 'Y'):
        #    gameison=True
        #else:
        #    gameison=False 

#print_board (board_row1,board_row2,board_row3)

#hor=input ("please enter an horizontal coord betwen 0-2:")
#ver=input ("please enter a vertical coord betwen 0-2:")
#char=input ("please enter an option X or O:")
startgame ()

