import os
os.chdir("E:/ThisPC/Desktop/Code/Caro/SinhH")
with open("H.txt", "w", encoding="utf-8") as out:
    with open("G2.txt", encoding="utf-8") as inp:
        for i in range(361):
            xau = list(inp.readline().split(" "))
            print(xau, len(xau))
            e = "".join(xau)[:-1] 
            index = xau.index("X")
            l = index - 1
            r = index + 1
            X = 0; white = 0
            while l >= 0:
                if xau[l] == "1":
                    X += 1
                    l -= 1
                else:
                    if xau[l] == "0":
                        white += 1
                    break
            while r < len(xau):
                if xau[r] == "1":
                    X += 1
                    r += 1
                else:
                    if xau[r] == "0" or r == len(xau)-1:
                        white += 1
                    break
            # A: đánh là thắng ngay
            # B: lượt tiếp theo sẽ thắng VÌ tạo ra hơn 2 nước thắng -> đối thủ sẽ không chặn được (trừ khi đối thắng luôn)
            # C: yêu cầu đối thủ chặn Nếu không tạo thành B -> đối thủ bắt buộc phải chặn được ở nước tới
            # => 2C = 1B 
            # D: có cơ hội tạo thành C
            # E: có cơ hội tạo thành D
            # F: Vô dụng
            if X >= 4:      # 1111X 111X1 11X11 1X111 X1111
                e += ";A;\n"
            elif X == 3:    # 111X
                if white == 2:      # 0111X0
                    e += ";B;x3w2\n"
                elif white == 1:    # -1111X0
                    e += ";C;x3w1\n"
                elif white == 0:    # -1111X-1
                    e += ";F;x3w0\n" 
            elif X == 2:    # 11X 
                if white == 2:  # 011X0      
                    X2L = 0; white2L = 0; 
                    l -= 1
                    while l >= 0:
                        if xau[l] == "1":
                            X2L += 1;
                            l -= 1
                        else:
                            if xau[l] == "0":
                                white2L += 1
                            break
                    X2R = 0; white2R = 0; 
                    r += 1
                    while r >= 0:
                        if xau[r] == "1":
                            X2R += 1;
                            r += 1
                        else:
                            if xau[r] == "0" or r == len(xau)-1:
                                white2R += 1
                            break
                    if X2L >= 1:
                        if X2R >= 1:
                            e += ";A;x2w2x2l1x2r1\n"
                        elif X2R == 0: #   -11011X0-1
                            e += ";C;x2w2x2l1x2r0\n"
                    elif X2L == 0:
                        if X2R >= 1:  #   -1011X01-1
                            e += ";C;x2w2x2l0x2r1\n"
                        elif X2R == 0: # -1011X0-1
                            e += ";F;x2w2x2l0x2r0\n"
                elif white == 1:    # -111X0
                    l = index - 1
                    r = index + 1
                    while l >= 0:
                        if xau[l] == "0":
                            index2 = l
                            break
                        l -= 1
                    while r < len(xau):
                        if xau[r] == "0" or r == len(xau)-1:
                            index2 = r
                            break
                        r += 1
                    X2 = 0; white2 = 0
                    if index2 == l:
                        l -= 1
                        while l >= 0:
                            if xau[l] == "1":
                                X2 += 1
                                l -= 1
                            else:
                                if xau[l] == "0":
                                    white2 += 1
                                break
                    else:
                        r += 1
                        while r < len(xau):
                            if xau[r] == "1":
                                X2 += 1
                                r += 1
                            else:
                                if xau[r] == "0" or r == len(xau)-1:
                                    white2 += 1
                                break

                    if X2 == 0: # -111X0-1
                        if white2 == 0:
                            e += ";F;x2w1x20w20\n" 
                        else:
                            e += ";D;x2w1x20w21\n" 
                    elif X2 >= 1:  # -111X010   -111X01-1
                        e += ";C;x2w1x21\n" 

                elif white == 0:    # -111X-1
                    e += ";F;x2w0\n"

            elif X == 1:    # 1X 
                if white == 2:      # 01X0
                    X2L = 0; white2L = 0; 
                    l -= 1
                    while l >= 0:
                        if xau[l] == "1":
                            X2L += 1;
                            l -= 1
                        else:
                            if xau[l] == "0":
                                white2L += 1
                            break
                    X2R = 0; white2R = 0; 
                    r += 1
                    while r >= 0:
                        if xau[r] == "1":
                            X2R += 1;
                            r += 1
                        else:
                            if xau[r] == "0" or r == len(xau)-1:
                                white2R += 1
                            break
                    if X2L == 1:   
                        if X2R == 1: # -1101X01-1
                            e += ";D;x1w2x2l1x2r1\n"
                        elif X2R == 0: # -1101X0-1
                            e += ";D;x1w2x2l1x2r0\n"
                        elif X2R >= 2: # -1101X011-1
                            e += ";C;x1w2x2l1x2r2\n"
                    elif X2L == 0:
                        if X2R == 1: # -101X01-1
                            e += ";D;x1w2x2l0x2r1\n"
                        elif X2R == 0: # -101X0-1
                            e += ";F;x1w2x2l0x2r0\n"
                        elif X2R >= 2: # -101X011-1
                            e += ";C;x1w2x2l0x2r2\n"
                    elif X2L >= 2:
                        if X2R == 1: # -11101X01-1
                            e += ";C;x1w2x2l2x2r1\n"
                        elif X2R == 0: # -11101X0-1
                            e += ";C;x1w2x2l2x2r0\n"
                        elif X2R >= 2: # -11101X011-1
                            e += ";B;x1w2x2l2x2r2\n"
                elif white == 1:    # -11X0 
                    l = index - 1
                    r = index + 1
                    while l >= 0:
                        if xau[l] == "0":
                            index2 = l
                            break
                        l -= 1
                    while r < len(xau):
                        if xau[r] == "0" or r == len(xau)-1:
                            index2 = r
                            break
                        r += 1
                    X2 = 0; white2 = 0
                    if index2 == l:
                        l -= 1
                        while l >= 0:
                            if xau[l] == "1":
                                X2 += 1
                                l -= 1
                            else:
                                if xau[l] == "0":
                                    white2 += 1
                                break
                    else:
                        r += 1
                        while r < len(xau):
                            if xau[r] == "1":
                                X2 += 1
                                r += 1
                            else:
                                if xau[r] == "0" or r == len(xau)-1:
                                    white2 += 1
                                break

                    if X2 == 0: # -11X0-1
                        if white2 == 0:
                            e += ";F;x1w1x20w20\n" 
                        elif white2 == 1:
                            e += ";E;x1w1x20w21\n" 
                    elif X2 == 1:     
                        if white2 == 1: # -11X010
                            e += ";D;x1w1x21w21\n" 
                        elif white2 == 0: #-11X01-1
                            e += ";F;x1w1x21w20\n" 
                    elif X2 >= 2: # -11X0110   -11X011-1
                        e += ";C;x1w1x22\n" 

                elif white == 0:    # -11X-1
                    e += ";F;x1w0\n"
            elif X == 0:    # X
                if white == 2: # 0X0 
                    X2L = 0; white2L = 0; 
                    l -= 1
                    while l >= 0:
                        if xau[l] == "1":
                            X2L += 1;
                            l -= 1
                        else:
                            if xau[l] == "0":
                                white2L += 1
                            break
                    X2R = 0; white2R = 0; 
                    r += 1
                    while r >= 0:
                        if xau[r] == "1":
                            X2R += 1;
                            r += 1
                        else:
                            if xau[r] == "0" or r == len(xau)-1:
                                white2R += 1
                            break
                    if X2L == 1:   
                        if X2R == 1:    # -110X01-1
                            e += ";D;x0w2x2l1x2r1\n"
                        elif X2R == 0:  # -110X00
                            e += ";F;x0w2x2l1x2r0\n"
                        elif X2R == 2:  # -110X011-1
                            e += ";D;x0w2x2l1x2r2\n"
                        elif X2R >= 3:  # -110X0111-1
                            e += ";C;x0w2x2l1x2r3\n"
                    elif X2L == 0:
                        if X2R == 1:    # -10X01-1
                            e += ";F;x0w2x2l0x2r1\n"
                        elif X2R == 0:  # -10X00
                            e += ";F;x0w2x2l0x2r0\n"
                        elif X2R == 2:  # -10X0110
                            e += ";D;x0w2x2l0x2r2\n"
                        elif X2R >= 3:  # -110X0111-1
                            e += ";C;x0w2x2l0x2r3\n"
                    elif X2L == 2:
                        if X2R == 1:    # -1110X01-1
                            e += ";D;x0w2x2l2x2r1\n"
                        elif X2R == 0:  # -1110X0-1
                            e += ";D;x0w2x2l2x2r0\n"
                        elif X2R == 2:  # -1110X011-1
                            e += ";D;x0w2x2l2x2r2\n"
                        elif X2R >= 3:  # -1110X0111-1
                            e += ";C;x0w2x2l1x2r3\n"
                    elif X2L >= 3:      # -11110X0
                            e += ";C;x0w2x2l2x2r3\n"
                elif white == 1: # -1X0
                    l = index - 1
                    r = index + 1
                    while l >= 0:
                        if xau[l] == "0":
                            index2 = l
                            break
                        l -= 1
                    while r < len(xau):
                        if xau[r] == "0" or r == len(xau)-1:
                            index2 = r
                            break
                        r += 1
                    X2 = 0; white2 = 0
                    if index2 == l:
                        l -= 1
                        while l >= 0:
                            if xau[l] == "1":
                                X2 += 1
                                l -= 1
                            else:
                                if xau[l] == "0":
                                    white2 += 1
                                break
                    else:
                        r += 1
                        while r < len(xau):
                            if xau[r] == "1":
                                X2 += 1
                                r += 1
                            else:
                                if xau[r] == "0" or r == len(xau)-1:
                                    white2 += 1
                                break

                    if X2 == 0: # -1X0-1
                        e += ";F;x0w1x20\n" 
                    elif X2 == 1:     
                        if white2 == 1: # -1X010
                            e += ";E;x0w1x21w21\n" 
                        elif white2 == 0: #-1X01-1
                            e += ";F;x0w1x21w20\n" 
                    elif X2 == 2: 
                        if white2 == 1: # -1X0110
                            e += ";D;x0w1x22w21\n" 
                        elif white2 == 0: #-1X011-1
                            e += ";F;x0w1x22w20\n" 
                    elif X2 >= 3: 
                        if white2 == 1: # -1X01110
                            e += ";C;x0w1x23w21\n" 
                        elif white2 == 0: #-1X0111-1
                            e += ";C;x0w1x23w20\n" 

                elif white == 0: # -1X-1 -1X-1
                    e += ";F;x0w0\n" 
            if ";" not in e:
                e += "; Chua xet;\n"
            out.write(e)


