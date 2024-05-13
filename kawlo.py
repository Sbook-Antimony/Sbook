template = "https://cameroongcerevision.com/cameroon-gce-%s-june-%d-%s-%d/"
saveTemplate = "questions/cameroon-gce-%s-june-%d-%s-%d.txt"
levels = ("a-level", "o-level")
years = reversed(range(2020, 2024))
subjects = ("biology",)
papers = (1,)


def get_mcq(txt):
	begin = txt.rindex("<div class=\"entry-content\">")
	end = txt.index("<p><div class=\"uk-cover-container\">")
	if -1 in (begin, end):
		return None
	return txt[begin:end]
import requests

for level in levels:
	print(f"level {level}")
	for year in years:
		print(f"  year {year}")
		for subject in subjects:
			print(f"    subject {subject}")
			for paper in papers:
				print("      paper: {paper}")
				try:
					print("        loading page..."+template%(level, year, subject, paper))
					page = requests.get(template%(level, year, subject, paper))
					if not "200" in str(page):
						print(page)
						raise TypeError("        could not get page")

					print("        ...finished")
					text = page.text
					text = get_mcq(text)
					print(f"        got mcq {type(text)}")
					if text is not None:
						open(saveTemplate%(level, year, subject, paper), "w", encoding="utf-8").write(text)
						print("        finished writting")
				except Exception as e:
					print(f"        ERROR: {e}")