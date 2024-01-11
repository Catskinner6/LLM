# My changes to ChatGPT code for Google Scholar query
# Looks up all papers that cited Ulrich
# 	Scott Rice
# 		 Began: 	2023-12-07
# Last Updated:		2023-12-12

import Pkg
Pkg.add("HTTP")
Pkg.add("Gumbo")
Pkg.add("CSV")
Pkg.add("Cascadia")
Pkg.add("DataFrames")

using HTTP
using Gumbo
using CSV
using Cascadia
using DataFrames

url = "https://scholar.google.com/scholar?cites=570960603430622329&as_sdt=5,45&sciodt=0,45&hl=en";
results = HTTP.get(url);

body = String(results.body);
html = parsehtml(body);

# Extract publication titles and DOIs
titles = eachmatch(sel"h3[class='gs_rt']", html.root)
dois = eachmatch(sel"a.gs_or_cit", html.root)
authors = eachmatch(sel"h3[class='gs_a']", html.root)

# Extract text content from matched nodes
titles = [strip(string(title)) for title in titles]
dois = [strip(string(doi)) for doi in dois]
authors = [strip(string(author)) for author in authors]

# Create a list of tuples with titles and DOIs
publications = zip(titles, dois, authors)

# Save to CSV File    
csv_filename = "Citing_Ulrich1995"
CSV.write(csv_filename, publications, header=["Title", "DOI", "Authors"])

# URL for papers citing Ulrich's
google_scholar_url = "https://scholar.google.com/scholar?cites=570960603430622329&as_sdt=5,45&sciodt=0,45&hl=en"

# Scrape publications
publications = scrape_google_scholar(google_scholar_url)

# Specify the CSV filename
csv_filename = "publications_citing_ulrich.csv"

# Save titles and DOIs to a CSV file
save_to_csv(publications, csv_filename)
