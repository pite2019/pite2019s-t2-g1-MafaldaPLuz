import json

class Student:
    def __init__(self, name, surname, student_number):
        self.name = name
        self.surname = surname
        self.student_number = student_number
        self.classes = []
      
    def __getitem__(self, index):
        return self.classes[index]

    def __setitem__(self,index,value):
        self.classes[index] = value
       
    def changeAverage(self):
        list_grades = []
        sub_list_grades = []
        for classroom in self.classes:
            info_student = classroom.students_info
            sub_list_grades = info_student[self.student_number]['grades : ']
            for sub in sub_list_grades:    
                list_grades.append(sub)
    
    def changeAttendance(self):
        list_grades = []
        i=0
        for classroom in self.classes:
            info_student = classroom.students_info
            list_grades.append(info_student[self.student_number]['attendance : '])
            i+=1
    

class Classroom:

    def __init__(self, subject):
        self.subject = subject
        self.list_students = []
        self.students_info = {}

    def __len__(self):
        return len(self.list_students)

    def __getitem__(self, student_number):
        return self.list_students[student_number]
    
    def addStudentToClass (self, name, surname, student_number):
        student = Student(name,surname,student_number)
        self.list_students.append(student)
        student_data = ['attendance : ', 'average : ', 'grades : ']
        student.classes.append(self)
        for i in self.list_students:
            self.students_info[student_number] = {}
            for entry in student_data:
                if(entry=='grades : '):
                    self.students_info[student_number][entry] = []
                else:
                    self.students_info[student_number][entry] = 0
        
    def classAverage(self):
        sumAvg = 0
        for student in self.list_students:
            sumAvg += int(self.students_info[student.student_number]['average : '])
        nStudents = len(self.list_students)
        return sumAvg / nStudents         
        
    def addGrade(self, student_number, grade):
        self.students_info[student_number]['grades : '].append(grade)
        list_grades = self.students_info[student_number]['grades : ']
        average = calculateAverage(list_grades)
        self.students_info[student_number]['average : '] = average
        index = findStudent(self.list_students, student_number)
        self.list_students[index].changeAverage()
    
    def addAttendance(self, student_number):
        number = int(self.students_info[student_number]['attendance : '])
        self.students_info[student_number]['attendance : '] = number + 1
        index = findStudent(self.list_students, student_number)
        self.list_students[index].changeAttendance()
        
    def positiveAverage(self,grade):
        if(grade >= 3):
            return True
        else:
            return False
        
    def numberPositiveAverage(self):
        listOfAverages = []
        for student in self.list_students:
            listOfAverages.append(self.students_info[student.student_number]['average : '])
        filtered = filter(self.positiveAverage,listOfAverages)
        return len(list(filtered))
    

def findStudent(list_students, number):
    for student in list_students:
        if (student.student_number == number):
            index = list_students.index(student)
    return index
    
def calculateAverage(grades = list()):
    average = 0
    sum_grades = 0
    for grade in grades:
        sum_grades += int(grade)
    average= sum_grades / len(grades)
    return average


   
def main():
    print('Welcome to the user interface menu!')
    keepGoing = True
    students = []
    subjects = []
    
    with open('data.txt') as json_file:  
        data = json.load(json_file)
    for student in data['students']:
        students.append(Student(student['name'], student['surname'], student['student number']))
    for subject in data['classroom']: 
        subjects.append(Classroom(subject['subject name']))
            
    while(keepGoing):
        print('Choose one of the following options:')
        print('1 - Create a new Subject')
        print('2 - Create a Student')
        print('3 - Add a Student to a Class')
        print('4 - Add a grade of a Student in a Class')
        print('5 - Add +1 attendance of a Student in a Class')
        print('6 - Check the average Grade of a Class')
        print('7 - Check the average Grade of a Student')
        print('8 - Check the average Grade of a Student in a Class')
        print('9 - Check the Attendance of a Student')
        print('10 - Check the Attendance of a Student in a Class')
        print('11 - Check how many Students have a positive grade in a Class')
        print('0 - Exit')
        
        number = input("Write the number you choose: ")    
        if(number == '1'):
            print("creating a new Subject:")
            subject = input ("Enter the subject name: ")
            classroom = Classroom(subject)
            subjects.append(classroom)
            print('Subject created!')
        elif(number == '2'):
            print("creating a new Student:")
            name= input ("Enter the first name: ")
            surname = input ("Enter the last name: ")
            student_number = input ("Enter the student's number: ")
            student = Student(name, surname, student_number)
            students.append(student)
            print('Student created!')
           
        elif(number == '3'):
            print('Adding a Student to a Class')
            subject_name = input ("Enter the class: ")
            found = False
            for s in subjects:
                if(s.subject ==subject_name):
                    found = True
                    subject = s
            if(found):
                student_number = input ("Enter the student's number: ")
                found_student = False
                for st in students:
                    if(st.student_number == student_number):
                        found_student = True
                        student = st
                if(found_student):
                    subject.addStudentToClass(student.name,student.surname,student.student_number)
                    print(str(student.name)+' was added to '+str(subject.subject)+'!')
                else:
                    print('That student does not exist!')
            else:
                print ('That subject does not exist!')
        elif(number == '4'):
            print('Adding a grade of a Student in a Class')
            subject_name = input ("Enter the class: ")
            found = False
            for s in subjects:
                if(s.subject ==subject_name):
                    found = True
                    subject = s
            if(found):
                student_number = input ("Enter the student's number: ")
                found_student = False
                for st in students:
                    if(st.student_number == student_number):
                        found_student = True
                        #student = st
                fount_Student_inClass = False
                for studentInSubject in subject.list_students:
                    if(studentInSubject.student_number == student_number):
                        fount_Student_inClass = True
                if(found_student and fount_Student_inClass):
                    grade = input ("Enter the student's grade: ")
                    subject.addGrade(student_number, grade)
                    print('Grade added!')
                else:
                    print('That student does not exist or it is not in this class!')
            else:
                print ('That subject does not exist!')
        elif(number == '5'):
            print('Adding +1 attendance of a Student in a Class')
            subject_name = input ("Enter the class: ")
            found = False
            for s in subjects:
                if(s.subject ==subject_name):
                    found = True
                    subject = s
            if(found):
                student_number = input ("Enter the student's number: ")
                found_student = False
                for st in students:
                    if(st.student_number == student_number):
                        found_student = True
                        #student = st
                fount_Student_inClass = False
                for studentInSubject in subject.list_students:
                    if(studentInSubject.student_number == student_number):
                        fount_Student_inClass = True
                if(found_student and fount_Student_inClass):
                    subject.addAttendance(student_number)
                    print('Attendance added!')
                else:
                    print('That student does not exist or it is not in this class!')
            else:
                print ('That subject does not exist!')
         
        elif(number == '6'):
            print('Checking the average Grade of a Class')
            subject_name = input ("Enter the class: ")
            found = False
            for s in subjects:
                if(s.subject ==subject_name):
                    found = True
                    subject = s
            if(found):
                classAverage = subject.classAverage()
                print ('The class Average is '+ str(classAverage))
            else:
                print ('That subject does not exist!')
        elif(number == '7'):
            print('Checking the average Grade of a Student')
            student_number = input ("Enter the student's number: ")
            found_student = False
            for st in students:
                if(st.student_number == student_number):
                    found_student = True
                    student = st
            if(found_student):
                found_subject = False
                fount_Student_inClass = False
                avg = 0
                count = 0
                for s in subjects:
                    if(s.subject ==subject_name):
                        found_subject = True
                        subject = s
                    for studentInSubject in subject.list_students:
                        if(studentInSubject.student_number == student_number):
                            fount_Student_inClass = True
                    if(found_subject and fount_Student_inClass):
                        count += 1
                        avg += subject.students_info[student_number]['average : ']
                if(found_subject and fount_Student_inClass):
                    result = avg / count                    
                    print ('The student Average grade is '+ str(result))
                else:
                    print('Student not in class')
            else:
                print ('That student does not exist!')
        elif(number == '8'):
            print('Checking the average Grade of a Student in a Class')
            subject_name = input ("Enter the class: ")
            found = False
            for s in subjects:
                if(s.subject ==subject_name):
                    found = True
                    subject = s
            if(found):
                student_number = input ("Enter the student's number: ")
                found_student = False
                for st in students:
                    if(st.student_number == student_number):
                        found_student = True
                        student = st
                fount_Student_inClass = False
                for studentInSubject in subject.list_students:
                    if(studentInSubject.student_number == student_number):
                        fount_Student_inClass = True
                if(found_student and fount_Student_inClass):
                    avg = subject.students_info[student.student_number]['average : ']
                    print('The student Average grade in '+str(subject_name) +' is ' + str(avg))
                else:
                    print('That student does not exist!')
            else:
                print ('That subject does not exist!')
        elif(number == '9'):
            print('Checking the Attendance of a Student')
            student_number = input ("Enter the student's number: ")
            found_student = False
            for st in students:
                if(st.student_number == student_number):
                    found_student = True
                    student = st
            if(found_student):
                found_subject = False
                fount_Student_inClass = False
                count = 0
                for s in subjects:
                    if(s.subject ==subject_name):
                        found_subject = True
                        subject = s
                    for studentInSubject in subject.list_students:
                        if(studentInSubject.student_number == student_number):
                            fount_Student_inClass = True
                    if(found_subject and fount_Student_inClass):
                        count += subject.students_info[student_number]['attendance : ']
                print('The student attendance is ' + str(count))
            else:
                print('That student does not exist!')
        elif(number == '10'):
            print('Checking the Attendance of a Student in a Class')
            subject_name = input ("Enter the class: ")
            found = False
            for s in subjects:
                if(s.subject ==subject_name):
                    found = True
                    subject = s
            if(found):
                student_number = input ("Enter the student's number: ")
                found_student = False
                for st in students:
                    if(st.student_number == student_number):
                        found_student = True
                        student = st
                fount_Student_inClass = False
                for studentInSubject in subject.list_students:
                    if(studentInSubject.student_number == student_number):
                        fount_Student_inClass = True
                if(found_student and fount_Student_inClass):
                    at = subject.students_info[student.student_number]['attendance : ']
                    print('The student attendance in '+str(subject_name) +' is ' + str(at))
                else:
                    print('That student does not exist!')
            else:
                print ('That subject does not exist!')
        elif(number == '11'):
            print('Checking how many Students have a positive grade in a Class')
            subject_name = input ("Enter the class: ")
            found = False
            for s in subjects:
                if(s.subject ==subject_name):
                    found = True
                    subject = s
            if(found):
                nPositive = subject.numberPositiveAverage()
                nTotal = len(subject.list_students)
                print('There is '+ str(nPositive)+' positive grades in '+ str(nTotal) +' students.')
            else:
                print ('That subject does not exist!')
        elif(number == '0'):
            keepGoing = False
   
    
    data = {}  
    data['students'] = []  
    for studentInfo in students:
        data['students'].append({  
            'name': studentInfo.name,
            'surname': studentInfo.surname,
            'student number': studentInfo.student_number
        })
        
    data['classroom'] = []  
    for subjectInfo in subjects:
        data['classroom'].append({  
            'subject name': subjectInfo.subject
        })
    
    with open('data.txt', 'w') as outfile:  
        json.dump(data, outfile)
            

if __name__== "__main__":
    main()
	