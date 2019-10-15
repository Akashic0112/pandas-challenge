#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Dependencies and Setup
import pandas as pd

# File to Load (Remember to Change These)
##csv= structured data
##DF- any time you create a table with pd's
# Read School and Student Data File and store into Pandas Data Frames
school_data = pd.read_csv("schools_complete.csv")
student_data = pd.read_csv("students_complete.csv")


# In[2]:


#verify your dfs came in correctly

student_data.head()
#student_data.columns


# In[3]:


school_data


# In[4]:


#Calculate number of total schools
#total_schools = len(school_data["school_name"].unique())
total_schools= len(school_data)
print(total_schools)


# In[5]:


#Calc total students
total_students = len(student_data)
print(total_students)
#verify:
#t_students = len(student_data["Student ID"].unique())
#print(t_students)


# In[6]:


#Calc total budget
total_budget = school_data["budget"].sum()
print(total_budget)


# In[7]:


avg_math_score = student_data["math_score"].mean()
print(avg_math_score)


# In[8]:


avg_reading_score = student_data["reading_score"].mean()
print(avg_reading_score)


# In[9]:


#Percent passing in math
#First call on df, then series(column), then apply filter to series
total_student_passing_math = len(student_data[student_data["math_score"] >= 70])
print(total_student_passing_math)
percent_total_student_passing_math = ((total_student_passing_math/total_students))*100
print(percent_total_student_passing_math)


# In[10]:


#percent passing reading
total_student_passing_reading = len(student_data[student_data["reading_score"] >= 70])
print(total_student_passing_reading)
percent_total_student_passing_reading = ((total_student_passing_reading/total_students))*100
print(percent_total_student_passing_reading)


# In[11]:


#Calculate the overall passing rate (overall average score), i.e. (avg. math score + avg. reading score)/2
overall_passing_rate= (percent_total_student_passing_reading+percent_total_student_passing_math)/2
print(overall_passing_rate)


# In[12]:


#District Summary Snapshot/table
district_summary = pd.DataFrame({
                        "Total Schools" : [total_schools],
                        "Total Students" : [total_students],
                        "Total Budget" : [total_budget],
                        "Average Math Score" : [avg_math_score],
                        "Avereage Reading Score" : [avg_reading_score],
                        "% Passing Math" : [percent_total_student_passing_math],
                        "% Passing Reading" : [percent_total_student_passing_reading],
                        "Overall Passing Rate" : [overall_passing_rate]

})
district_summary


# In[13]:


#Make it pretty


# ## School Summary

# In[14]:


#School Summary
#Common column = school_name
#Combine the data into a single dataset
merged_data = pd.merge(student_data, school_data, how="left", on=["school_name", "school_name"])
merged_data.head()


# In[15]:


#School names
school_names = school_data.set_index(["school_name"])["type"]


# In[16]:


total_students_per_school = merged_data.groupby(["school_name"]).count()["Student ID"]
total_students_per_school
#type(total_students_per_school)


# In[17]:


total_budget_per_school= merged_data.groupby(["school_name"]).mean()["budget"]
total_budget_per_school


# In[18]:


avg_budget_per_student= (total_budget_per_school/total_students_per_school)
print(avg_budget_per_student)


# In[19]:


#average math score
avg_math_score_school=merged_data.groupby(["school_name"]).mean()["math_score"]
avg_math_score_school


# In[20]:


#average reading score
avg_reading_score_school = merged_data.groupby(["school_name"]).mean()["math_score"]
avg_reading_score_school


# In[21]:


#Percent students passing math per school...
passing_students_math = merged_data[merged_data["math_score"]>=70]

passing_students_math.info()


# In[22]:


passing_students_math_per_school= passing_students_math.groupby(["school_name"]).count()["Student ID"]
percent_passing_students_math_per_school= (passing_students_math_per_school/total_students_per_school)*100
percent_passing_students_math_per_school


# In[23]:


passing_students_reading = merged_data[merged_data["reading_score"]>=70]
passing_students_reading_per_school= passing_students_reading.groupby(["school_name"]).count()["Student ID"]
percent_passing_reading_per_school = (passing_students_reading_per_school/total_students_per_school)*100
len(percent_passing_reading_per_school)


# In[24]:


#Percent passing per school
percent_passing_students_per_school= (percent_passing_students_math_per_school + percent_total_student_passing_reading)
overall_passing_rate= percent_passing_students_per_school/2
overall_passing_rate
print(len(overall_passing_rate))


# In[25]:


#school summary
school_summary = pd.DataFrame({
                    "School Type" : school_names,
                    "Total Students" : total_students_per_school, 
                    "Per Student Budget" : avg_budget_per_student,
                    "Average Math Score" : avg_math_score_school,
                    "Average Reading Score" : avg_reading_score_school,
                    "% Passing Math" : percent_total_student_passing_math,
                    "% Passing Reading" : percent_total_student_passing_reading,
                    "Overall Passing Rate" : overall_passing_rate

})
school_summary.head()


# In[26]:


#Make it Pretty :)

school_summary["Per Student Budget"] = school_summary["Per Student Budget"].map("${:.2f}".format)
school_summary["Average Math Score"] = school_summary["Average Math Score"].map("{:.2f}".format)
school_summary["Average Reading Score"] = school_summary["Average Reading Score"].map("{:.2f}".format)
school_summary["% Passing Math"] = school_summary["% Passing Math"].map("{:.2f}".format)
school_summary["% Passing Reading"] = school_summary["% Passing Reading"].map("{:.2f}".format)
school_summary["Overall Passing Rate"] = school_summary["Overall Passing Rate"].map("{:.2f}".format)


school_summary


# ## Top Performing Schools (By Passing Rate)

# * Sort and display the top five schools in overall passing rate

# In[27]:


#school_summary.info()
topschool_df = school_summary.sort_values(by=['Overall Passing Rate'], ascending=False)
topschool_df.head()


# ## Bottom Performing Schools (By Passing Rate)

# * Sort and display the five worst-performing schools

# In[28]:


lowestschool_df = school_summary.sort_values(by=['Overall Passing Rate'], ascending=True)
lowestschool_df.head()


# ## Math Scores by Grade

# * Create a table that lists the average Reading Score for students of each grade level (9th, 10th, 11th, 12th) at each school.
# 
#   * Create a pandas series for each grade. Hint: use a conditional statement.
#   
#   * Group each series by school
#   
#   * Combine the series into a dataframe
#   
#   * Optional: give the displayed data cleaner formatting

# In[29]:


merged_data.columns


# In[30]:


#New ds for each grade: 9,10,11,12(observ it's already sorted by school!)
ninth_grade = merged_data[(merged_data["grade"] == "9th")]
tenth_grade = merged_data[(merged_data["grade"] == "10th")]
elev_grade = merged_data[(merged_data["grade"] == "11th")]
twel_grade = merged_data[(merged_data["grade"] == "12th")]

#ninth_grade.head()


# In[31]:


#each by school MATH avg per grade
ninth_avg_school = ninth_grade.groupby(["school_name"]).mean()["math_score"]
#ninth_avg_school.head
tenth_avg_school = tenth_grade.groupby(["school_name"]).mean()["math_score"]
eleventh_avg_school = elev_grade.groupby(["school_name"]).mean()["math_score"]
twelfth_avg_school = twel_grade.groupby(["school_name"]).mean()["math_score"]


# In[32]:


#Combine into new df by grade
scores_bygrade_df = pd.DataFrame({
                                    "9th" : ninth_avg_school,
                                    "10th" : tenth_avg_school,
                                    "11th" : eleventh_avg_school,
                                    "12th" : twelfth_avg_school
})

#scores_bygrade_df.head()

#make it pretty :)
scores_bygrade_df.reset_index(inplace=True)
scores_bygrade_df["9th"] = scores_bygrade_df["9th"].map("{:.2f}".format)
scores_bygrade_df["10th"] = scores_bygrade_df["10th"].map("{:.2f}".format)
scores_bygrade_df["11th"] = scores_bygrade_df["11th"].map("{:.2f}".format)
scores_bygrade_df["12th"] = scores_bygrade_df["12th"].map("{:.2f}".format)

scores_bygrade_df.head()


# ## Reading Score by Grade 

# * Perform the same operations as above for reading scores

# In[33]:


#READING avg per grade
ninth_rdg_avg_school = ninth_grade.groupby(["school_name"]).mean()["reading_score"]
#ninth_avg_school.head
ninth_rdg_avg_school = tenth_grade.groupby(["school_name"]).mean()["reading_score"]
ninth_rdg_avg_school = elev_grade.groupby(["school_name"]).mean()["reading_score"]
twelfth_rdg_avg_school = twel_grade.groupby(["school_name"]).mean()["reading_score"]


# In[34]:


#New Reading score df
rdg_scores_bygrade = pd.DataFrame({
                                    "9th avg" : ninth_rdg_avg_school,
                                    "10th avg" : ninth_rdg_avg_school,
                                    "11th avg" : eleventh_avg_school,
                                    "12th avg" : ninth_rdg_avg_school})
##rdg_scores_bygrade.head()

# #make it pretty :)
rdg_scores_bygrade.reset_index(inplace=True)
rdg_scores_bygrade["9th avg"] = rdg_scores_bygrade["9th avg"].map("{:.2f}".format)
rdg_scores_bygrade["10th avg"] = rdg_scores_bygrade["10th avg"].map("{:.2f}".format)
rdg_scores_bygrade["11th avg"] = rdg_scores_bygrade["11th avg"].map("{:.2f}".format)
rdg_scores_bygrade["12th avg"] = rdg_scores_bygrade["12th avg"].map("{:.2f}".format)

rdg_scores_bygrade.head()


# ## Scores by School Spending

# * Create a table that breaks down school performances based on average Spending Ranges (Per Student). Use 4 reasonable bins to group school spending. Include in the table each of the following:
#   * Average Math Score
#   * Average Reading Score
#   * % Passing Math
#   * % Passing Reading
#   * Overall Passing Rate (Average of the above two)

# In[40]:


# Sample bins. Feel free to create your own bins.
##How did they come up with the sample bins?
spending_bins = [0, 585, 615, 645, 675]
group_names = ["<$585", "$585-615", "$615-645", "$645-675"]
school_summary.head()


# In[41]:


#Add new column to df for bin categories
school_summary["Spending amt/student"]= pd.cut(avg_budget_per_student, spending_bins, labels=group_names)
school_summary.info()


# In[44]:


#need to make numbers back into integers
cols = ['Average Math Score', 'Average Reading Score', '% Passing Math','% Passing Reading','Overall Passing Rate']
for col in cols:  # Iterate over chosen columns
    school_summary[col] = pd.to_numeric(school_summary[col])
    
school_summary.info()


# In[45]:


#Group by different parameters: 
# Average Math Score
perstuduent_avgmathscore = school_summary.groupby(["Spending amt/student"]).mean()["Average Math Score"]
 
# Average Reading Score
perstudent_avgrdgscore = school_summary.groupby(["Spending amt/student"]).mean()["Average Reading Score"]
 
# % Passing Math
perstudent_mathpass = school_summary.groupby(["Spending amt/student"]).mean()["% Passing Math"]

# % Passing Reading
perstudent_rdgpass = school_summary.groupby(["Spending amt/student"]).mean()["% Passing Reading"]

# Overall Passing Rate (Average of the above two)
perstudent_overallpass = (perstudent_mathpass + perstudent_rdgpass)/ 2



# In[46]:


#Create another df for per student school summary
perstudent_summary = pd.DataFrame({ 
                                    "Average Math Score" : perstuduent_avgmathscore,
                                 "Average Reading Score": perstudent_avgrdgscore,
                                 "% Passing Math": perstudent_mathpass,
                                 "% Passing Reading": perstudent_rdgpass,
                                 "% Overall Passing Rate": perstudent_overallpass})


perstudent_summary.head()


# ## Scores by School Size

# * Perform the same operations as above, based on school size.

# In[47]:


# Sample bins. Feel free to create your own bins.
size_bins = [0, 1000, 2000, 5000]
group_names = ["Small (<1000)", "Medium (1000-2000)", "Large (2000-5000)"]
school_summary.info()


# In[48]:


#Add new column with grouping info
school_summary["School Size"]= pd.cut(school_summary["Total Students"], size_bins, labels=group_names)
# school_summary.head()

#Group by different parameters: 
# Average Math Score
size_avgmathscore = school_summary.groupby(["School Size"]).mean()["Average Math Score"]
 
# Average Reading Score
size_avgrdgscore = school_summary.groupby(["School Size"]).mean()["Average Reading Score"]
 
# % Passing Math
size_mathpass = school_summary.groupby(["School Size"]).mean()["% Passing Math"]

# % Passing Reading
size_rdgpass = school_summary.groupby(["School Size"]).mean()["% Passing Reading"]

# Overall Passing Rate (Average of the above two)
size_overallpass = (size_mathpass + size_rdgpass)/ 2



# In[49]:


#Create ANOTHER Df with your new groupby info
size_summary = pd.DataFrame({
                                "Average Math Score" : size_avgmathscore,
                                 "Average Reading Score": size_avgrdgscore,
                                 "% Passing Math": size_mathpass,
                                 "% Passing Reading": size_rdgpass,
                                 "% Overall Passing Rate": size_overallpass})


size_summary.head()


# In[ ]:


school_summary.head()


# ## Scores by School Type

# * Perform the same operations as above, based on school type.

# In[50]:


#Lets group again...by Type: DISTRICT or CHARTER
type_math = school_summary.groupby(["School Type"]).mean()["Average Math Score"]
type_rdg = school_summary.groupby(["School Type"]).mean()["Average Reading Score"]
type_mathpass = school_summary.groupby(["School Type"]).mean()["% Passing Math"]
type_rdgpass = school_summary.groupby(["School Type"]).mean()["% Passing Reading"]
type_overall = (type_mathpass + type_rdgpass) / 2


# In[51]:


#Create one more df for types
type_summary = pd.DataFrame({
                                "Average Math Score" : type_math,
                                 "Average Reading Score": type_rdg,
                                 "% Passing Math": type_mathpass,
                                 "% Passing Reading": type_rdgpass,
                                 "% Overall Passing Rate": type_overall})

type_summary.head()


# In[ ]:





# In[ ]:




