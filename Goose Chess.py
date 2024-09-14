#for Python 3.12.6
import tkinter
import copy
root=tkinter.Tk()
root.title("Goose Chess")
white_pieces="♔♕🩏♖♗♘♙" #King, Queen, Chancellor, Rook, Bishop, Knight, Pawn
black_pieces="♚♛🩒♜♝♞♟" #same as above
goose="\U0001316c"
egg="\U0001f95a"
player="White"
state="accepting starting Square for Piece"
starting_square=None
en_passant_square=None
moves_left_until_draw=100
castling_rights={"White":{"queenside":True,"kingside":True},"Black":{"queenside":True,"kingside":True}}
def rangers_blocked_by(square):
    if squares[square].cget("text") in " "+goose:
        return False
    if square[1]!="8" and squares[square[0]+str(int(square[1])+1)].cget("text")==egg:
        return False
    if square[0]!="h" and squares[chr(ord(square[0])+1)+square[1]].cget("text")==egg:
        return False
    if square[1]!="1" and squares[square[0]+str(int(square[1])-1)].cget("text")==egg:
        return False
    if square[0]!="a" and squares[chr(ord(square[0])-1)+square[1]].cget("text")==egg:
        return False
    return True
def rook_can_range_over(starting_square,ending_square):
    if starting_square[0]!=ending_square[0] and starting_square[1]!=ending_square[1]:
        return False
    if int(ending_square[1])-int(starting_square[1])==1 or ord(ending_square[0])-ord(starting_square[0])==1 or int(starting_square[1])-int(ending_square[1])==1 or ord(starting_square[0])-ord(ending_square[0])==1:
        return True
    if int(ending_square[1])>int(starting_square[1]):
        if rook_can_range_over(starting_square,ending_square[0]+str(int(ending_square[1])-1)) and not rangers_blocked_by(ending_square[0]+str(int(ending_square[1])-1)):
            return True
        return False
    if ord(ending_square[0])>ord(starting_square[0]):
        if rook_can_range_over(starting_square,chr(ord(ending_square[0])-1)+ending_square[1]) and not rangers_blocked_by(chr(ord(ending_square[0])-1)+ending_square[1]):
            return True
        return False
    if int(starting_square[1])>int(ending_square[1]):
        if rook_can_range_over(starting_square,ending_square[0]+str(int(ending_square[1])+1)) and not rangers_blocked_by(ending_square[0]+str(int(ending_square[1])+1)):
            return True
        return False
    if ord(starting_square[0])>ord(ending_square[0]):
        if rook_can_range_over(starting_square,chr(ord(ending_square[0])+1)+ending_square[1]) and not rangers_blocked_by(chr(ord(ending_square[0])+1)+ending_square[1]):
            return True
        return False
    return False
def bishop_can_range_over(starting_square,ending_square):
    if (ord(ending_square[0])-ord(starting_square[0]))**2!=(int(ending_square[1])-int(starting_square[1]))**2:
        return False
    if int(ending_square[1])-int(starting_square[1])==1 or int(starting_square[1])-int(ending_square[1])==1:
        return True
    if ord(ending_square[0])>ord(starting_square[0]) and int(ending_square[1])>int(starting_square[1]):
        if bishop_can_range_over(starting_square,chr(ord(ending_square[0])-1)+str(int(ending_square[1])-1)) and not rangers_blocked_by(chr(ord(ending_square[0])-1)+str(int(ending_square[1])-1)):
            return True
        return False
    if ord(ending_square[0])>ord(starting_square[0]):
        if bishop_can_range_over(starting_square,chr(ord(ending_square[0])-1)+str(int(ending_square[1])+1)) and not rangers_blocked_by(chr(ord(ending_square[0])-1)+str(int(ending_square[1])+1)):
            return True
        return False
    if int(starting_square[1])>int(ending_square[1]):
            if bishop_can_range_over(starting_square,chr(ord(ending_square[0])+1)+str(int(ending_square[1])+1)) and not rangers_blocked_by(chr(ord(ending_square[0])+1)+str(int(ending_square[1])+1)):
                return True
            return False
    if bishop_can_range_over(starting_square,chr(ord(ending_square[0])+1)+str(int(ending_square[1])-1)) and not rangers_blocked_by(chr(ord(ending_square[0])+1)+str(int(ending_square[1])-1)):
        return True
    return False
def move_is_legal(starting_square,ending_square):
    match squares[starting_square].cget("text"):
        case "♘":
            if squares[ending_square].cget("text") in " "+black_pieces and (ord(ending_square[0])-ord(starting_square[0]))**2+(int(ending_square[1])-int(starting_square[1]))**2==5:
                return True
            return False
        case "♞":
            if squares[ending_square].cget("text") in " "+white_pieces and (ord(ending_square[0])-ord(starting_square[0]))**2+(int(ending_square[1])-int(starting_square[1]))**2==5:
                return True
            return False
        case "♙":
            if starting_square[0]==ending_square[0]:
                if int(ending_square[1])-int(starting_square[1])==2:
                    if squares[ending_square].cget("text")==" " and not rangers_blocked_by(ending_square[0]+"3") and starting_square[1]=="2":
                        return True
                if int(ending_square[1])-int(starting_square[1])==1:
                    if squares[ending_square].cget("text")==" ":
                        return True
            if int(ending_square[1])-int(starting_square[1])==1 and (ord(ending_square[0])-ord(starting_square[0])==1 or ord(starting_square[0])-ord(ending_square[0])==1):
                if squares[ending_square].cget("text") in black_pieces or (squares[ending_square].cget("text")==" " and ending_square==en_passant_square):
                    return True
            return False
        case "♟":
            if starting_square[0]==ending_square[0]:
                if int(starting_square[1])-int(ending_square[1])==2:
                    if squares[ending_square].cget("text")==" " and not rangers_blocked_by(ending_square[0]+"6") and starting_square[1]=="7":
                        return True
                if int(starting_square[1])-int(ending_square[1])==1:
                    if squares[ending_square].cget("text")==" ":
                        return True
            if int(starting_square[1])-int(ending_square[1])==1 and (ord(ending_square[0])-ord(starting_square[0])==1 or ord(starting_square[0])-ord(ending_square[0])==1):
                if squares[ending_square].cget("text") in white_pieces or (squares[ending_square].cget("text")==" " and ending_square==en_passant_square):
                    return True
            return False
        case "♖":
            if squares[ending_square].cget("text") in " "+black_pieces and rook_can_range_over(starting_square,ending_square):
                return True
            return False
        case "♜":
            if squares[ending_square].cget("text") in " "+white_pieces and rook_can_range_over(starting_square,ending_square):
                return True
            return False
        case "🩏":
            if squares[ending_square].cget("text") in " "+black_pieces and (rook_can_range_over(starting_square,ending_square) or (ord(ending_square[0])-ord(starting_square[0]))**2+(int(ending_square[1])-int(starting_square[1]))**2==5):
                return True
            return False
        case "🩒":
            if squares[ending_square].cget("text") in " "+white_pieces and (rook_can_range_over(starting_square,ending_square) or (ord(ending_square[0])-ord(starting_square[0]))**2+(int(ending_square[1])-int(starting_square[1]))**2==5):
                return True
            return False
        case "♗":
            if squares[ending_square].cget("text") in " "+black_pieces and bishop_can_range_over(starting_square,ending_square):
                return True
            return False
        case "♝":
            if squares[ending_square].cget("text") in " "+white_pieces and bishop_can_range_over(starting_square,ending_square):
                return True
            return False
        case "♕":
            if squares[ending_square].cget("text") in " "+black_pieces and (rook_can_range_over(starting_square,ending_square) or bishop_can_range_over(starting_square,ending_square)):
                return True
            return False
        case "♛":
            if squares[ending_square].cget("text") in " "+white_pieces and (rook_can_range_over(starting_square,ending_square) or bishop_can_range_over(starting_square,ending_square)):
                return True
            return False
        case "♔":
            if squares[ending_square].cget("text") in " "+black_pieces and (ord(ending_square[0])-ord(starting_square[0]))**2+(int(ending_square[1])-int(starting_square[1]))**2 in {1,2}:
                return True
            if starting_square=="e1" and ending_square=="g1" and squares["f1"].cget("text")==" " and castling_rights["White"]["kingside"]:
                return True
            if starting_square=="e1" and ending_square=="c1" and squares["d1"].cget("text")==" " and castling_rights["White"]["queenside"] and not rangers_blocked_by("b1"):
                return True
            return False
        case "♚":
            if squares[ending_square].cget("text") in " "+white_pieces and (ord(ending_square[0])-ord(starting_square[0]))**2+(int(ending_square[1])-int(starting_square[1]))**2 in {1,2}:
                return True
            if starting_square=="e8" and ending_square=="g8" and squares["f8"].cget("text")==" " and castling_rights["Black"]["kingside"]:
                return True
            if starting_square=="e8" and ending_square=="c8" and squares["d8"].cget("text")==" " and castling_rights["Black"]["queenside"] and not rangers_blocked_by("b8"):
                return True
            return False
def square_clicked(square):
    global player
    global state
    global starting_square
    global goose_ending_square
    global en_passant_square
    global moves_left_until_draw
    if state=="accepting starting Square for Piece":
        if (squares[square].cget("text") in white_pieces and player=="White") or (squares[square].cget("text") in black_pieces and player=="Black"):
            starting_square=square
            state="accepting ending Square for Piece"
            information_label.config(text=f"It is {player}'s turn. Click the same Square to cancel your Move or click another Square to Move to.")
        else:
            information_label.config(text=f"{player}, please click a Square with one of your own Pieces on it.")
    elif state=="accepting ending Square for Piece":
        if square==starting_square:
            state="accepting starting Square for Piece"
            information_label.config(text=f"It is {player}'s turn. Click a square to pick up the Piece on it.")
            starting_square=None
        else:
            if move_is_legal(starting_square,square):
                if squares[square].cget("text") in "♔♚":
                    state="game over"
                if squares[starting_square].cget("text") in "♙♟" and abs(int(square[1])-int(starting_square[1]))==2:
                    if player=="White":
                        next_en_passant_square=square[0]+"3"
                    else:
                        next_en_passant_square=square[0]+"6"
                else:
                    next_en_passant_square=None
                if squares[starting_square].cget("text") in "♙♟" or squares[square].cget("text")!=" ":
                    moves_left_until_draw-=1
                squares[square].config(text=squares[starting_square].cget("text"))
                squares[starting_square].config(text=" ")
                if square==en_passant_square and squares[square].cget("text") in "♙♟":
                    if player=="White":
                        squares[square[0]+"5"].config(text=" ")
                    else:
                        squares[square[0]+"4"].config(text=" ")
                elif squares[square].cget("text") in "♔♚" and abs(ord(square[0])-ord(starting_square[0]))==2:
                    match square:
                        case "c1":
                            squares["d1"].config(text="♖")
                            squares["a1"].config(text=" ")
                        case "g1":
                            squares["f1"].config(text="♖")
                            squares["h1"].config(text=" ")
                        case "c8":
                            squares["d8"].config(text="♜")
                            squares["a8"].config(text=" ")
                        case "g8":
                            squares["f8"].config(text="♜")
                            squares["h8"].config(text=" ")
                en_passant_square=next_en_passant_square
                match starting_square:
                    case "e1":
                        castling_rights["White"]={"queenside":False,"kingside":False}
                    case "e8":
                        castling_rights["Black"]={"queenside":False,"kingside":False}
                    case "a1":
                        castling_rights["White"]["queenside"]=False
                    case "h1":
                        castling_rights["White"]["kingside"]=False
                    case "a8":
                        castling_rights["Black"]["queenside"]=False
                    case "h8":
                        castling_rights["Black"]["kingside"]=False
                match square:
                    case "e1":
                        castling_rights["White"]={"queenside":False,"kingside":False}
                    case "e8":
                        castling_rights["Black"]={"queenside":False,"kingside":False}
                    case "a1":
                        castling_rights["White"]["queenside"]=False
                    case "h1":
                        castling_rights["White"]["kingside"]=False
                    case "a8":
                        castling_rights["Black"]["queenside"]=False
                    case "h8":
                        castling_rights["Black"]["kingside"]=False
                if squares[square].cget("text") in "♙♟" and square[1] in "18":
                    information_label.config(text=f"It is {player}'s turn. Click which Piece you would like to promote to.")
                    queen_promotion_button.config(state="normal")
                    chancellor_promotion_button.config(state="normal")
                    rook_promotion_button.config(state="normal")
                    bishop_promotion_button.config(state="normal")
                    knight_promotion_button.config(state="normal")
                    if state=="game over":
                        state="waiting for Promotion choice to end game"
                    else:
                        state="waiting for Promotion choice"
                    return
                if state=="game over":
                    information_label.config(text=f"{player} wins by capturing their Opponent's King!")
                    compressed_board_state={square:squares[square].cget("text") for square in squares}
                    compressed_board_state["castling_rights"]=copy.deepcopy(castling_rights)
                    compressed_board_state["en_passant_square"]=en_passant_square
                    history.append(copy.deepcopy(compressed_board_state))
                else:
                    state="accepting ending Square for Goose"
                    information_label.config(text=f"It is {player}'s turn. Click an empty square to move the Goose there. The Egg will be moved automatically.")
            else:
                information_label.config(text=f"That move is illegal! {player}, please click a Square you can legally move to!")
    elif state=="accepting ending Square for Goose":
        if squares[square].cget("text")==" ":
            for goose_square in squares:
                if squares[goose_square].cget("text")==goose:
                    squares[goose_square].config(text=" ")
                    break
            squares[square].config(text=goose)
            for egg_square in squares:
                if squares[egg_square].cget("text")==egg:
                    squares[egg_square].config(text=" ")
                    break
            squares[goose_square].config(text=egg)
            move_found=False
            for opponent_piece_square in squares:
                if player=="White":
                    if squares[opponent_piece_square].cget("text") in black_pieces:
                        for square_to_move_to in squares:
                            if move_is_legal(opponent_piece_square,square_to_move_to):
                                move_found=True
                                break
                else:
                    if squares[opponent_piece_square].cget("text") in white_pieces:
                        for square_to_move_to in squares:
                            if move_is_legal(opponent_piece_square,square_to_move_to):
                                move_found=True
                                break
            if move_found==False:
                if player=="White":
                    player="Black"
                    queen_promotion_button.config(text="♛")
                    chancellor_promotion_button.config(text="🩒")
                    rook_promotion_button.config(text="♜")
                    bishop_promotion_button.config(text="♝")
                    knight_promotion_button.config(text="♞")
                else:
                    player="White"
                    queen_promotion_button.config(text="♕")
                    chancellor_promotion_button.config(text="🩏")
                    rook_promotion_button.config(text="♖")
                    bishop_promotion_button.config(text="♗")
                    knight_promotion_button.config(text="♘")
                state="game over"
                information_label.config(text=f"{player} wins by being Fowled!")
                compressed_board_state={square:squares[square].cget("text") for square in squares}
                compressed_board_state["castling_rights"]=copy.deepcopy(castling_rights)
                compressed_board_state["en_passant_square"]=en_passant_square
                history.append(copy.deepcopy(compressed_board_state))
                return
            repetitions=0
            compressed_board_state={square:squares[square].cget("text") for square in squares}
            compressed_board_state["castling_rights"]=copy.deepcopy(castling_rights)
            compressed_board_state["en_passant_square"]=en_passant_square
            for position in history:
                if compressed_board_state==position:
                    repetitions+=1
            history.append(copy.deepcopy(compressed_board_state))
            if moves_left_until_draw==0 or repetitions==3:
                state="game over"
                information_label.config(text="The game is drawn!")
            else:
                state="accepting starting Square for Piece"
                if player=="White":
                    player="Black"
                    queen_promotion_button.config(text="♛")
                    chancellor_promotion_button.config(text="🩒")
                    rook_promotion_button.config(text="♜")
                    bishop_promotion_button.config(text="♝")
                    knight_promotion_button.config(text="♞")
                else:
                    player="White"
                    queen_promotion_button.config(text="♕")
                    chancellor_promotion_button.config(text="🩏")
                    rook_promotion_button.config(text="♖")
                    bishop_promotion_button.config(text="♗")
                    knight_promotion_button.config(text="♘")
                information_label.config(text=f"It is {player}'s turn. Click a square to pick up the Piece on it.")
        else:
            information_label.config(text=f"{player}, you cannot Move the Goose to an occupied Square! Please select an unoccupied Square.")
    elif state=="waiting for Promotion choice to end game" or state=="waiting for Promotion choice":
        information_label.config(text=f"{player}, please click which Piece you would like to promote to.")
squares={}
square_image=tkinter.PhotoImage()
for file_number in range(97,105):
    for rank in range(1,9):
        exec(f"def click():\n    square_clicked(chr({file_number})+str({rank}))")
        if (file_number+rank)%2==0:
            squares[chr(file_number)+str(rank)]=tkinter.Button(root,command=click,bg="green",activebackground="green",image=square_image,width=100,height=100,text=" ",font=("JuliaMono",30),compound="center")
        else:
            squares[chr(file_number)+str(rank)]=tkinter.Button(root,command=click,bg="white",activebackground="white",image=square_image,width=100,height=100,text=" ",font=("JuliaMono",30),compound="center")
        squares[chr(file_number)+str(rank)].grid(row=9-rank,column=file_number)
squares["a1"].config(text="♖")
squares["b1"].config(text="♘")
squares["c1"].config(text="♗")
squares["d1"].config(text="🩏")
squares["e1"].config(text="♔")
squares["f1"].config(text="♗")
squares["g1"].config(text="♘")
squares["h1"].config(text="♖")
squares["a2"].config(text="♙")
squares["b2"].config(text="♙")
squares["c2"].config(text="♙")
squares["d2"].config(text="♙")
squares["e2"].config(text="♙")
squares["f2"].config(text="♙")
squares["g2"].config(text="♙")
squares["h2"].config(text="♙")
squares["d4"].config(text=egg)
squares["e4"].config(text=goose)
squares["a7"].config(text="♟")
squares["b7"].config(text="♟")
squares["c7"].config(text="♟")
squares["d7"].config(text="♟")
squares["e7"].config(text="♟")
squares["f7"].config(text="♟")
squares["g7"].config(text="♟")
squares["h7"].config(text="♟")
squares["a8"].config(text="♜")
squares["b8"].config(text="♞")
squares["c8"].config(text="♝")
squares["d8"].config(text="♛")
squares["e8"].config(text="♚")
squares["f8"].config(text="♝")
squares["g8"].config(text="♞")
squares["h8"].config(text="♜")
information_label=tkinter.Label(root,text="It is White's turn. Click a square to pick up the Piece on it.",fg="red")
information_label.grid(row=9,column=97,columnspan=8)
promotion_label=tkinter.Label(root,text="Promote to:")
promotion_label.grid(row=0,column=98)
def promote_to_queen():
    global state
    if player=="White":
        for file_number in range(97,105):
            if squares[chr(file_number)+"8"].cget("text")=="♙":
                squares[chr(file_number)+"8"].config(text="♕")
                break
    else:
        for file_number in range(97,105):
            if squares[chr(file_number)+"1"].cget("text")=="♟":
                squares[chr(file_number)+"1"].config(text="♛")
                break
    queen_promotion_button.config(state="disabled")
    chancellor_promotion_button.config(state="disabled")
    rook_promotion_button.config(state="disabled")
    bishop_promotion_button.config(state="disabled")
    knight_promotion_button.config(state="disabled")
    if state=="waiting for Promotion choice to end game":
        information_label.config(text=f"{player} wins by capturing their Opponent's King!")
        compressed_board_state={square:squares[square].cget("text") for square in squares}
        compressed_board_state["castling_rights"]=copy.deepcopy(castling_rights)
        compressed_board_state["en_passant_square"]=en_passant_square
        history.append(copy.deepcopy(compressed_board_state))
    else:
        state="accepting ending Square for Goose"
        information_label.config(text=f"It is {player}'s turn. Click an empty square to move the Goose there. The Egg will be moved automatically.")
queen_promotion_button=tkinter.Button(root,command=promote_to_queen,image=square_image,width=50,height=50,text="♕",font=("JuliaMono",30),compound="center",state="disabled")
queen_promotion_button.grid(row=0,column=99)
def promote_to_chancellor():
    global state
    if player=="White":
        for file_number in range(97,105):
            if squares[chr(file_number)+"8"].cget("text")=="♙":
                squares[chr(file_number)+"8"].config(text="🩏")
                break
    else:
        for file_number in range(97,105):
            if squares[chr(file_number)+"1"].cget("text")=="♟":
                squares[chr(file_number)+"1"].config(text="🩒")
                break
    queen_promotion_button.config(state="disabled")
    chancellor_promotion_button.config(state="disabled")
    rook_promotion_button.config(state="disabled")
    bishop_promotion_button.config(state="disabled")
    knight_promotion_button.config(state="disabled")
    if state=="waiting for Promotion choice to end game":
        information_label.config(text=f"{player} wins by capturing their Opponent's King!")
        compressed_board_state={square:squares[square].cget("text") for square in squares}
        compressed_board_state["castling_rights"]=copy.deepcopy(castling_rights)
        compressed_board_state["en_passant_square"]=en_passant_square
        history.append(copy.deepcopy(compressed_board_state))
    else:
        state="accepting ending Square for Goose"
        information_label.config(text=f"It is {player}'s turn. Click an empty square to move the Goose there. The Egg will be moved automatically.")
chancellor_promotion_button=tkinter.Button(root,command=promote_to_chancellor,image=square_image,width=50,height=50,text="🩏",font=("JuliaMono",30),compound="center",state="disabled")
chancellor_promotion_button.grid(row=0,column=100)
def promote_to_rook():
    global state
    if player=="White":
        for file_number in range(97,105):
            if squares[chr(file_number)+"8"].cget("text")=="♙":
                squares[chr(file_number)+"8"].config(text="♖")
                break
    else:
        for file_number in range(97,105):
            if squares[chr(file_number)+"1"].cget("text")=="♟":
                squares[chr(file_number)+"1"].config(text="♜")
                break
    queen_promotion_button.config(state="disabled")
    chancellor_promotion_button.config(state="disabled")
    rook_promotion_button.config(state="disabled")
    bishop_promotion_button.config(state="disabled")
    knight_promotion_button.config(state="disabled")
    if state=="waiting for Promotion choice to end game":
        information_label.config(text=f"{player} wins by capturing their Opponent's King!")
        compressed_board_state={square:squares[square].cget("text") for square in squares}
        compressed_board_state["castling_rights"]=copy.deepcopy(castling_rights)
        compressed_board_state["en_passant_square"]=en_passant_square
        history.append(copy.deepcopy(compressed_board_state))
    else:
        state="accepting ending Square for Goose"
        information_label.config(text=f"It is {player}'s turn. Click an empty square to move the Goose there. The Egg will be moved automatically.")
rook_promotion_button=tkinter.Button(root,command=promote_to_rook,image=square_image,width=50,height=50,text="♖",font=("JuliaMono",30),compound="center",state="disabled")
rook_promotion_button.grid(row=0,column=101)
def promote_to_bishop():
    global state
    if player=="White":
        for file_number in range(97,105):
            if squares[chr(file_number)+"8"].cget("text")=="♙":
                squares[chr(file_number)+"8"].config(text="♗")
                break
    else:
        for file_number in range(97,105):
            if squares[chr(file_number)+"1"].cget("text")=="♟":
                squares[chr(file_number)+"1"].config(text="♝")
                break
    queen_promotion_button.config(state="disabled")
    chancellor_promotion_button.config(state="disabled")
    rook_promotion_button.config(state="disabled")
    bishop_promotion_button.config(state="disabled")
    knight_promotion_button.config(state="disabled")
    if state=="waiting for Promotion choice to end game":
        information_label.config(text=f"{player} wins by capturing their Opponent's King!")
        compressed_board_state={square:squares[square].cget("text") for square in squares}
        compressed_board_state["castling_rights"]=copy.deepcopy(castling_rights)
        compressed_board_state["en_passant_square"]=en_passant_square
        history.append(copy.deepcopy(compressed_board_state))
    else:
        state="accepting ending Square for Goose"
        information_label.config(text=f"It is {player}'s turn. Click an empty square to move the Goose there. The Egg will be moved automatically.")
bishop_promotion_button=tkinter.Button(root,command=promote_to_bishop,image=square_image,width=50,height=50,text="♗",font=("JuliaMono",30),compound="center",state="disabled")
bishop_promotion_button.grid(row=0,column=102)
def promote_to_knight():
    global state
    if player=="White":
        for file_number in range(97,105):
            if squares[chr(file_number)+"8"].cget("text")=="♘":
                squares[chr(file_number)+"8"].config(text="♗")
                break
    else:
        for file_number in range(97,105):
            if squares[chr(file_number)+"1"].cget("text")=="♞":
                squares[chr(file_number)+"1"].config(text="♝")
                break
    queen_promotion_button.config(state="disabled")
    chancellor_promotion_button.config(state="disabled")
    rook_promotion_button.config(state="disabled")
    bishop_promotion_button.config(state="disabled")
    knight_promotion_button.config(state="disabled")
    if state=="waiting for Promotion choice to end game":
        information_label.config(text=f"{player} wins by capturing their Opponent's King!")
        compressed_board_state={square:squares[square].cget("text") for square in squares}
        compressed_board_state["castling_rights"]=copy.deepcopy(castling_rights)
        compressed_board_state["en_passant_square"]=en_passant_square
        history.append(copy.deepcopy(compressed_board_state))
    else:
        state="accepting ending Square for Goose"
        information_label.config(text=f"It is {player}'s turn. Click an empty square to move the Goose there. The Egg will be moved automatically.")
knight_promotion_button=tkinter.Button(root,command=promote_to_knight,image=square_image,width=50,height=50,text="♘",font=("JuliaMono",30),compound="center",state="disabled")
knight_promotion_button.grid(row=0,column=103)
print("Don't close or interrupt this window. The game might crash if you do.")
history=[{square:squares[square].cget("text") for square in squares}]
history[0]["castling_rights"]=copy.deepcopy(castling_rights)
history[0]["en_passant_square"]=en_passant_square
root.mainloop()
