import json
from .models import Major

class MajorManagment():
    def create_major(name, major_dictionary):
        major_course = json.dumps(major_dictionary)
        Major.objects.update_or_create(
                    name = name,
                    defaults={
                        'major_courses': major_course,
                        'name': name
                    }
                )

Computer_Science_B_A_ = {
  "CSCI1101": "",
  "CSCI1102": "",
  "CSCI2271": "",
  "CSCI2272": "",
  "CSCI2243": "",
  "CSCI2244": "",
  "CSCI3383": "",
  "CSCI2": "",
  "CSCI3": 3,
  "MATH1103": "", # probably also need MATH1102
}

Computer_Science_B_S_ = {
  "CSCI1101": "",
  "CSCI1102": "",
  "CSCI2271": "",
  "CSCI2272": "",
  "CSCI2243": "",
  "CSCI2244": "",
  "CSCI3383": "",
  "CSCI2": 1,
  "CSCI3": 3,
  "MATH1103": "",
  "Natural_Science": [["BIOL2000", "BIOL2010", "BIOL2040"], ["BIOL2000", "BIOL1300", "BIOL2040"], ["CHEM1109", "CHEM1110"], ["PHYS2200", "PHYS2050", "PHYS2201", "PHYS2051"], ["EESC1132", "EESC22", "EESC22"], ["EESC1132", ["EESC2", "EESC3", "EESC4"]], ["EESC22", "EESC22", ["EESC2", "EESC3", "EESC4"]]]
}

Math_B_A_ = {
  "MATH220": "", # to account for honors sections, 2202 and 2203
  "MATH221": "", # to account for honors sections
  "MATH2216": "",
  "MATH3310": "",
  "MATH3320": "",
  "MATH330": 6, # 6 electives numbered 3312, 3322, or 4400 and above
}

Core_req = {
  "ma": "", #math
  "ns": "", #natural science
  "h1": "", #history1
  "h2": "", #history2
  "cd": "", #culture/diversity
  "li": "", #literature
  "ph": "", #philosp
  "ss": 2,  #social science
  "th": "", #theology
  "wr": "", #writing
  "fa": "" #fine art
}

Computer_Science = {
  "CSCI1101": "",
  "CSCI1102": "",
  "CSCI2271": "",
  "CSCI2272": "",
  "CSCI2243": "",
  "CSCI2244": "",
  "CSCI3383": "",
  "CSCI2": "",
  "CSCI3": 3,
  "MATH1103": "",
}

Math_Minor = { # missing that with approval, students can substitute required course for elective
  "MATH220": "",
  "MATH221":"",
  "Electives": [["MATH22", "MATH33","MATH44"], 4]
}

CS_Minor = { # missing that you can't take the classes from the ethical issues cluster
  "CSCI1101":"",
  "CSCI1102":"",
  "Choice_1": ["CSCI2271","CSCI2243"],
  "CSCI2":"",
  "CSCI3": 2,
  "MATH1103":""
}

def create_all_majors():
    MajorManagment.create_major("Computer Science B.A.", Computer_Science_B_A_)
    MajorManagment.create_major("Computer Science B.S.", Computer_Science_B_S_)
    MajorManagment.create_major("Mathematics B.A.", Math_B_A_)
    MajorManagment.create_major("Core Requirements", Core_req)
    MajorManagment.create_major("Mathematics", Math_Minor)
    MajorManagment.create_major("Computer Science", CS_Minor)




