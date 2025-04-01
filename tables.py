
# %%
from dataclasses import dataclass
from typing import List

@dataclass
class Field:
    name: str
    type: str
    length: int
    primary_key: bool

@dataclass
class Table:
    name: str
    columns: List[Field]

def create_table(table: Table):
    tb1 = table
    
    cols = ','.join([f"{col.name} {col.type}\n" for col in tb1.columns])
    primary_key = ','.join([col.name for col in tb1.columns if col.primary_key])
    primary_key_str = f",primary key({primary_key})" if primary_key else ""
    script= f"CREATE TABLE {tb1.name} (\n {cols} {primary_key_str}  \n )" 
    
    return script 

def insert_script(table_name:str, fields: List[Field], data: List[str]):
    flds=[] #[f.name for f in fields]
    vals=[]
    for idx, d in enumerate(data):
        val = f"'{d}'"
        if d:
            if fields[idx].type.lower() == "date":
                val = f"DATE '{d}'"
            vals.append(val)
            flds.append(fields[idx].name)

    cols = ",\n".join(flds)
    values = ",\n".join(vals)
    script = f"insert into {table_name} ( \n {cols} )\n values (\n {values} )"

    return script

def update_script(table_name:str, fields: List[Field], data: List[str]):
    vals=[]
    wheres=[]
    for idx, d in enumerate(data):
        
        fld = fields[idx]
        fld_type = fld.type.lower() 
        fld_name = fld.name
        
        if not fld.primary_key:
            dd = f"'{d}'" if d else 'NULL'
            # val = f"{fld_name} = '{d}'"
            val = f"{fld_name} = {dd}"
            if fld_type  == "date":
                dd = f"DATE '{d}'" if d else 'NULL'
                # val = f"{fld_name} = DATE '{d}'"
                val = f"{fld_name} = {dd}"
            vals.append(val)
        else:        
            where = f"{fld_name} = '{d}'"
            wheres.append(where)
    
    set_values = ",\n".join(vals)
    where_condition = "and \n".join(wheres)
    script = f"update {table_name} set \n {set_values} \n where {where_condition}"

    return script
    

def get_table(table_name: str):
    for tb in table_list:
        if tb.name.lower() == table_name.lower():
            return tb
    
    return None

def list_tables():
    tb_list = [tb.name for tb in table_list]
    return tb_list


table_list= []

test_tb_fields = [ Field(name="col1",type="varchar(100)", length=100, primary_key=False),
               Field(name="col2",type="varchar(10)", length=10, primary_key=True),
               Field(name="col3",type="Number(5,2)", length=10, primary_key=True),     
               Field(name="col4",type="Date", length=23, primary_key=False) 
             ]

TEST_TABLE = Table(name="test_table", columns=test_tb_fields)


student_fields = [
    Field(name="STUDENT_NUMBER",type="NUMBER", length=39, primary_key=True)
    ,Field(name="STUDENT_NAME",type="VARCHAR(255)", length=255, primary_key=False)
    ,Field(name="SIN",type="NUMBER", length=39, primary_key=False)
    ,Field(name="DOB",type="DATE", length=23, primary_key=False)
    ,Field(name="STUDENT_EMAIL",type="VARCHAR(255)", length=255, primary_key=False)
    ,Field(name="UNIVERSITY",type="VARCHAR(255)", length=255, primary_key=False)
]
STUDENT = Table(name="student", columns=student_fields)

university_fields = [
    Field(name="UNIVERSITY_NAME",type="VARCHAR(255)", length=255, primary_key=True)
    ,Field(name="ADDRESS",type="VARCHAR(255)", length=255, primary_key=False)
    ,Field(name="PHONE_NUMBER",type="VARCHAR(20)", length=20, primary_key=False)
    ,Field(name="UNIVERSITY_EMAIL",type="VARCHAR(255)", length=255, primary_key=False)
]
UNIVERSITY = Table(name="university", columns=university_fields)

ta_field = [
    Field(name="TA_ID",type="NUMBER", length=39, primary_key=True)
    ,Field(name="TA_NAME",type="VARCHAR(255)", length=255, primary_key=False)
    ,Field(name="TA_EMAIL",type="VARCHAR(255)", length=255, primary_key=False)
    ,Field(name="PROFESSOR",type="NUMBER", length=39, primary_key=False)
]

TEACHING_ASSISTANT = Table(name="teaching_assistant", columns=ta_field)

st_fee_fields = [
    Field(name="STUDENT_NUMBER",type="NUMBER", length=39, primary_key=True)
    ,Field(name="FEES",type="NUMBER", length=14, primary_key=False)
] 

STUDENT_FEES = Table(name="student_fees", columns=st_fee_fields)

section_fields = [ 
    Field(name="SECTION_NUMBER",type="NUMBER", length=39, primary_key=False)
    ,Field(name="OPEN_SLOTS",type="NUMBER", length=39, primary_key=False)
    ,Field(name="TA",type="NUMBER", length=39, primary_key=False)
]
SECTION = Table(name="section", columns=section_fields)

prof_fields = [
    Field(name="PROFESSOR_ID",type="NUMBER", length=39, primary_key=True)
    ,Field(name="PROFESSOR_NAME",type="VARCHAR", length=255, primary_key=False)
    ,Field(name="PROFESSOR_EMAIL",type="VARCHAR", length=255, primary_key=False)
    ,Field(name="UNIVERSITY",type="VARCHAR", length=255, primary_key=False)
]
PROFESSOR = Table(name="professor", columns=prof_fields)

prereq_fields = [
    Field(name="PREREQUSITE_ID",type="VARCHAR", length=255, primary_key=False)
    ,Field(name="COURSE_ID",type="VARCHAR", length=255, primary_key=False)
]

PREREQUISITE = Table(name="prerequisite", columns=prereq_fields)

course_taken_fields= [
    Field(name="RECORD_ID",type="NUMBER", length=39, primary_key=True)
    ,Field(name="GPA",type="NUMBER", length=14, primary_key=False)
    ,Field(name="ENROLL_DATE",type="DATE", length=23, primary_key=False)
    ,Field(name="DROP_DATE",type="DATE", length=23, primary_key=False)
    ,Field(name="COURSE_CODE",type="VARCHAR", length=255, primary_key=False)
    ,Field(name="STUDENT_NUMBER",type="NUMBER", length=39, primary_key=False)
]
COURSE_TAKEN = Table ( name="course_taken", columns=course_taken_fields)

course_fields = [ 
    Field(name="COURSE_CODE",type="VARCHAR", length=255, primary_key=True)
    ,Field(name="COURSE_NAME",type="VARCHAR", length=255, primary_key=False)
    ,Field(name="COORDINATOR",type="NUMBER", length=39, primary_key=False)
    ,Field(name="FEE",type="NUMBER", length=14, primary_key=False)
    ,Field(name="NUM_STUDENTS",type="NUMBER", length=39, primary_key=False)
    ,Field(name="CREDIT",type="NUMBER", length=9, primary_key=False)
    ,Field(name="TERM",type="VARCHAR", length=255, primary_key=False)
]
COURSE = Table(name="course", columns=course_fields)

advisor_fields = [ 
    Field(name="PROGRAM",type="VARCHAR", length=255, primary_key=False)
    ,Field(name="ADVISOR_ID",type="NUMBER", length=39, primary_key=True)
    ,Field(name="ADVISOR_NAME",type="VARCHAR", length=255, primary_key=False)
]

ADVISOR = Table(name ="advisor", columns=advisor_fields)

acd_status_flields = [ 
    Field(name="STUDENT_NUMBER",type="NUMBER", length=39, primary_key=True)
    ,Field(name="STUDY_YEAR",type="NUMBER", length=39, primary_key=False)
    ,Field(name="GPA",type="NUMBER", length=14, primary_key=False)
    ,Field(name="CREDITS_EARNED",type="NUMBER", length=14, primary_key=False)
]

ACADEMIC_STATUS = Table(name="academic_status", columns=acd_status_flields)

acd_rec_fields = [
    Field(name="RECORD_ID",type="NUMBER", length=39, primary_key=True)
    ,Field(name="STUDY_YEAR",type="NUMBER", length=39, primary_key=False)
    ,Field(name="GPA",type="NUMBER", length=14, primary_key=False)
    ,Field(name="CREDITS_EARNED",type="NUMBER", length=14, primary_key=False)
    ,Field(name="FEES",type="NUMBER", length=14, primary_key=False)
    ,Field(name="STUDENT_NUMBER",type="NUMBER", length=39, primary_key=False)
]
ACADEMIC_RECORDS = Table(name="academic_records", columns=acd_rec_fields)

table_list.append(TEST_TABLE)
table_list.append(STUDENT)
table_list.append(UNIVERSITY)
table_list.append(TEACHING_ASSISTANT)
table_list.append(SECTION)
table_list.append(PROFESSOR)
table_list.append(PREREQUISITE)
table_list.append(COURSE_TAKEN)
table_list.append(COURSE)
table_list.append(ADVISOR)
table_list.append(ACADEMIC_STATUS)
table_list.append(STUDENT_FEES)
# table_list.append(ACADEMIC_RECORDS)

