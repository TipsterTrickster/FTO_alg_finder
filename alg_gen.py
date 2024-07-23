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
    

    # Rotates arount R face in CIF notation
    def x_rotation(self, case):
        start_orientation = ["U", "D", "F", "B", "R", "BL", "L", "BR"]
        final_orientation = ["BR", "L", "U", "D", "R", "BL", "B", "F"]

        new_case = ""
        case.strip()
        
        for move in case.split(" "):
            suffix = ""
            if "'" in move:
                move = move.removesuffix("'")
                suffix = "'"
            new_case += " " + final_orientation[start_orientation.index(move)] + suffix
    
        return new_case.strip()


    # Rotates arount U face in CIF notation
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

    # Rotates around UF corner in CIF notation
    def T_rotation(self, case):
        start_orientation = ["U", "D", "F", "B", "R", "BL", "L", "BR"]
        final_orientation = ["R", "BL", "L", "BR", "F", "B", "U", "D"]

        new_case = ""
        case.strip()
        
        for move in case.split(" "):
            suffix = ""
            if "'" in move:
                move = move.removesuffix("'")
                suffix = "'"
            new_case += " " + final_orientation[start_orientation.index(move)] + suffix
        
        return new_case.strip()

    # turns BL moves into Rw moves (EIF)
    def rwiden_EIF(self, case):
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
        rotations.append((case, AUF + " {U,F}", AUF + " {U,L}"))
        rotations.append((self.y_rotation(case), AUF + " {U,BR}", AUF + " {U,R}"))
        rotations.append((self.y_rotation(self.y_rotation(case)), AUF + " {U,BL}", AUF + " {U,B}"))

        # orange top
        rotations.append((self.x_rotation(case), AUF + " {F,BR}", AUF + " {F,D}"))
        rotations.append((self.y_rotation(self.x_rotation(case)), AUF + " {F,U}", AUF + " {F,R}"))
        rotations.append((self.y_rotation(self.y_rotation(self.x_rotation(case))), AUF + " {F,BL}", AUF + " {F,L}"))

        # grey top
        rotations.append((self.x_rotation(self.x_rotation(case)), AUF + " {BR,U}", AUF + " {BR,B}"))
        rotations.append((self.y_rotation(self.x_rotation(self.x_rotation(case))), AUF + " {BR,F}", AUF + " {BR,R}"))
        rotations.append((self.y_rotation(self.y_rotation(self.x_rotation(self.x_rotation(case)))), AUF + " {BR,BL}", AUF + " {BR,D}"))

        # green top
        rotations.append((self.x_rotation(self.y_rotation(self.y_rotation(case))), AUF + " {BL,F}", AUF + " {BL,D}"))
        rotations.append((self.y_rotation(self.x_rotation(self.y_rotation(self.y_rotation(case)))), AUF + " {BL,U}", AUF + " {BL,L}"))
        rotations.append((self.y_rotation(self.y_rotation(self.x_rotation(self.y_rotation(self.y_rotation(case))))), AUF + " {BL,BR}", AUF + " {BL,B}"))

        # other orbit
        # white top
        rotations.append((self.T_rotation(case), AUF + " {L,R}", AUF + " {L,F}"))
        rotations.append((self.y_rotation(self.T_rotation(case)), AUF + " {L,B}", AUF + " {L,U}"))
        rotations.append((self.y_rotation(self.y_rotation(self.T_rotation(case))), AUF + " {L,D}", AUF + " {L,BL}"))

        # orange top
        rotations.append((self.x_rotation(self.T_rotation(case)), AUF + " {R,B}", AUF + " {R,BR}"))
        rotations.append((self.y_rotation(self.x_rotation(self.T_rotation(case))), AUF + " {R,L}", AUF + " {R,U}"))
        rotations.append((self.y_rotation(self.y_rotation(self.x_rotation(self.T_rotation(case)))), AUF + " {R,D}", AUF + " {R,F}"))

        # grey top
        rotations.append((self.x_rotation(self.x_rotation(self.T_rotation(case))), AUF + " {B,L}", AUF + " {B,BL}"))
        rotations.append((self.y_rotation(self.x_rotation(self.x_rotation(self.T_rotation(case)))), AUF + " {B,R}", AUF + " {B,U}"))
        rotations.append((self.y_rotation(self.y_rotation(self.x_rotation(self.x_rotation(self.T_rotation(case))))), AUF + " {B,D}", AUF + " {R,BR}"))

        # green top
        rotations.append((self.x_rotation(self.y_rotation(self.y_rotation(self.T_rotation(case)))), AUF + " {D,R}", AUF + " {D,BR}"))
        rotations.append((self.y_rotation(self.x_rotation(self.y_rotation(self.y_rotation(self.T_rotation(case))))), AUF + " {D,L}", AUF + " {D,F}"))
        rotations.append((self.y_rotation(self.y_rotation(self.x_rotation(self.y_rotation(self.y_rotation(self.T_rotation(case)))))), AUF + " {D,B}", AUF + " {D,BL}"))

        for orientation in rotations:
            variations[0].append((self.CIF2EIF(orientation[0]), orientation[2]))
            variations[0].append((self.rwiden_EIF(self.CIF2EIF(orientation[0])), orientation[2]))
            variations[1].append((orientation[0], orientation[1]))
            variations[1].append((self.rwiden_CIF(orientation[0]), orientation[1]))

        return variations

    def filter_solutions(self, algs):
        filtered = []

        # EIF
        for alg in algs[0]:
            replace_alg = f" {alg[0]} "
            score = 0
            move_count = 0
            triggers = [(" R' U R U' ", " SD "), (" U R' U' R ", " SD' "), (" R U' R' U ", " HD "), (" U' R U R' ", " HD' "), (" R U R' U' ", " SX "), (" U R U' R' ", " SX' "),
                        (" R' U' R U ", " BX "), (" U' R' U R ", " BX' "), (" R U R' ", " FI "), (" R U' R' ", " FI' "), (" R' U R ", " BI "), (" R' U' R ", " BI' "),
                        (" R Rw' ", " M "), (" Rw' R ", " M "), (" R' Rw ", " M' "), (" Rw R' ", " M' ")]

            for trigger in triggers:
                replace_alg = replace_alg.replace(trigger[0], trigger[1])

            grip_up = None
            for move in replace_alg.strip().split():     
                if move == "R" or move == "Rw":
                    if grip_up == False:
                        score += 0.5
                    elif grip_up == True:
                        score += 1.5
                    else:
                        score += 0.5
                    grip_up = True
                elif move == "R'" or move == "Rw'":
                    if grip_up == True:
                        score += 0.5
                    elif grip_up == False:
                        score += 1.5
                    else:
                        score += 0.5
                    grip_up = False

                move = move.removesuffix("'")


                if move == "B":
                    score += 5
                elif move == "F":
                    score += 4
                elif move == "BL":
                    score += 4
                elif move == "L":
                    score += 3
                elif move == "BR":
                    score += 1.5
                elif move == "U":
                    score += 1
                elif move == "D":
                    score += 1.5
                elif move == "SD":
                    score += 2
                elif move == "HD":
                    score += 2
                elif move == "SX":
                    score += 2
                elif move == "BX":
                    score += 2
                elif move == "FI":
                    score += 1.5
                elif move == "BI":
                    score += 1.5
                elif move == "M":
                    score += 1.25

            filtered.append((alg[0], alg[1] + " (EIF)", score, len(alg[0].split())))

        for alg in algs[1]:
            replace_alg = f" {alg[0]} "
            score = 0
            move_count = 0

            triggers = [(" R' U R U' ", " SD "), (" U R' U' R ", " SD' "), (" R U' R' U ", " HD "), (" U' R U R' ", " HD' "), (" R U R' U' ", " SX "), (" U R U' R' ", " SX' "),
                        (" R' U' R U ", " BX "), (" U' R' U R ", " BX' "), (" R U R' ", " FI "), (" R U' R' ", " FI' "), (" R' U R ", " BI "), (" R' U' R ", " BI' "),
                        (" R' L R L' ", " SL "), (" L R' L' R ", " SL' "), (" R B' R' B ", " HE "), (" B' R B R' ", " HE' "),
                        (" R' L R ", " SH "), (" R' L' R ", " SH' "), (" R B' R' ", " HH "), (" R B R' ", " HH' "),
                        (" R Rw' ", " M "), (" Rw' R ", " M "), (" R' Rw ", " M' "), (" Rw R' ", " M' ")]

            for trigger in triggers:
                replace_alg = replace_alg.replace(trigger[0], trigger[1])

            grip_up = None
            for move in replace_alg.strip().split():     
                if move == "R" or move == "Rw":
                    if grip_up == False:
                        score += 0.5
                    elif grip_up == True:
                        score += 1.5
                    else:
                        score += 0.5
                    grip_up = True
                elif move == "R'" or move == "Rw'":
                    if grip_up == True:
                        score += 0.5
                    elif grip_up == False:
                        score += 1.5
                    else:
                        score += 0.5
                    grip_up = False

                move = move.removesuffix("'")


                if move == "B":
                    score += 2
                elif move == "F":
                    score += 4
                elif move == "BL":
                    score += 4
                elif move == "L":
                    score += 2
                elif move == "BR":
                    score += 2
                elif move == "U":
                    score += 1
                elif move == "D":
                    score += 1.5
                elif move == "SD":
                    score += 2
                elif move == "HD":
                    score += 2
                elif move == "SX":
                    score += 2
                elif move == "BX":
                    score += 2
                elif move == "FI":
                    score += 1.5
                elif move == "BI":
                    score += 1.5
                elif move == "M":
                    score += 1.25
                elif move == "SL":
                    score += 2
                elif move == "HE":
                    score += 2
                elif move == "SH":
                    score += 1.5
                elif move == "HH":
                    score += 1.5


            filtered.append((alg[0], alg[1] + " (CIF)", score, len(alg[0].split())))


        return filtered

    def generate_solutions_twizzle(self, setup, count=1000, start_depth=4, max_depth=15, memory=4096, U_Face = "U"):

        AUFs = [("", ""), ("U ", ""), ("U' ", ""), ("", " U"), ("U ", " U"), ("U' ", " U"), ("", " U'"), ("U ", " U'"), ("U' ", " U'")]

        with open("./twizzle/l3t.scr", 'w') as f:
            for auf in AUFs:
                f.write("ScrambleAlg L3T\n")
                f.write(auf[0] + setup + auf[1] + "\n")
                f.write("End\n")

        twsearch_path = "/home/aedan/Desktop/cubing/twsearch/build/bin/twsearch"

        p = subprocess.Popen(f"{twsearch_path} -M {memory} -c {count} --maxdepth {max_depth} --quiet twizzle/FTO.tws twizzle/l3t.scr", shell = True, stdout=subprocess.PIPE)

        pOut = p.communicate()
        p.kill()

        pOut = pOut[0].decode().split("\n")[1:-2]
        pOut = [x.strip() for x in pOut if "found" not in x.lower()]

        pOut = list(filter(lambda alg: self.filter_AUF(alg, U_Face), pOut))

        return pOut
    
    def rank_algs(self, algs, U_Face="U", count=100):
        all_solutions = [[],[]]

        for solution in algs:
            all_solutions[0].extend(self.generate_variations(solution, U_Face)[0])
            all_solutions[1].extend(self.generate_variations(solution, U_Face)[1])

        scored_solutions = self.filter_solutions(all_solutions)
        scored_solutions = sorted(set(scored_solutions), key=lambda x : x[2])

        return scored_solutions[:count]

    def rank_algs_rotation(self, algs, U_Face="U", count=100, cutoff=3):
        scored_solutions = []
        for solution in algs:
            list_solution = solution.split()

            for i, move in enumerate(list_solution):

                if i <= 3 or i >= len(list_solution) - 3:
                    continue
                first_half = ' '.join(list_solution[:i])
                second_half = ' '.join(list_solution[i:])

                first_half_variations = self.generate_variations(first_half, U_Face="}")
                scored_first_half = self.filter_solutions(first_half_variations)
                scored_first_half = sorted(set(scored_first_half), key=lambda x : x[2])[:cutoff]

                second_half_variations = self.generate_variations(second_half, U_Face="}")
                scored_second_half = self.filter_solutions(second_half_variations)
                scored_second_half = sorted(set(scored_second_half), key=lambda x : x[2])[:cutoff]

                for fh in scored_first_half:
                    for sh in scored_second_half:
                        scored_solutions.append((fh[0], sh[0], fh[1], sh[1], fh[2] + sh[2], fh[3] + sh[3]))

        scored_solutions = sorted(set(scored_solutions), key=lambda x : x[4])

        return scored_solutions[:count]
    
    def filter_AUF(self, case, U_Face="U"):
        if case.split()[0] ==  U_Face:
            return False
        elif case.split()[0] == U_Face + "'":
            return False
        elif case.split()[-1] ==  U_Face:
            return False
        elif case.split()[-1] == U_Face + "'":
            return False
        else:
            return True