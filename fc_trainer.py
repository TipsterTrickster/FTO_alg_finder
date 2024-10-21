from alg_gen import AlgGen
import subprocess


class FirstCenter(AlgGen):
    def __init__(self):
        # Make these SUPER (CUBE)
        self.rotations = {"{U, F}": "", "{U, BL}": "F D B' D U' L' BL D F D U B' BR B' U'", "{U, BR}": "U B BR' B U' D' F' D' BL' L U D' B D' F'",
                          "{F, BR}": "F D' F D' R U R BR BL B' BL' R D' BL' R", "{F,U}": "F B' BL' L BL' D' U BR' R F BR' B' BL' L BL'", "{F, BL}": "B BR' L' F' L' U' R BR L' B BR L' F' D F'",
                          "{BR, U}": "R' BL D R' BL B BL' BR' R' U' R' D F' D F'", "{BR, BL}": "F B' BR' D BR' R' U' BL L F U' B' BR' D BR'", "{BR, F}": "U R' U R' B BL B BR F D' B F' R' B F'",
                          "{BL, U}": "F D' F L BR' B' L BR' R' U L F L BR B'", "{BL, F}": "F B' R F B' D F' BR' B' BL' B' R U' R U'", "{BL, BR}": "BL B BR' U D' F' L BL F' R' BR' B BR' D' F'"}


    def generate_solutions_twizzle(self, setup, count=1000, start_depth=0, max_depth=8, memory=8192, U_Face = "U"):

        solutions = []
        min = 99

        for orientation, rotation in zip(self.rotations.keys(), self.rotations.values()):
            with open("./twizzle/first_center.scr", 'w') as f:
                    f.write("ScrambleAlg FC\n")
                    f.write(f"{setup} {rotation}\n")
                    f.write("End\n")

            twsearch_path = "/home/aedan/Desktop/cubing/twsearch/build/bin/twsearch"

            p = subprocess.Popen(f"{twsearch_path} -M {memory} -c {count} --maxdepth {max_depth} --quiet twizzle/FTO_FC.tws twizzle/first_center.scr", shell = True, stdout=subprocess.PIPE)

            pOut = p.communicate()
            p.kill()

            pOut = pOut[0].decode().split("\n")[1:-2]
            pOut = [x.strip() for x in pOut if "found" not in x.lower()]

            pOut = [(orientation, x, len(x.split())) for x in pOut]
            solutions.extend(pOut)

        return solutions