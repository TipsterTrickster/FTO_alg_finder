import subprocess


class AlgGen():
    def __init__(self):
        pass

    def EIF2CIF(self, case):
        CIF = ["U", "D", "F", "B", "R", "BL", "L", "BR"]
        EIF = ["U", "D", "R", "BL", "BR", "L", "F", "B"]
        
        new_case = ""
        case.strip()
        
        for move in case.split(" "):
            suffix = ""
            if "'" in move:
                move = move.removesuffix("'")
                suffix = "'"
            new_case += " " + CIF[EIF.index(move)] + suffix
        return new_case.strip()


    def CIF2EIF(self, case):
        CIF = ["U", "D", "F", "B", "R", "BL", "L", "BR"]
        EIF = ["U", "D", "R", "BL", "BR", "L", "F", "B"]
        
        new_case = ""
        case.strip()
        
        for move in case.split(" "):
            suffix = ""
            if "'" in move:
                move = move.removesuffix("'")
                suffix = "'"
            new_case += " " + EIF[CIF.index(move)] + suffix
        return new_case.strip()


    # Rotates arount R face in EIF notation
    def x_rotation(self, case):
        start_orientation = ["U", "D", "F", "B", "R", "BL", "L", "BR"]
        final_orientation = ["B", "F", "BR", "L", "R", "BL", "U", "D"]

        new_case = ""
        case.strip()
        
        for move in case.split(" "):
            suffix = ""
            if "'" in move:
                move = move.removesuffix("'")
                suffix = "'"
            new_case += " " + final_orientation[start_orientation.index(move)] + suffix
        return new_case.strip()


    # Rotates arount U face
    def y_rotation(self, case):
        start_orientation = ["U", "D", "F", "B", "R", "BL", "L", "BR"]
        final_orientation = ["U", "D", "BL", "R", "L", "BR", "B", "F"]

        new_case = ""
        case.strip()
        
        for move in case.split(" "):
            suffix = ""
            if "'" in move:
                move = move.removesuffix("'")
                suffix = "'"
            new_case += " " + final_orientation[start_orientation.index(move)] + suffix
        return new_case.strip()

    # Rotates around UFR corner
    def tr_rotation(self, case):
        start_orientation = ["U", "D", "F", "B", "R", "BL", "L", "BR"]
        final_orientation = ["BR", "L", "U", "D", "F", "B", "BL", "R"]

        new_case = ""
        case.strip()
        
        for move in case.split(" "):
            suffix = ""
            if "'" in move:
                move = move.removesuffix("'")
                suffix = "'"
            new_case += " " + final_orientation[start_orientation.index(move)] + suffix
        return new_case.strip()

    # unwiden algs written with f and u moves
    def unwiden(self, case):
        start_centers = ["U", "u", "R", "BL", "BR", "L", "F", "f"]
        current_centers = ["U", "D", "R", "BL", "BR", "L", "F", "B"]

        new_case = ""
        case.strip()

        for move in case.split(" "):
            suffix = ""
            if "'" in move:
                move = move.removesuffix("'")
                suffix = "'"
            
            if move == "f"  and suffix != "'":
                current_centers[0], current_centers[2], current_centers[5] = current_centers[5], current_centers[0], current_centers[2]
                current_centers[1], current_centers[3], current_centers[4] = current_centers[4], current_centers[1], current_centers[3]
                new_case += " " + current_centers[start_centers.index(move)] + suffix
            elif move == "u" and suffix != "'":
                current_centers[2], current_centers[5], current_centers[7] = current_centers[7], current_centers[2], current_centers[5]
                current_centers[3], current_centers[4], current_centers[6] = current_centers[6], current_centers[3], current_centers[4]
                new_case += " " + current_centers[start_centers.index(move)] + suffix
            elif move == "f" and suffix == "'":
                current_centers[0], current_centers[2], current_centers[5] = current_centers[2], current_centers[5], current_centers[0]
                current_centers[1], current_centers[3], current_centers[4] = current_centers[3], current_centers[4], current_centers[1]
                new_case += " " + current_centers[start_centers.index(move)] + suffix
            elif move == "u" and suffix == "'":
                current_centers[2], current_centers[5], current_centers[7] = current_centers[5], current_centers[7], current_centers[2]
                current_centers[3], current_centers[4], current_centers[6] = current_centers[4], current_centers[6], current_centers[3]
                new_case += " " + current_centers[start_centers.index(move)] + suffix
            else:
                new_case += " " + current_centers[start_centers.index(move)] + suffix
        
        return new_case.strip()

    # widen algs to write with f and u moves
    def widen(self, case):
        new_case = []
        case.strip()

        list_case = case.split(" ")

        for i in range(len(list_case)):
            if list_case[0] == "B":
                list_case.pop(0)
                new_case.append("f")
                if len(list_case) > 0:
                    list_case = self.y_rotation(self.x_rotation(' '.join(list_case))).split(" ")
            elif list_case[0] == "B'":
                list_case.pop(0)
                new_case.append("f'")
                if len(list_case) > 0:
                    list_case = self.y_rotation(self.x_rotation(self.y_rotation(self.x_rotation(' '.join(list_case))))).split(" ")
            elif list_case[0] == "D":
                list_case.pop(0)
                new_case.append("u")
                if len(list_case) > 0:
                    list_case = self.y_rotation(' '.join(list_case)).split(" ")
            elif list_case[0] == "D'":
                list_case.pop(0)
                new_case.append("u'")
                if len(list_case) > 0:
                    list_case = self.y_rotation(self.y_rotation(' '.join(list_case))).split(" ")
            else:
                new_case.append(list_case.pop(0))
        
        return ' '.join(new_case)

    # turns BL moves into Rw moves (EIF)
    def rwiden(self, case):
        start_centers = ["U", "D", "R", "BL", "BR", "L", "F", "B"]
        current_centers = ["U", "D", "R", "Rw", "BR", "L", "F", "B"]

        new_case = ""
        case.strip()

        for move in case.split(" "):
            suffix = ""
            if "'" in move:
                move = move.removesuffix("'")
                suffix = "'"
            
            if move == "BL"  and suffix != "'":
                current_centers[1], current_centers[4], current_centers[6] = current_centers[6], current_centers[1], current_centers[4]
                current_centers[0], current_centers[7], current_centers[5] = current_centers[7], current_centers[5], current_centers[0]
                new_case += " " + current_centers[start_centers.index(move)] + suffix
            elif move == "BL" and suffix == "'":
                current_centers[1], current_centers[4], current_centers[6] = current_centers[4], current_centers[6], current_centers[1]
                current_centers[0], current_centers[7], current_centers[5] = current_centers[5], current_centers[0], current_centers[7]
                new_case += " " + current_centers[start_centers.index(move)] + suffix
            else:
                new_case += " " + current_centers[start_centers.index(move)] + suffix
        
        return new_case.strip()

    # turns BL moves into Rw moves (CIF)
    def rwiden_CIF(self, case):
        start_centers = ["U", "D", "R", "BL", "BR", "L", "F", "B"]
        current_centers = ["U", "D", "R", "Rw", "BR", "L", "F", "B"]

        new_case = ""
        case.strip()

        for move in case.split(" "):
            suffix = ""
            if "'" in move:
                move = move.removesuffix("'")
                suffix = "'"
            
            if move == "BL"  and suffix != "'":
                current_centers[1], current_centers[7], current_centers[5] = current_centers[5], current_centers[1], current_centers[7]
                current_centers[0], current_centers[4], current_centers[6] = current_centers[4], current_centers[6], current_centers[0]
                new_case += " " + current_centers[start_centers.index(move)] + suffix
            elif move == "BL" and suffix == "'":
                current_centers[1], current_centers[7], current_centers[5] = current_centers[7], current_centers[5], current_centers[1]
                current_centers[0], current_centers[4], current_centers[6] = current_centers[6], current_centers[0], current_centers[4]
                new_case += " " + current_centers[start_centers.index(move)] + suffix
            else:
                new_case += " " + current_centers[start_centers.index(move)] + suffix
        
        return new_case.strip()

    # variations [0] is EIF, [1] is CIF
    def generate_variations(self, case, U_Face="U"):
        rotations = []
        variations = [[], []]
        AUF = ""

        # if case.split()[0] ==  U_Face:
        #     AUF = U_Face
        # elif case.split()[0] == U_Face + "'":
        #     AUF = U_Face + "'"

        case = case.removeprefix(U_Face + "'")
        case = case.removesuffix(U_Face + "'") 
        case = case.removeprefix(U_Face)
        case = case.removesuffix(U_Face)
        
        case = case.strip()

        # white top
        rotations.append((case, AUF + " "))
        rotations.append((self.y_rotation(case), AUF + " Uo"))
        rotations.append((self.y_rotation(self.y_rotation(case)), AUF + " Uo'"))

        # orange top
        rotations.append((self.x_rotation(case), AUF + " Ro"))
        rotations.append((self.y_rotation(self.x_rotation(case)), AUF + " Ro Uo"))
        rotations.append((self.y_rotation(self.y_rotation(self.x_rotation(case))), AUF + " Ro Uo'"))

        # grey top
        rotations.append((self.x_rotation(self.x_rotation(case)), AUF + " Ro'"))
        rotations.append((self.y_rotation(self.x_rotation(self.x_rotation(case))), AUF + " Ro' Uo"))
        rotations.append((self.y_rotation(self.y_rotation(self.x_rotation(self.x_rotation(case)))), AUF + " Ro' Uo'"))

        # green top
        rotations.append((self.x_rotation(self.y_rotation(case)), AUF + " Lo'"))
        rotations.append((self.y_rotation(self.x_rotation(self.y_rotation(case))), AUF + " Tr2"))
        rotations.append((self.y_rotation(self.y_rotation(self.x_rotation(self.y_rotation(case)))), AUF + " Fo'"))

        # other orbit
        # white top
        rotations.append((self.tr_rotation(case), AUF + " Tr"))
        rotations.append((self.y_rotation(self.tr_rotation(case)), AUF + " Tr Uo"))
        rotations.append((self.y_rotation(self.y_rotation(self.tr_rotation(case))), AUF + " Tr Uo'"))

        # orange top
        rotations.append((self.x_rotation(self.tr_rotation(case)), AUF + " Tr Ro"))
        rotations.append((self.y_rotation(self.x_rotation(self.tr_rotation(case))), AUF + " Tr Ro Uo"))
        rotations.append((self.y_rotation(self.y_rotation(self.x_rotation(self.tr_rotation(case)))), AUF + " Tr Ro Uo'"))

        # grey top
        rotations.append((self.x_rotation(self.x_rotation(self.tr_rotation(case))), AUF + " Tr Ro'"))
        rotations.append((self.y_rotation(self.x_rotation(self.x_rotation(self.tr_rotation(case)))), AUF + " Tr Ro' Uo"))
        rotations.append((self.y_rotation(self.y_rotation(self.x_rotation(self.x_rotation(self.tr_rotation(case))))), AUF + " Tr Ro' Uo'"))

        # green top
        rotations.append((self.x_rotation(self.y_rotation(self.tr_rotation(case))), AUF + " Tr Lo'"))
        rotations.append((self.y_rotation(self.x_rotation(self.y_rotation(self.tr_rotation(case)))), AUF + " Tr'"))
        rotations.append((self.y_rotation(self.y_rotation(self.x_rotation(self.y_rotation(self.tr_rotation(case))))), AUF + " Tr Fo'"))

        for orientation in rotations:
            variations[0].append(orientation)
            variations[0].append((self.rwiden(orientation[0]), orientation[1]))
            variations[1].append((self.EIF2CIF(orientation[0]), orientation[1]))
            variations[1].append((self.rwiden_CIF(self.EIF2CIF(orientation[0])), orientation[1]))


        return variations


    def filter_solutions(self, algs):
        filtered = []

        for alg in algs[0]:
            score = 0
            move_count = 0


            for move in alg[0].split():
                move = move.removesuffix("'")
                move_count += 1

                if move == "B":
                    score += 5
                elif move == "F":
                    score += 4
                elif move == "BL":
                    score += 4
                elif move == "L":
                    score += 3
                elif move == "BR":
                    score += 2
                elif move == "R":
                    score += 1
                elif move == "U":
                    score += 1
                elif move == "Rw":
                    score += 1
                elif move == "D":
                    score += 1.5

            score -= alg.count("R U' R' U") * 2
            score -= alg.count("U' R U R'") * 2
            score -= alg.count("U R' U' R") * 2
            score -= alg.count("R' U R U'") * 2
            score -= alg.count("U R U' R'") * 2
            score -= alg.count("R U R' U'") * 2
            score -= alg.count("R' U' R U") * 2
            score -= alg.count("U' R' U R") * 2


            score -= alg.count("R U' R'") * 1 - alg.count("R U' R' U") * 1 - alg.count("U R U' R'") * 1
            score -= alg.count("U' R U") * 1 - alg.count("U' R U R'") * 1 - alg.count("R' U' R U") * 1
            score -= alg.count("U R' U'") * 1 - alg.count("U R' U' R") * 1 - alg.count("R U R' U'") * 1
            score -= alg.count("R' U R") * 1 - alg.count("R' U R U'") * 1 - alg.count("U' R' U R") * 1
            score -= alg.count("U R U'") * 1 - alg.count("U R U' R'") * 1 - alg.count("R U' R' U") * 1
            score -= alg.count("R U R'") * 1 - alg.count("R U R' U'") * 1 - alg.count("U R' U' R") * 1
            score -= alg.count("R' U' R") * 1 - alg.count("R' U' R U") * 1 - alg.count("U' R U R'") * 1
            score -= alg.count("U' R' U") * 1 - alg.count("U' R' U R") * 1 - alg.count("R' U R U'") * 1

            score -= alg.count("BR BL' BR' BL") * 8
            score -= alg.count("BL' BR BL BR'") * 8
            score -= alg.count("BL BR' BL' BR") * 8
            score -= alg.count("BR' BL BR BL'") * 8
            score -= alg.count("BL BR BL' BR'") * 8
            score -= alg.count("BR BL BR' BL'") * 8
            score -= alg.count("BR' BL' BR BL") * 8
            score -= alg.count("BL' BR' BL BR") * 8

            score -= alg.count("BR BL' BR'") * 4 - alg.count("BR BL' BR' BL") * 4 - alg.count("BL BR BL' BR'") * 4
            score -= alg.count("BL' BR BL") * 4 - alg.count("BL' BR BL BR'") * 4 - alg.count("BR' BL' BR BL") * 4
            score -= alg.count("BL BR' BL'") * 4 - alg.count("BL BR' BL' BR") * 4 - alg.count("BR BL BR' BL'") * 4
            score -= alg.count("BR' BL BR") * 4 - alg.count("BR' BL BR BL'") * 4 - alg.count("BL' BR' BL BR") * 4
            score -= alg.count("BL BR BL'") * 4 - alg.count("BL BR BL' BR'") * 4 - alg.count("BR BL' BR' BL") * 4
            score -= alg.count("BR BL BR'") * 4 - alg.count("BR BL BR' BL'") * 4 - alg.count("BL BR' BL' BR") * 4
            score -= alg.count("BR' BL' BR") * 4 - alg.count("BR' BL' BR BL") * 4 - alg.count("BL' BR BL BR'") * 4
            score -= alg.count("BL' BR' BL") * 4 - alg.count("BL' BR' BL BR") * 4 - alg.count("BR' BL BR BL'") * 4

            score -= alg.count("BR F' BR' F") * 8
            score -= alg.count("F' BR F BR'") * 8
            score -= alg.count("F BR' F' BR") * 8
            score -= alg.count("BR' F BR F'") * 8
            score -= alg.count("F BR F' BR'") * 8
            score -= alg.count("BR F BR' F'") * 8
            score -= alg.count("BR' F' BR F") * 8
            score -= alg.count("F' BR' F BR") * 8

            score -= alg.count("BR F' BR'") * 4 - alg.count("BR F' BR' F") * 4 - alg.count("F BR F' BR'") * 4
            score -= alg.count("F' BR F") * 4 - alg.count("F' BR F BR'") * 4 - alg.count("BR' F' BR F") * 4
            score -= alg.count("F BR' F'") * 4 - alg.count("F BR' F' BR") * 4 - alg.count("BR F BR' F'") * 4
            score -= alg.count("BR' F BR") * 4 - alg.count("BR' F BR F'") * 4 - alg.count("F' BR' F BR") * 4
            score -= alg.count("F BR F'") * 4 - alg.count("F BR F' BR'") * 4 - alg.count("BR F' BR' F") * 4
            score -= alg.count("BR F BR'") * 4 - alg.count("BR F BR' F'") * 4 - alg.count("F BR' F' BR") * 4
            score -= alg.count("BR' F' BR") * 4 - alg.count("BR' F' BR F") * 4 - alg.count("F' BR F BR'") * 4
            score -= alg.count("F' BR' F") * 4 - alg.count("F' BR' F BR") * 4 - alg.count("BR' F BR F'") * 4

            filtered.append((alg[0], "(EIF) " + alg[1], score, move_count))

        for alg in algs[1]:
            score = 0
            move_count = 0

            for move in alg[0].split():
                move_count += 1
                move = move.removesuffix("'")

                if move == "B":
                    score += 2
                elif move == "F":
                    score += 5
                elif move == "BL":
                    score += 5
                elif move == "L":
                    score += 2
                elif move == "BR":
                    score += 3
                elif move == "R":
                    score += 1
                elif move == "U":
                    score += 1
                elif move == "Rw":
                    score += 1
                elif move == "D":
                    score += 3

            score -= alg.count("Rw R'") * 0.5
            score -= alg.count("Rw' R") * 0.5
            score -= alg.count("R Rw'") * 0.5
            score -= alg.count("R' Rw") * 0.5


            score -= alg.count("R B' R' B") * 4
            score -= alg.count("B' R B R'") * 4
            score -= alg.count("B R' B' R") * 4
            score -= alg.count("R' B R B'") * 4
            score -= alg.count("B R B' R'") * 4
            score -= alg.count("R B R' B'") * 4
            score -= alg.count("R' B' R B") * 4
            score -= alg.count("B' R' B R") * 4

            score -= alg.count("R' L R L'") * 4
            score -= alg.count("L R' L' R") * 4
            score -= alg.count("R L' R' L") * 4
            score -= alg.count("L' R L R'") * 4
            score -= alg.count("L' R' L R") * 4
            score -= alg.count("R' L' R L") * 4
            score -= alg.count("L R L' R'") * 4
            score -= alg.count("R L R' L'") * 4


            score -= alg.count("R B' R'") * 2 - alg.count("R B' R' B") * 2 - alg.count("B R B' R'") * 2
            score -= alg.count("B' R B") * 2 - alg.count("B' R B R'") * 2 - alg.count("R' B' R B") * 2
            score -= alg.count("B R' B'") * 2 - alg.count("B R' B' R") * 2 - alg.count("R B R' B'") * 2
            score -= alg.count("R' B R") * 2 - alg.count("R' B R B'") * 2 - alg.count("B' R' B R") * 2
            score -= alg.count("B R B'") * 2 - alg.count("B R B' R'") * 2 - alg.count("R B' R' B") * 2
            score -= alg.count("R B R'") * 2 - alg.count("R B R' B'") * 2 - alg.count("B R' B' R") * 2
            score -= alg.count("R' B' R") * 2 - alg.count("R' B' R B") * 2 - alg.count("B' R B R'") * 2
            score -= alg.count("B' R' B") * 2 - alg.count("B' R' B R") * 2 - alg.count("R' B R B'") * 2

            score -= alg.count("R' L R") * 2 - alg.count("R' L R L'") * 2 - alg.count("L' R' L R") * 2
            score -= alg.count("L R' L'") * 2 - alg.count("L R' L' R") * 2 - alg.count("R L R' L'") * 2
            score -= alg.count("R L' R'") * 2 - alg.count("R L' R' L") * 2 - alg.count("L R L' R'") * 2
            score -= alg.count("L' R L") * 2 - alg.count("L' R L R'") * 2 - alg.count("R' L' R L") * 2
            score -= alg.count("L' R' L") * 2 - alg.count("L' R' L R") * 2 - alg.count("R' L R L'") * 2
            score -= alg.count("R' L' R") * 2 - alg.count("R' L' R L") * 2 - alg.count("L' R L R'") * 2
            score -= alg.count("L R L'") * 2 - alg.count("L R L' R'") * 2 - alg.count("R L' R' L") * 2
            score -= alg.count("R L R'") * 2 - alg.count("R L R' L'") * 2 - alg.count("L R' L' R") * 2

            score -= alg.count("R' D R D'") * 5
            score -= alg.count("D R' D' R") * 4
            score -= alg.count("R D' R' D") * 5
            score -= alg.count("D' R D R'") * 4
            score -= alg.count("D' R' D R") * 5
            score -= alg.count("D R D' R'") * 5


            score -= alg.count("R' D R") * 2 - alg.count("R' D R D'") * 2 - alg.count("D R D' R'") * 2
            score -= alg.count("D R' D'") * 2 - alg.count("D R' D' R") * 2
            score -= alg.count("R D' R'") * 2 - alg.count("R D' R' D") * 2 - alg.count("D' R' D R") * 2
            score -= alg.count("D' R D") * 2 - alg.count("D' R D R'") * 2
            score -= alg.count("D' R' D") * 2 - alg.count("D' R' D R") * 2 - alg.count("R D' R' D") * 2
            score -= alg.count("D R D'") * 2 - alg.count("D R D' R'") * 2 - alg.count("R' D R D'") * 2

            filtered.append((alg[0], "(CIF) " + alg[1], score, move_count))


        return filtered


    def generate_solutions(self, setup, slack=0, start_depth=4, max_depth=14):
        setup = self.CIF2EIF(setup)
        setup = self.widen(setup)

        AUFs = [("", ""), ("U ", ""), ("U' ", ""), ("", " U"), ("U ", " U"), ("U' ", " U"), ("", " U'"), ("U ", " U'"), ("U' ", " U'")]

        for i, auf in enumerate(AUFs):
            with open("D:\\Users\\tipst\\Downloads\\ksolve_pp\\FTO\\a" + str(i) + ".txt", 'w') as f:
                f.write("StartDepth " + str(start_depth) + "\n")
                f.write("Slack " + str(slack) + "\n")
                f.write("MaxDepth " + str(max_depth) + "\n")
                f.write("ScrambleAlg a\n")
                f.write(auf[0] + setup + auf[1] + "\n")
                f.write("End")


        subprocessess = [[],[],[],[],[],[],[],[],[]]
        final_solutions = []

        for i in range(9):
            subprocessess[i] = subprocess.Popen("FTO.exe a" + str(i) + ".txt", shell = True, cwd = "D:\\Users\\tipst\\Downloads\\ksolve_pp\\FTO",stdout=subprocess.PIPE,stdin=subprocess.PIPE)

        for i in range(9):
            nOutput = subprocessess[i].communicate()
            nOutput = nOutput[0].decode()
            nOutput = nOutput.split("Solving scramble")
            nOutput.pop(0)
            solutions = []
            
            nOutput = nOutput[0].split("Depth")
            nOutput.pop(0)
            for depth in nOutput:
                depth = depth.split("\r\n")
                depth.pop(0)
                depth.pop()
                depth.pop()
                solutions.extend(depth)

            for solution in solutions:
                final_solutions.append(solution.strip())

        return final_solutions
    
    def rank_algs(self, algs, U_Face="U"):
        all_solutions = [[],[]]
        for solution in algs:
            all_solutions[0].extend(self.generate_variations(self.unwiden(solution), U_Face)[0])
            all_solutions[1].extend(self.generate_variations(self.unwiden(solution), U_Face)[1])

        scored_solutions = self.filter_solutions(all_solutions)
        scored_solutions = sorted(set(scored_solutions), key=lambda x : x[2])

        return scored_solutions
    
    def rank_e_centers(self, alg):
        yauified = []
        score = len(alg.split())
        up = None

        for move in alg.split():
            if move == "U":
                if up == False:
                    score -= 0.5
                up = True
                yauified.append("R")
            elif move == "U'":
                if up == True:
                    score -= 0.5
                up = False
                yauified.append("R'")
            elif move == "u":
                if up == False:
                    score -= 0.5
                up = True
                yauified.append("Rw")
            elif move == "u'":
                if up == True:
                    score -= 0.5
                up = False
                yauified.append("Rw'")
            elif move == "F":
                yauified.append("U")
            elif move == "F'":
                yauified.append("U'")

        yauified = ' '.join(yauified)

        return (yauified, score)
    
    def rank_algs_rotation(self, algs, U_Face="U"):
        scored_solutions = []
        for solution in algs:
            list_solution = solution.split()

            for i, move in enumerate(list_solution):

                if i == 0:
                    continue
                first_half = ' '.join(list_solution[:i])
                second_half = ' '.join(list_solution[i:])


                first_half_variations = self.generate_variations(self.unwiden(first_half), U_Face)
                scored_first_half = self.filter_solutions(first_half_variations)

                second_half_variations = self.generate_variations(self.unwiden(second_half), U_Face)
                scored_second_half = self.filter_solutions(second_half_variations)

                for fh in scored_first_half:
                    for sh in scored_second_half:
                        scored_solutions.append((fh[0], sh[0], fh[1], sh[1], fh[2] + sh[2], fh[3] + sh[3]))

        scored_solutions = sorted(set(scored_solutions), key=lambda x : x[4])

        return scored_solutions