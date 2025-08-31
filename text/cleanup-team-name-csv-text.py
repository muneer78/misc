import csv

input_lines = [
"Rank: 1, : Giants, Opponents' combined 2024 record: 166-123, Opponents' combined 2024 win percentage: .574",
"Rank: T-2, : Bears, Opponents' combined 2024 record: 165-124, Opponents' combined 2024 win percentage: .571",
"Rank: T-2, : Lions, Opponents' combined 2024 record: 165-124, Opponents' combined 2024 win percentage: .571",
"Rank: 4, : Eagles, Opponents' combined 2024 record: 162-127, Opponents' combined 2024 win percentage: .561",
"Rank: T-5, : Cowboys, Opponents' combined 2024 record: 161-128, Opponents' combined 2024 win percentage: .557",
"Rank: T-5, : Packers, Opponents' combined 2024 record: 161-128, Opponents' combined 2024 win percentage: .557",
"Rank: T-5, : Vikings, Opponents' combined 2024 record: 161-128, Opponents' combined 2024 win percentage: .557",
"Rank: 8., : Commanders, Opponents' combined 2024 record: 159-130, Opponents' combined 2024 win percentage: .550",
"Rank: 9., : Ravens, Opponents' combined 2024 record: 154-135, Opponents' combined 2024 win percentage: .533",
"Rank: 10., : Steelers, Opponents' combined 2024 record: 152-137, Opponents' combined 2024 win percentage: .526",
"Rank: T-11, : Chiefs, Opponents' combined 2024 record: 151-138, Opponents' combined 2024 win percentage: .522",
"Rank: T-11, : Chargers, Opponents' combined 2024 record: 151-138, Opponents' combined 2024 win percentage: .522",
"Rank: T-12, : Browns, Opponents' combined 2024 record: 150-139, Opponents' combined 2024 win percentage: .519",
"Rank: T-12, : Bengals, Opponents' combined 2024 record: 147-142, Opponents' combined 2024 win percentage: .509",
"Rank: T-12, : Broncos, Opponents' combined 2024 record: 146-143, Opponents' combined 2024 win percentage: .505",
"Rank: T-16, : Raiders, Opponents' combined 2024 record: 145-144, Opponents' combined 2024 win percentage: .502",
"Rank: T-16, : Rams, Opponents' combined 2024 record: 142-147, Opponents' combined 2024 win percentage: .491",
"Rank: T-16, : Texans, Opponents' combined 2024 record: 139-150, Opponents' combined 2024 win percentage: .481",
"Rank: T-16, : Buccaneers, Opponents' combined 2024 record: 139-150, Opponents' combined 2024 win percentage: .481",
"Rank: 20, : Falcons, Opponents' combined 2024 record: 138-151, Opponents' combined 2024 win percentage: .478",
"Rank: T-21, : Dolphins, Opponents' combined 2024 record: 137-152, Opponents' combined 2024 win percentage: .474",
"Rank: T-21, : Seahawks, Opponents' combined 2024 record: 137-152, Opponents' combined 2024 win percentage: .474",
"Rank: T-23, : Bills, Opponents' combined 2024 record: 135-154, Opponents' combined 2024 win percentage: .467",
"Rank: T-23, : Jaguars, Opponents' combined 2024 record: 135-154, Opponents' combined 2024 win percentage: .467",
"Rank: 25, : Colts, Opponents' combined 2024 record: 134-155, Opponents' combined 2024 win percentage: .464",
"Rank: 26, : Jets, Opponents' combined 2024 record: 133-156, Opponents' combined 2024 win percentage: .460",
"Rank: T-27, : Cardinals, Opponents' combined 2024 record: 132-157, Opponents' combined 2024 win percentage: .457",
"Rank: T-27, : Panthers, Opponents' combined 2024 record: 132-157, Opponents' combined 2024 win percentage: .457",
"Rank: 29, : Titans, Opponents' combined 2024 record: 130-159, Opponents' combined 2024 win percentage: .450",
"Rank: 30, : Patriots, Opponents' combined 2024 record: 124-165, Opponents' combined 2024 win percentage: .429",
"Rank: 31, : Saints, Opponents' combined 2024 record: 121-168, Opponents' combined 2024 win percentage: .419",
"Rank: 32, : 49ers, Opponents' combined 2024 record: 120-169, Opponents' combined 2024 win percentage: .415",
]

with open('/Users/muneer78/Downloads/output.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Rank', 'Team'])
    for idx, line in enumerate(input_lines, 1):
        team = line.split(':', 2)[2].split(',', 1)[0].strip()
        writer.writerow([idx, team])