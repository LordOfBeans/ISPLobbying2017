import urllib.request
import urllib.parse
import json
import csv

def reg_data(reg_id, year):
	params = {
		"registrant_id":reg_id,
		"contribution_type":"feca",
		"filing_year":year
	}
	query = query = urllib.parse.urlencode(params)
	req = urllib.request.Request("https://lda.senate.gov/api/v1/contributions/?" + query)
	with urllib.request.urlopen(req) as resp:
		data = json.loads(resp.read())
	return data

recipient_dict = {}
registrant_dict = {}

def add_cont(rec_dict, reg_dict, payee, group, amount, honoree):
	if payee in rec_dict:
		rec_dict[payee]["total"] += float(amount)
		if group in rec_dict[payee]["cont"]:
			rec_dict[payee]["cont"][group] += float(amount)
		else:
			rec_dict[payee]["cont"][group] = float(amount)
	else:
		rec_dict[payee] = {"honoree":honoree, "total": float(amount),"cont":{group:float(amount)}}
	if group in reg_dict:
		reg_dict[group] += float(amount)
	else:
		reg_dict[group] = float(amount)


def add_conts(rec_dict, reg_dict, group, reg_id, year):
	data = reg_data(reg_id, year)
	for i in data["results"]:
		for j in i["contribution_items"]:
			if j["contribution_type"] == "feca":
				add_cont(rec_dict, reg_dict, j["payee_name"], group, j["amount"], j["honoree_name"])

def build_csv(rec_dict, reg_dict, num):
	node_fields = ["id", "Group", "Size"]
	edge_fields = ["Source", "Target", "Value"]
	sort_total = sorted(rec_dict.items(), key = lambda x: x[1]["total"], reverse = True)
	node_list = []
	edge_list = []
	for k in reg_dict.items():
		node_list.append([k[0], 'ISP', k[1]])
	for i in range(num):
		rec = sort_total[i]
		node_list.append([rec[0], '', rec[1]["total"]])
		for j in rec[1]["cont"].items():
			edge_list.append([j[0], rec[0], j[1]])
	with open("nodes.csv", "w") as nodecsv:
		csvwriter = csv.writer(nodecsv)
		csvwriter.writerow(node_fields)
		csvwriter.writerows(node_list)
	with open("edges.csv", "w") as edgecsv:
		csvwriter = csv.writer(edgecsv)
		csvwriter.writerow(edge_fields)
		csvwriter.writerows(edge_list)

def get_rec(pac):
	print(recipient_dict[pac])
		
add_conts(recipient_dict, registrant_dict,  "AT&T", 34455, 2017)
add_conts(recipient_dict, registrant_dict, "Verizon", 5836, 2017)
add_conts(recipient_dict, registrant_dict, "Comcast", 10057, 2017)
add_conts(recipient_dict, registrant_dict, "Sprint", 36388, 2017)
add_conts(recipient_dict, registrant_dict, "Cox Enterprises", 11231, 2017)
add_conts(recipient_dict, registrant_dict, "Windstream", 316376, 2017)
add_conts(recipient_dict, registrant_dict, "TDS Telecom", 37653, 2017)
add_conts(recipient_dict, registrant_dict, "Lumen Technologies", 400859523, 2017)
add_conts(recipient_dict, registrant_dict, "Charter Communications", 59056, 2017)

#build_csv(recipient_dict, registrant_dict, 100)

	