

def show(banco, nxn):
    #pygame.event.pump()
    print("Now:")
    for i in range(1, nxn+1):
        print(i%10, end = " ")
    print()
    for i in range(nxn):
        for j in range(nxn):
            print(banco[i][j], end = " ")
        print((i+1)%10)
    print(flush=True)

def checkWin(banco, player:str, x:int, y:int, nxn, NumberToWin):
    #show(banco, nxn)
    # dựa vào bước vừa đi để tính toán
    # check hàng ngang
    demNgangM = 0; demDocM = 0
    demNgang = 0; ngang = False; demDoc = 0; doc = False
    for i in range(nxn):
        if banco[x-1][i] == player:
            if ngang:
                demNgang += 1
            else:
                ngang = True; demNgang = 1
        else:
            ngang = False;
            if demNgang > demNgangM:
                demNgangM = demNgang
        if banco[i][y-1] == player:
            if doc:
                demDoc += 1
            else:
                doc = True; demDoc = 1
        else:
            doc = False;
            if demDoc > demDocM:
                demDocM = demDoc
    if demNgang > demNgangM:
        demNgangM = demNgang
    if demDoc > demDocM:
        demDocM = demDoc 
    if demNgangM >= NumberToWin or demDocM >= NumberToWin:
        print("Win Ngang/Doc")
        return "Win"

    # check chéo chính
    dem = 0; demM = 0; cheo = False;
    if x == y: 
        for i in range(nxn):
            # check cheo chinh
            if banco[i][i] == player:   
                if cheo:
                    dem += 1
                else:
                    cheo = True; dem = 1
            else:
                cheo = False;
                if dem > demM:
                    demM = dem 
        if dem > demM:
            demM = dem  
    elif y > x:
        # tính cột start (j)
        hieu = y-x; start = 1 + hieu; i = 0
        for j in range(start, nxn+1):
            i += 1;
            if banco[i-1][j-1] == player:
                if cheo:
                    dem += 1
                else:
                    cheo = True; dem = 1
            else:
                cheo = False;
                if dem > demM:
                    demM = dem
        if dem > demM:
            demM = dem
    elif x > y:
        # tính hàng start (i)
        hieu = x - y; start = 1 + hieu; j = 0
        for i in range(start, nxn+1):
            j += 1;
            if banco[i-1][j-1] == player:
                if cheo:
                    dem += 1
                else:
                    cheo = True; dem = 1
            else:
                cheo = False;
                if dem > demM:
                    demM = dem
        if dem > demM:
            demM = dem

    if demM >= NumberToWin:
        print("Win Cheo")
        return "Win"
    
    # check chéo phụ
    dem2 = 0; dem2M = 0; cheo2 = False;
    if x + y == nxn + 1:
        # thuoc cheo phu
        for i in range(nxn):
            j = nxn - 1 - i
            if banco[i][j] == player:   
                if cheo2:
                    dem2 += 1
                else:
                    cheo2 = True; dem2 = 1
            else:
                cheo2 = False;
                if dem2 > dem2M:
                    dem2M = dem2 
        if dem2 > dem2M:
            dem2M = dem2
    elif x + y > nxn + 1:
        hieu = x + y - nxn - 1; start = hieu
        j = nxn 
        for i in range(start, nxn):
            j -= 1
            if banco[i][j] == player:   
                if cheo2:
                    dem2 += 1
                else:
                    cheo2 = True; dem2 = 1
            else:
                cheo2 = False;
                if dem2 > dem2M:
                    dem2M = dem2 
        if dem2 > dem2M:
            dem2M = dem2
    elif x + y < nxn + 1:
        start = x + y - 1 - 1
        j = -1
        for i in range(start, -1, -1):
            j += 1
            #print(135, i, j)
            if banco[i][j] == player:   
                if cheo2:
                    dem2 += 1
                else:
                    cheo2 = True; dem2 = 1
            else:
                cheo2 = False;
                if dem2 > dem2M:
                    dem2M = dem2 
        if dem2 > dem2M:
            dem2M = dem2

    if dem2M >= NumberToWin:
        print("Win cheo phu")
        return "Win"
