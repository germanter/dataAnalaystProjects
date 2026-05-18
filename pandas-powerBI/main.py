import pandas as pd
import numpy as np
import keyw as src

dat = pd.read_csv("mess.csv")
# print(dat.columns)
# Index(['index', 'Job Title', 'Salary Estimate', 'Job Description', 'Rating',
#        'Company Name', 'Location', 'Headquarters', 'Size', 'Founded',
#        'Type of ownership', 'Industry', 'Sector', 'Revenue', 'Competitors'],
#       dtype='str')


dat = dat.replace([-1,"-1"], np.nan)
dat["Salary Estimate"] = dat["Salary Estimate"].str.replace("(Glassdoor est.)","",regex=False).str.strip()
dat["Salary Estimate"] = dat["Salary Estimate"].str.replace("(Employer est.)","",regex=False).str.strip()
minmaxSalary = dat["Salary Estimate"].str.replace("$","").str.replace("K","").str.split("-",expand=True)
dat["Minimum Salary ($)"] = minmaxSalary[0].astype('float64') * 1000
dat["Maximum Salary ($)"] = minmaxSalary[1].astype('float64') * 1000
dat["Job Title"] = dat["Job Title"].str.replace(" - SAN ANTONIO OR","",regex=False).str.strip()
dat["Job Title"] = dat["Job Title"].str.replace(" -SAN ANTONIO OR","",regex=False).str.strip()


dat["Skills"] = dat["Job Description"].apply(src.kw_match).astype(str)
dat["Size"] = dat["Size"].str.replace(" ",'').str.replace("to","-").str.replace("employees","").str.strip()
dat["Company Name"] = dat["Company Name"].str.replace(r'\n.*','',regex = True).str.strip()



dat["Location"] = dat["Location"].str.replace(r',.*','',regex=True).str.strip()
dat["Headquarters"] = dat["Headquarters"].str.replace(r',.*','',regex=True).str.strip()
dat["Revenue"] = dat["Revenue"].replace("Unknown / Non-Applicable",np.nan).str.strip()
dat["Revenue"] = dat["Revenue"].str.replace("to","-").str.replace(" - ","-").str.replace("(USD)","").str.replace("$","").str.strip()
dat = dat.rename(columns = {"Revenue":"Revenue (USD)","Size":"Size (Employees)"})
dat["Size (Employees)"] = "'" + dat["Size (Employees)"].astype(str)
dat = dat.drop_duplicates()

dat["Job Title"] = dat["Job Title"].apply(src.jt_stizer)
dat = dat.dropna(subset={"Job Title"})
dat = dat.drop(columns=["Job Description","Salary Estimate","Competitors"])
dat["index"] = range(0,dat.shape[0])

dat.to_csv("clean.csv", encoding = 'utf-8-sig', index=False)





