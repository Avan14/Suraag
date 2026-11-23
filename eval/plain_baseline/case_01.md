Fictional UPI-Fraud Forensic Training Case

SIMULATED
CASE
—
UNIVERSITY
TRAINING
ONLY
 
Intermediate
difficulty

Case ID: UPI-FOR-2026-017
Case title: The Deleted Transfer
Location: Gwalior, Madhya Pradesh, India
Incident date: 18 November 2026
Subject: Suspected UPI fraud, mule-account coordination, evidence deletion and location reconstruction.

All individuals, phone numbers, transactions, locations and evidence in this exercise are fictional. The coordinates are simulated training data and are not intended to identify real individuals.

1. Case background

A university cybercrime investigation team receives a complaint from a victim who allegedly lost ₹48,500 through a fraudulent UPI transaction.

The money was transferred into an account belonging to a suspected money mule, Rohan Verma.

Investigators recover:

A WhatsApp-style group chat export.

A six-entry call log.

An image recovered from the mule's phone.

Three candidate locations associated with the investigation.

The central questions are who ordered the deletion of the transfer record, when the instruction was issued, and where the mule was when the recovered photograph was taken.

2. Evidence A — WhatsApp group chat export

Group: UPI Support Team 🔐

Participants:

Rohan Verma — suspected mule

Aman Qureshi — suspected coordinator

Neha Sharma — account handler

Vikram Soni — secondary suspect

Export file: whatsapp_group_export.txt

text
01. [18-11-2026 09:02:11] Rohan: Bhai kal wala payment abhi tak settle nahi hua.
02. [18-11-2026 09:03:45] Aman: Tension mat le, account mein entry aa gayi hai.
03. [18-11-2026 09:05:18] Neha: Amount ₹48,500 tha na?
04. [18-11-2026 09:06:02] Rohan: Haan, screenshot mere phone mein hai.
05. [18-11-2026 09:08:31] Vikram: Mujhe bhi transaction ka detail bhej dena.
06. [18-11-2026 09:10:09] Aman: Vikram, tum is matter mein involve mat ho.
07. [18-11-2026 09:14:22] Rohan: Bank se confirmation SMS bhi aaya tha.
08. [18-11-2026 09:16:40] Neha: Screenshot group mein mat bhejna.
09. [18-11-2026 09:19:13] Vikram: Main toh bas help kar raha tha.
10. [18-11-2026 09:25:51] Aman: Rohan, kal ka transfer record phone se delete kar dena.
11. [18-11-2026 09:26:30] Rohan: Sirf screenshot ya poora record?
12. [18-11-2026 09:27:04] Aman: Dono. Backup bhi check kar lena.
13. [18-11-2026 09:31:17] Neha: Bhai ye sab risky lag raha hai.
14. [18-11-2026 09:33:52] Aman: Neha, tum bas apna kaam karo.
15. [18-11-2026 09:40:08] Rohan: Main abhi station side ja raha hoon.
16. [18-11-2026 09:44:29] Vikram: Kaunsa station?
17. [18-11-2026 09:46:03] Rohan: Gwalior Junction ke paas.
18. [18-11-2026 10:02:18] Neha: Photo bheji thi kya location ki?
19. [18-11-2026 10:04:47] Rohan: Haan, ek photo save hai gallery mein.
20. [18-11-2026 10:10:33] Aman: Kisi ko original file forward mat karna.
21. [18-11-2026 10:15:09] Vikram: Mujhe laga hum sirf normal payment help kar rahe hain.
22. [18-11-2026 10:18:55] Rohan: Ab mujhe bhi doubt ho raha hai.
23. [18-11-2026 10:23:41] Neha: Call pe baat karna, group mein nahi.
24. [18-11-2026 10:25:12] Aman: Rohan, meri call ka wait kar.
25. [18-11-2026 10:29:06] Rohan: Theek hai, main phone available rakhta hoon.
3. Evidence B — Call log CSV

Source: Recovered device call-history database
File: call_log.csv

All telephone numbers are fictional and begin with +91-5.

csv
row,datetime,direction,number,contact_name,duration_s
1,2026-11-18 09:20:14,INCOMING,+91-5123456701,Aman Qureshi,126
2,2026-11-18 09:28:42,OUTGOING,+91-5234567802,Neha Sharma,84
3,2026-11-18 09:48:10,INCOMING,+91-5123456701,Aman Qureshi,203
4,2026-11-18 10:06:35,OUTGOING,+91-5345678903,Vikram Soni,47
5,2026-11-18 10:21:08,INCOMING,+91-5123456701,Aman Qureshi,95
6,2026-11-18 10:31:52,OUTGOING,+91-5234567802,Neha Sharma,61
4. Evidence C — Recovered photograph EXIF metadata

File: IMG_20261118_095512.jpg

Image metadata report

EXIF recovered
 
File name	

IMG_20261118_095512.jpg


DateTimeOriginal	2026:11:18 09:55:12
GPSLatitude	26°13′55.2″ N
GPSLongitude	78°10′26.4″ E
GPSLatitudeRef	N
GPSLongitudeRef	E

Training metadata. The illustrative image is not the actual recovered photograph.

Decimal GPS conversion:

Latitude: 26.232000

Longitude: 78.174000

5. Evidence D — Candidate places

Investigators identify three possible locations based on the mule's chat messages and the EXIF coordinates.

Candidate A — Gwalior Junction Railway Station

 

26.232000° N, 78.174000° E

Match against recovered photograph GPS.

Candidate B — Gwalior Bus Stand

 

26.215800° N, 78.182400° E

Alternative transport location.

Candidate C — Phool Bagh

 

26.201900° N, 78.173500° E

Alternative public meeting location.

Candidate locations and recovered photo coordinates
Reset view
Expand map
📍
Candidate A — Gwalior Junction
📍
Candidate B — Gwalior Bus Stand
📍
Candidate C — Phool Bagh
© Mapbox © OpenStreetMap Improve this map
📍 Candidate A — Gwalior Junction
★ 4 · Railway services
Open
📍 Candidate B — Gwalior Bus Stand
★ 3.4 · Bus depot
Open
📍 Candidate C — Phool Bagh
★ 4.1 · Student dormitory
Open
6. Student investigation questions

Answer each question using at least two pieces of evidence where possible.

Question 1 — Who instructed Rohan to delete the transfer record?

Identify the person who explicitly gave the instruction. Distinguish between the person giving the instruction and other group members who may have been aware of it.

Question 2 — When was the deletion instruction issued?

Provide:

Exact date.

Exact time.

Supporting chat line number.

Relevant call-log evidence, if applicable.

Question 3 — Where was the mule when the photograph was taken?

Use:

EXIF DateTimeOriginal.

GPS coordinates.

Candidate location list.

Relevant WhatsApp messages.

Explain why the other two locations are less likely.

7. Answer key — Instructor edition
Correct answers and evidence correlations
Answer 1: Who instructed deletion?

Aman Qureshi.

Evidence:

Chat line 10: Aman explicitly instructs Rohan to delete the previous day's transfer record.

Chat line 11: Rohan asks whether only the screenshot or the complete record should be deleted.

Chat line 12: Aman clarifies that both should be deleted, including the backup.

Call-log row 1: Aman calls Rohan at 09:20:14, before the written instruction.

Call-log row 3: Aman calls Rohan again at 09:48:10.

The evidence identifies Aman as the person who explicitly issued the instruction.

Plausible wrong suspect: Vikram Soni.

Vikram appears suspicious because:

He asks for transaction details (line 5).

He asks about Rohan's location (line 16).

He contacts Rohan by phone (call-log row 4).

However, there is no explicit message showing Vikram instructing deletion.

Answer 2: When was the instruction issued?

18 November 2026 at 09:25:51.

Primary evidence:

Chat line 10 — timestamp 09:25:51: Aman tells Rohan to delete the transfer record.

Chat line 11 — timestamp 09:26:30: Rohan requests clarification.

Chat line 12 — timestamp 09:27:04: Aman confirms deletion of both the screenshot and record, including the backup.

Supporting call-log evidence:

Call-log row

	

Time

	

Person

	

Duration




1

	

09:20:14

	

Aman

	

126 seconds




3

	

09:48:10

	

Aman

	

203 seconds

The first call occurred before the instruction, and the second occurred afterward. These calls establish a communication timeline but do not independently prove what was discussed.

Answer 3: Where was Rohan when the photo was taken?
Candidate A

Gwalior Junction Railway Station.

Evidence:

EXIF DateTimeOriginal: 2026:11:18 09:55:12.

EXIF GPS: 26.232000° N, 78.174000° E.

Chat line 15: Rohan says he is heading towards the station.

Chat line 17: Rohan specifically identifies Gwalior Junction.

Chat line 19: Rohan confirms that a photograph is saved in his gallery.

The recovered coordinates match Candidate A exactly in this simulated dataset.

Candidates B and C have different coordinates, making them less consistent with the recorded EXIF metadata.

Important forensic qualification: EXIF metadata can be modified or inaccurate. The result establishes the photograph's recorded location, not necessarily the photographer's independently verified physical location. Device integrity, clock accuracy and metadata authenticity would need separate examination.

8. Evidence correlation summary

Investigation finding

	

Primary evidence

	

Supporting evidence




Deletion instruction issued by Aman

	

Chat 10, 12

	

Call rows 1, 3




Exact instruction time

	

Chat 10

	

Chat 11, 12




Photo recorded at Gwalior Junction

	

EXIF GPS

	

Chat 15, 17, 19




Potential alternative suspect

	

Chat 5, 16

	

Call row 4

9. Suggested university marking scheme

Total: 20 marks

Assessment criterion

	

Marks




Correct identification of instructor

	

4




Exact date and time of instruction

	

4




Correct chat-line citations

	

3




Correct call-log row interpretation

	

3




Correct location identification using GPS

	

4




Recognition of alternative suspect and evidence limitations

	

2




Total

	

20

10. Instructor discussion prompts

Can a WhatsApp message alone establish criminal intent?

Why should investigators correlate call logs with chat timestamps?

Can EXIF GPS metadata be treated as conclusive proof of someone's location?

What is the difference between a suspicious contact and a person directly issuing an instruction?

How should investigators preserve the original device and its forensic image?

Learning outcome: Students should learn to construct a defensible event timeline, correlate multiple digital evidence sources, distinguish direct evidence from circumstantial evidence, and avoid overstating forensic conclusions.
