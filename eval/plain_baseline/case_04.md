University Forensic Training Case: Operation Split Ledger

Fictional
training
simulation
 
Intermediate
difficulty

Case ID: UPI-FOR-2026-017
Subject: Suspected UPI fraud, mule-account coordination, evidence deletion, and geolocation analysis
Jurisdiction: Gwalior, Madhya Pradesh, India
All names, phone numbers, transactions, locations, and evidence are fictional. Coordinates are synthetic and intended only for classroom analysis.

1. Case background

On 18 November 2026, a university student, Aarav Mehta, reported an unauthorized UPI transfer of ₹28,500.

The investigation identified a suspected mule account belonging to Rohan Saini. Investigators recovered:

A WhatsApp-style group chat export.

A six-entry call log.

One photograph recovered from the mule's phone.

Three candidate locations relevant to the investigation.

Investigators suspect that someone instructed Rohan to delete a transfer record after the transaction.

Investigation objective: Establish who gave the deletion instruction, when it was given, and where Rohan was when the photograph was captured.

2. WhatsApp group chat export

Group: UPI Help Desk – Private | Export recovered from Rohan's device

Participants:

Rohan Saini — suspected mule account holder

Neha Verma — group administrator

Kabir Malhotra — financial intermediary

Dev Arora — technical support contact (plausible wrong suspect)

WhatsApp Group Export

Recovered

18 November 2026 · All timestamps IST (UTC+5:30)

01

Neha

09:02

Guys, aaj ka settlement pending hai. Sab online rehna.

02

Rohan

09:04

Haan, mera account ready hai.

03

Dev

09:06

UPI app mein koi issue aaye toh mujhe batana.

04

Kabir

09:11

Rohan, account details confirm kar do.

05

Rohan

09:13

Account active hai. Payment receive ho sakta hai.

06

Neha

09:18

Transaction ka screenshot group mein mat bhejna.

07

Kabir

09:21

Client side se amount release hone wala hai.

08

Rohan

09:26

Notification aa gaya, ₹28,500 received.

09

Neha

09:27

Amount confirm kar, jaldi.

10

Rohan

09:29

Haan confirm hai. Balance update ho gaya.

11

Dev

09:31

Maine koi transfer initiate nahi kiya, FYI.

12

Kabir

09:34

Ab record ka screenshot phone se hata dena.

13

Rohan

09:36

Sirf screenshot ya transaction history bhi?

14

Kabir

09:38

Transfer record bhi delete kar dena. Samjha?

15

Neha

09:39

Rohan, pehle confirm karna ki paisa forward hua.

16

Rohan

09:43

Amount doosre account mein bhej diya.

17

Kabir

09:45

Good. Ab purani entry visible nahi honi chahiye.

18

Rohan

09:47

Theek hai, record remove kar raha hoon.

19

Dev

09:51

Mujhe is transaction ke baare mein kuch nahi pata.

20

Neha

10:02

Phone ki gallery mein bhi check kar lena.

21

Rohan

10:15

Ek photo location ke saath save hui hai.

22

Kabir

10:17

Us photo ko abhi touch mat karna.

23

Rohan

10:32

Main station ke paas hoon, baad mein call karta hoon.

24

Neha

10:35

Kabir ko call kar, woh details samjhayega.

25

Rohan

10:41

Okay, call kar raha hoon.

3. Call log (CSV)

Source: Simulated extraction from the mule's mobile device

csv
row,datetime,direction,number,contact_name,duration_s
1,2026-11-18 09:15:22,OUTGOING,+91-5000000101,Neha Verma,86
2,2026-11-18 09:30:10,INCOMING,+91-5000000102,Kabir Malhotra,142
3,2026-11-18 09:40:05,INCOMING,+91-5000000102,Kabir Malhotra,211
4,2026-11-18 09:55:41,INCOMING,+91-5000000103,Dev Arora,48
5,2026-11-18 10:20:17,OUTGOING,+91-5000000101,Neha Verma,73
6,2026-11-18 10:42:09,OUTGOING,+91-5000000102,Kabir Malhotra,195

Forensic observation: Kabir's two calls around the deletion instruction may be relevant. Dev also contacted Rohan, making him a plausible alternative suspect.

4. Recovered photograph: EXIF metadata
 

IMG_20261118_1018.jpg

Recovered from Rohan's phone gallery

EXIF present

Simulated metadata extraction:

text
FileName: IMG_20261118_1018.jpg
Make: Fictional Mobile Device
Model: F-Phone X2

DateTimeOriginal: 2026:11:18 10:18:36

GPSLatitude: 26.218400
GPSLatitudeRef: N

GPSLongitude: 78.182100
GPSLongitudeRef: E

GPSCoordinates: 26.218400, 78.182100

Evidence handling note: EXIF timestamps and coordinates are metadata claims, not independently verified proof of when and where a photograph was taken.

5. Candidate places

The investigation team has identified three possible locations in Gwalior.

 

A. Gwalior Railway Station

Candidate A

Coordinates: 26.218400, 78.182100

 

B. Gwalior Bus Stand

Candidate B

Coordinates: 26.203800, 78.157400

 

C. Phool Bagh

Candidate C

Coordinates: 26.202600, 78.173900

Candidate locations and recovered photo coordinates
Reset view
Expand map
📍
A. Gwalior Railway Station
📍
B. Gwalior Bus Stand
📍
C. Phool Bagh
© Mapbox © OpenStreetMap Improve this map
📍 A. Gwalior Railway Station
★ 4 · Railway services
Open
📍 B. Gwalior Bus Stand
★ 3.4 · Bus depot
Open
📍 C. Phool Bagh
★ 4.3 · Park
6. Questions for students

Question 1 — Attribution

Who instructed Rohan to delete the UPI transfer record?

Question 2 — Timeline reconstruction

At what exact date and time was the deletion instruction communicated? Identify the relevant chat evidence and supporting call-log entries.

Question 3 — Geolocation

Where was the mule, Rohan Saini, when the recovered photograph was taken?

Choose one:

A. Gwalior Railway Station

B. Gwalior Bus Stand

C. Phool Bagh

Additional challenge: Why might Dev Arora initially appear suspicious, and what evidence weakens the case against him?

7. Answer key — Instructor copy
Suggested answers
Answer 1: Kabir Malhotra

Primary evidence:

Chat line 12: Kabir says, "Ab record ka screenshot phone se hata dena."

Chat line 14: Kabir explicitly says, "Transfer record bhi delete kar dena."

Chat line 17: Kabir reinforces that the old entry should no longer be visible.

Corroborating call evidence:

Call-log row 2: Kabir called Rohan at 09:30:10 for 142 seconds.

Call-log row 3: Kabir called Rohan at 09:40:05 for 211 seconds.

The conversation and calls support the conclusion that Kabir instructed Rohan to delete the transfer record.

Answer 2: 18 November 2026, 09:38 IST

Exact instruction:

Chat line 12 — 09:34: initial instruction to remove the screenshot.

Chat line 13 — 09:36: Rohan asks whether transaction history should also be deleted.

Chat line 14 — 09:38: Kabir explicitly instructs him to delete the transfer record.

Chat line 17 — 09:45: Kabir reiterates that the old entry should not remain visible.

Chat line 18 — 09:47: Rohan acknowledges that he is removing the record.

Call-log corroboration:

Row

	

Time

	

Contact

	

Duration




2

	

09:30:10

	

Kabir

	

142 s




3

	

09:40:05

	

Kabir

	

211 s

The call log supports communication with Kabir around the relevant period, but does not independently establish the content of either call.

Answer 3: A. Gwalior Railway Station

The recovered photograph contains:

text
GPSLatitude:  26.218400 N
GPSLongitude: 78.182100 E
DateTimeOriginal: 2026:11:18 10:18:36

These coordinates exactly match Candidate A in the supplied dataset.

Therefore, the intended answer is Gwalior Railway Station.

8. Plausible wrong suspect analysis: Dev Arora

Dev is deliberately included as a misleading suspect.

Evidence

	

Interpretation




Chat line 3

	

Dev offers technical support




Chat line 11

	

Dev discusses the transaction




Call-log row 4

	

Dev calls Rohan at 09:55:41




Chat line 19

	

Dev denies knowledge of the transaction

Why Dev is a weaker suspect:

No recovered chat line explicitly instructs Rohan to delete the transfer record.

Kabir gives the direct instruction in lines 12 and 14.

Kabir's calls are temporally closer to the deletion discussion.

Important distinction: The absence of an explicit instruction from Dev does not prove that he had no involvement. It simply makes Kabir the better-supported attribution from this evidence set.

9. Instructor marking rubric

Suggested total: 20 marks

Assessment criterion

	

Marks




Correctly identifies Kabir

	

4




Cites chat lines 12 and 14

	

4




Reconstructs the 09:38 instruction time

	

4




Correctly interprets EXIF coordinates

	

4




Identifies Dev as a plausible alternative and evaluates evidence

	

4




Total

	

20

10. Discussion prompts

Can EXIF GPS data alone establish the physical presence of a suspect?

How could investigators establish whether the EXIF metadata was altered?

Does a call occurring near the time of an instruction prove that the instruction was communicated during that call?

What additional evidence would help establish the beneficiary account's ownership?

What is the difference between deleting a screenshot and deleting a bank transaction record?

Instructor note: This is a synthetic educational dataset, not a real criminal allegation or a verified forensic extraction. Students should distinguish direct evidence, corroborating evidence, metadata claims, and investigative inference.
