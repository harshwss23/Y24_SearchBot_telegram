import pandas as pd
df = pd.read_csv('chut.csv')
# print(df.head())
print(df["Personal Data"][0])
Roll=[]
Name=[]
Blood_Grourp=[]
Email_id=[]
Department=[]
Hall=[]
Room=[]
PD=df["Personal Data"][0].split('\n')
print(PD[2].split(": ")[1])
OD=df["Other details"][0].split('\n')

print(OD[0].split(":")[1]+" "+OD[1])
# OD[2].split(":")[1][-1]=0
print(OD[2].split(":")[1].split(',')[0])
print(OD[2].split(":")[1].split(',')[1].split(')')[0])

for i in range(0,1216):
    try:
        PD=df["Personal Data"][i].split('\n')
        OD=df["Other details"][i].split('\n')
        Roll.append(PD[0])
        Name.append(PD[1])
        Blood_Grourp.append(PD[2].split(": ")[1])
        Email_id.append(PD[3].split(":")[1])
        Department.append(OD[1].split(':')[1].split(')')[0]+', '+OD[0].split(":")[1])
        Hall.append(OD[2].split(":")[1].split(',')[0])
        Room.append(OD[2].split(":")[1].split(',')[1].split(')')[0])
    except:
        print(i)
Data={"Roll No.": Roll, "Name": Name, "Blood Group": Blood_Grourp, "Email": Email_id, "Department": Department, "Hall": Hall,"Room": Room}
df=pd.DataFrame(Data)
df.to_csv("final.csv", index=False)

