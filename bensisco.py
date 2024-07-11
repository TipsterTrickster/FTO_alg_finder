import subprocess
import concurrent.futures
from subprocess import Popen, PIPE
import re
from itertools import groupby
import csv



class StepSolvers():
    def __init__(self):
        pass

    def filter_fcs(self, fc):
        fc = fc[2].removesuffix("'")
        if fc.endswith("F") or fc.endswith("BR") or fc.endswith("BL") or fc.endswith("U") or fc.endswith("u"):
            return False
        return True

    def filter_fbs(self, fc):
        fc = fc[3].removesuffix("'")
        if fc.endswith("F") or fc.endswith("U") or fc.endswith("u"):
            return False
        return True

    def firstcenter(self, scrambles, slack, depth, start_depth=0):
        p = subprocess.Popen("fto.exe a.txt", shell = True, cwd = "D:\\Users\\tipst\\Downloads\\ksolve_pp\\FTO_FC_EIF",stdout=subprocess.PIPE,stdin=subprocess.PIPE)
        with open("D:\\Users\\tipst\\Downloads\\ksolve_pp\\FTO_FC_EIF\\a.txt", 'w') as f:
            for scram in scrambles:
                f.write(f"\nSlack {slack}\n")
                f.write(f"StartDepth {start_depth}\n")
                f.write(f"MaxDepth {depth}\n")
                f.write("ScrambleAlg a\n" + scram)
                f.write("\nEnd")
        nOutput = p.communicate()
        nOutput = nOutput[0].decode()
        nOutput = nOutput.split("Solving scramble")
        nOutput.pop(0)
        solutions = []
        for j, case in enumerate(nOutput):
            for i, depth in enumerate(case.split("Depth")):
                if i == 0:
                    continue
                d = depth.split("\r\n")
                d.pop(0)
                d.pop()
                d.pop()
                d = [(9, scrambles[j], d.strip()) for d in d]
                solutions.extend((d))


        solutions = list(set(solutions))
        solutions = list(filter(self.filter_fcs, solutions))
        
        return solutions


    def run_fb_solver(self, index):
        process = subprocess.Popen(f"fto.exe b{index}.txt", shell = True, cwd = "D:\\Users\\tipst\\Downloads\\ksolve_pp\\FTO_FB_EIF",stdout=subprocess.PIPE,stdin=subprocess.PIPE)
        output = process.communicate()
        return output


    def firstblock_fast(self, scrambles, slack, total_depth, step_depth):
        R_cycles = ["", "BL L BL f F' u BL u F u BL' f' BL' L' BL'", "BL L BL f BL u' F' u' BL' u' F f' BL' L' BL'"]
        L_cycles = ["", "BR f u f F' BR F BR u F u' f' u' f' BR'", "BR f u f u F' u' BR' F' BR' F f' u' f' BR'"]
        B_cycles = ["", "BR' f F' BR F BR' f' BR", "R L' BR' BL BR BL u BR u' L R'", "BL f' F BL' F' BL f BL'", "R L' u BR' u' BL' BR' BL' BR L R'", "R L' BR' BL BR BL' BR BL BR' BL' L R'"]

        for i in range(3):
            for j in range(3):
                for k in range(6):
                    with open(f"D:\\Users\\tipst\\Downloads\\ksolve_pp\\FTO_FB_EIF\\b{(i) + (3 * j) + (9 * k)}.txt", 'w') as f:
                        for scram in scrambles:
                            f.write(f"\nSlack {slack}\n")
                            f.write(f"MaxDepth {min(step_depth, (total_depth - scram[0]))}\n")
                            f.write(f"ScrambleAlg a\n {B_cycles[k]} {R_cycles[i]} {L_cycles[j]} {scram[1]} {scram[2]}")
                            f.write("\nEnd")

        solutions = []

        with concurrent.futures.ThreadPoolExecutor(max_workers=9) as executor:
            futures = [executor.submit(self.run_fb_solver, i) for i in range(54)]
            for future in concurrent.futures.as_completed(futures):
                output = future.result()
                nOutput = output[0].decode()
                nOutput = nOutput.split("Solving scramble")
                nOutput.pop(0)
                for j, case in enumerate(nOutput):
                    for i, depth in enumerate(case.split("Depth")):
                        if i == 0:
                            continue
                        d = depth.split("\r\n")
                        d.pop(0)
                        d.pop()
                        d.pop()
                        d = [(i + scrambles[j][0], scrambles[j][1], scrambles[j][2], d.strip()) for d in d]
                        solutions.extend((d))
  
        solutions = list(set(solutions))
        solutions = list(filter(self.filter_fbs, solutions))

        return solutions

    def firstblock(self, scrambles, slack, total_depth, step_depth):
        R_cycles = ["", "BL L BL f F' u BL u F u BL' f' BL' L' BL'", "BL L BL f BL u' F' u' BL' u' F f' BL' L' BL'"]
        L_cycles = ["", "BR f u f F' BR F BR u F u' f' u' f' BR'", "BR f u f u F' u' BR' F' BR' F f' u' f' BR'"]
        B_cycles = ["", "BR' f F' BR F BR' f' BR", "R L' BR' BL BR BL u BR u' L R'", "BL f' F BL' F' BL f BL'", "R L' u BR' u' BL' BR' BL' BR L R'", "R L' BR' BL BR BL' BR BL BR' BL' L R'"]

        with open(f"D:\\Users\\tipst\\Downloads\\ksolve_pp\\FTO_FB_EIF\\b.txt", 'w') as f:
            for scram in scrambles:
                for i in range(3):
                    for j in range(3):
                        for k in range(6):
                            f.write(f"\nSlack {slack}\n")
                            f.write(f"MaxDepth {min(step_depth, (total_depth - scram[0]))}\n")
                            f.write(f"ScrambleAlg a\n {B_cycles[k]} {R_cycles[i]} {L_cycles[j]} {scram[1]} {scram[2]}")
                            f.write("\nEnd")

        solutions = []

        p = subprocess.Popen(f"fto.exe b.txt", shell = True, cwd = "D:\\Users\\tipst\\Downloads\\ksolve_pp\\FTO_FB_EIF",stdout=subprocess.PIPE,stdin=subprocess.PIPE)
        nOutput = p.communicate()
        nOutput = nOutput[0].decode()
        nOutput = nOutput.split("Solving scramble")
        nOutput.pop(0)
        for j, case in enumerate(nOutput):
            k = j // 54
            for i, depth in enumerate(case.split("Depth")):
                if i == 0:
                    continue
                d = depth.split("\r\n")
                d.pop(0)
                d.pop()
                d.pop()
                d = [(i + scrambles[k][0], scrambles[k][1], scrambles[k][2], d.strip()) for d in d]
                solutions.extend((d))
        solutions = list(set(solutions))
        solutions = list(filter(self.filter_fbs, solutions))

        return solutions

    def firstblock_long(self, scrambles, slack, total_depth, step_depth):
        R_cycles = ["", "BL L BL f F' u BL u F u BL' f' BL' L' BL'", "BL L BL f BL u' F' u' BL' u' F f' BL' L' BL'"]
        L_cycles = ["", "BR f u f F' BR F BR u F u' f' u' f' BR'", "BR f u f u F' u' BR' F' BR' F f' u' f' BR'"]
        B_cycles = ["", "BR' f F' BR F BR' f' BR", "R L' BR' BL BR BL u BR u' L R'", "BL f' F BL' F' BL f BL'", "R L' u BR' u' BL' BR' BL' BR L R'", "R L' BR' BL BR BL' BR BL BR' BL' L R'"]

        solutions = []

        for rcycles in range(3):
            for lcycles in range(3):
                for bcycles in range(6):
                    with open(f"D:\\Users\\tipst\\Downloads\\ksolve_pp\\FTO_FB_EIF\\b.txt", 'w') as f:
                        for scram in scrambles:
                            f.write(f"\nSlack {slack}\n")
                            f.write(f"MaxDepth {min(step_depth, (total_depth - scram[0]))}\n")
                            f.write(f"ScrambleAlg a\n {B_cycles[bcycles]} {R_cycles[rcycles]} {L_cycles[lcycles]} {scram[1]} {scram[2]}")
                            f.write("\nEnd")

                    

                    p = subprocess.Popen(f"fto.exe b.txt", shell = True, cwd = "D:\\Users\\tipst\\Downloads\\ksolve_pp\\FTO_FB_EIF",stdout=subprocess.PIPE,stdin=subprocess.PIPE)
                    nOutput = p.communicate()
                    nOutput = nOutput[0].decode()
                    nOutput = nOutput.split("Solving scramble")
                    nOutput.pop(0)
                    for j, case in enumerate(nOutput):
                        for i, depth in enumerate(case.split("Depth")):
                            if i == 0:
                                continue
                            d = depth.split("\r\n")
                            d.pop(0)
                            d.pop()
                            d.pop()
                            d = [(i + scrambles[j][0], scrambles[j][1], scrambles[j][2], d.strip()) for d in d]
                            solutions.extend((d))
 
        solutions = list(set(solutions))
        solutions = list(filter(self.filter_fbs, solutions))

        return solutions



    def e_centers(self, scrambles, slack, total_depth, step_depth):
        p = subprocess.Popen("fto.exe c.txt", shell = True, cwd = "D:\\Users\\tipst\\Downloads\\ksolve_pp\\FTO_EC_EIF",stdout=subprocess.PIPE,stdin=subprocess.PIPE)
        with open("D:\\Users\\tipst\\Downloads\\ksolve_pp\\FTO_EC_EIF\\c.txt", 'w') as f:
            for scram in scrambles:
                    f.write(f"\nSlack {slack}\n")
                    f.write(f"MaxDepth {min(step_depth, (total_depth - scram[0]))}\n")
                    f.write(f"ScrambleAlg a\n{scram[1]} {scram[2]} {scram[3]}")
                    f.write("\nEnd")
        nOutput = p.communicate()
        nOutput = nOutput[0].decode()
        nOutput = nOutput.split("Solving scramble")
        nOutput.pop(0)
        solutions = []
        for j, case in enumerate(nOutput):
            for i, depth in enumerate(case.split("Depth")):
                if i == 0:
                    continue
                d = depth.split("\r\n")
                d.pop(0)
                d.pop()
                d.pop()
                d = [(i + scrambles[j][0], scrambles[j][1], scrambles[j][2], scrambles[j][3], d.strip()) for d in d]
                solutions.extend((d))
        return solutions

    def finish(self, scrambles, slack, total_depth, step_depth):
        p = subprocess.Popen("fto.exe d.txt", shell = True, cwd = "D:\\Users\\tipst\\Downloads\\ksolve_pp\\FTO",stdout=subprocess.PIPE,stdin=subprocess.PIPE)
        with open("D:\\Users\\tipst\\Downloads\\ksolve_pp\\FTO\\d.txt", 'w') as f:
            for scram in scrambles:
                    f.write(f"\nSlack {slack}\n")
                    f.write(f"MaxDepth {min(step_depth, (total_depth - scram[0]))}\n")
                    f.write(f"ScrambleAlg a\n{scram[1]} {scram[2]} {scram[3]} {scram[4]}")
                    f.write("\nEnd")
        nOutput = p.communicate()
        nOutput = nOutput[0].decode()
        nOutput = nOutput.split("Solving scramble")
        nOutput.pop(0)
        solutions = []
        for j, case in enumerate(nOutput):
            for i, depth in enumerate(case.split("Depth")):
                if i == 0:
                    continue
                d = depth.split("\r\n")
                d.pop(0)
                d.pop()
                d.pop()
                if i == 1 and ("16 nodes" in depth):
                    solutions.extend([(i + scrambles[j][0], scrambles[j][1], scrambles[j][2], scrambles[j][3], scrambles[j][4], "")])
                d = [(i + scrambles[j][0], scrambles[j][1], scrambles[j][2], scrambles[j][3], scrambles[j][4], d.strip()) for d in d]
                solutions.extend((d))
        return solutions
    

class Transformations():
    def __init__(self):
        pass
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

    # variations [0] is EIF, [1] is CIF
    def generate_variations(self, case, U_Face="U"):
        rotations = []
        
        case = case.strip()

        # white top
        rotations.append(case)
        rotations.append(self.y_rotation(case))
        rotations.append(self.y_rotation(self.y_rotation(case)))

        # orange top
        rotations.append(self.x_rotation(case))
        rotations.append(self.x_rotation(self.y_rotation(case)))
        rotations.append(self.x_rotation(self.y_rotation(self.y_rotation(case))))

        # grey top
        rotations.append(self.x_rotation(self.x_rotation(case)))
        rotations.append(self.x_rotation(self.x_rotation(self.y_rotation(case))))
        rotations.append(self.x_rotation(self.x_rotation(self.y_rotation(self.y_rotation(case)))))

        # green top
        rotations.append(self.y_rotation(self.x_rotation(case)))
        rotations.append(self.y_rotation(self.x_rotation(self.y_rotation(case))))
        rotations.append(self.y_rotation(self.x_rotation(self.y_rotation(self.y_rotation(case)))))

        # other orbit
        rotations.append(self.tr_rotation(case))
        rotations.append(self.tr_rotation(self.y_rotation(case)))
        rotations.append(self.tr_rotation(self.y_rotation(self.y_rotation(case))))

        rotations.append(self.tr_rotation(self.x_rotation(case)))
        rotations.append(self.tr_rotation(self.x_rotation(self.y_rotation(case))))
        rotations.append(self.tr_rotation(self.x_rotation(self.y_rotation(self.y_rotation(case)))))

        rotations.append(self.tr_rotation(self.x_rotation(self.x_rotation(case))))
        rotations.append(self.tr_rotation(self.x_rotation(self.x_rotation(self.y_rotation(case)))))
        rotations.append(self.tr_rotation(self.x_rotation(self.x_rotation(self.y_rotation(self.y_rotation(case))))))

        rotations.append(self.tr_rotation(self.y_rotation(self.x_rotation(case))))
        rotations.append(self.tr_rotation(self.y_rotation(self.x_rotation(self.y_rotation(case)))))
        rotations.append(self.tr_rotation(self.y_rotation(self.x_rotation(self.y_rotation(self.y_rotation(case))))))

        return rotations