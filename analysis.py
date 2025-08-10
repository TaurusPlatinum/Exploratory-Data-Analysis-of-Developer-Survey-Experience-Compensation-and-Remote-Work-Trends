import pandas as pd

df = pd.read_csv("survey_results_public.csv")
schema_df = pd.read_csv("survey_results_schema.csv")
schema_questions = set(schema_df["qname"].dropna())
questions_in_df = set(df.columns)
common_questions = schema_questions.intersection(questions_in_df)

# Identify common questions between schema and data
total_respondents = len(df)

# Number of respondents who answered all questions
df_complete = df.dropna(subset=common_questions)
complete_respondents = len(df_complete)

# Central tendency measures for professional coding experience (YearsCodePro)
df["YearsCodePro_num"] = pd.to_numeric(df["YearsCodePro"], errors='coerce')
mean_exp = df["YearsCodePro_num"].mean()
median_exp = df["YearsCodePro_num"].median()
mode_exp = df["YearsCodePro_num"].mode()

# Number of respondents working remotely
remote_workers = df["RemoteWork"].value_counts().get("Remote", 0)

# Percentage of respondents who code in Python
python_coders = df['LanguageHaveWorkedWith'].str.contains('Python', na=False).sum()
total_language_respondents = df['LanguageHaveWorkedWith'].dropna().shape[0]
percent_python = (python_coders / total_language_respondents) * 100 if total_language_respondents > 0 else 0

# Number of respondents who learned coding online (if column exists)
if 'LearnCodeOnline' in df.columns:
    learn_online_respondents = df['LearnCodeOnline'].dropna().str.contains("Online", case=False).sum()
else:
    learn_online_respondents = None

# Average and median compensation by country among Python programmers
df_python = df[df['LanguageHaveWorkedWith'].str.contains('Python', na=False)].copy()
df_python['ConvertedCompYearly_num'] = pd.to_numeric(df_python['ConvertedCompYearly'], errors='coerce')
comp_by_country = df_python.groupby('Country')['ConvertedCompYearly_num'].agg(['mean', 'median']).sort_values('mean', ascending=False)

# Education levels of top 5 highest compensated respondents
df["ConvertedCompYearly_num"] = pd.to_numeric(df["ConvertedCompYearly"], errors='coerce')
top5 = df.sort_values("ConvertedCompYearly_num", ascending=False).head(5)

# Percentage of Python programmers by age group
def python_percentage(group):
    total = group.shape[0]
    python_count = group["LanguageHaveWorkedWith"].str.contains('Python', na=False).sum()
    return (python_count / total) * 100 if total > 0 else 0
percent_by_age = df.groupby("Age").apply(python_percentage)
# Most common industries among high-paid remote workers (>= 75th percentile)
percentile_75 = df["ConvertedCompYearly_num"].quantile(0.75)
df_high_paid_remote = df[(df["ConvertedCompYearly_num"] >= percentile_75) & (df["RemoteWork"] == "Remote")]
industry_counts = df_high_paid_remote["DevType"].dropna().str.split(";").explode().value_counts()

print(f"1. Total respondents: {total_respondents}")
print(f"2. Respondents who answered all questions: {complete_respondents}")
print(f"3. Central tendency measures for professional coding experience (YearsCodePro):")
print(f"   Mean experience: {mean_exp:.2f}")
print(f"   Median experience: {median_exp}")
print(f"   Mode experience: {list(mode_exp)}")
print(f"4. Number of respondents working remotely: {remote_workers}")
print(f"5. Percentage of respondents who code in Python: {percent_python:.2f}%")
print(f"6. Number of respondents who learned coding online: {learn_online_respondents}")
print(f"7. Average and median compensation by country among Python programmers:\n{comp_by_country}")
print("8. Education levels of top 5 highest compensated respondents:")
print(top5.loc[:, ["ConvertedCompYearly_num", "EdLevel"]].to_string(index=False))
print(f"9. Percentage of Python programmers by age group:\n{percent_by_age}")
print(f"10. Most common industries among high-paid remote workers:\n{industry_counts.head(10)}")
