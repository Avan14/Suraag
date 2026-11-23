Fictional UPI Fraud Forensic Training Case

University
training
simulation
 
100%
fictional
data

Case ID: UPI-FOR-2026-017
Case title: Operation Digital Breadcrumb
Location: Gwalior, Madhya Pradesh, India
Investigation type: Digital forensics, timeline reconstruction, communication analysis and geolocation correlation.

1. Case background

On 19 November 2026, a university student's bank account was used as a mule account in a suspected UPI fraud involving ₹48,500.

The victim was persuaded to transfer money to an account controlled by a suspected intermediary. Shortly after the transfer, members of a WhatsApp group discussed deleting transaction evidence.

Investigators recovered:

A WhatsApp-style group chat export.

A six-entry telephone call log.

One photograph with EXIF metadata.

Three candidate locations where the suspected mule might have been present.

The objective is to reconstruct the incident and identify the person who instructed the deletion of the transfer record.

All names, telephone numbers, transactions, coordinates and communications below are invented for educational purposes.

2. WhatsApp-style group chat export

Group: QuickPay Support Team
Participants:

Aarav Sharma — suspected mule account holder

Rohan Verma — primary suspect

Neha Soni — operations coordinator

Kabir Jain — secondary suspect / plausible wrong suspect

WhatsApp Group Export

25 messages

19 November 2026 · All timestamps IST (UTC+5:30)

01

Aarav

09:02

Bhai payment abhi tak confirm nahi hua.

02

Rohan

09:04

Customer ko bolo thoda wait kare.

03

Neha

09:07

Account details verify ho gayi hain.

04

Aarav

09:11

UPI pe ₹48,500 receive ho gaye.

05

Kabir

09:12

Nice. Screenshot group mein bhej do.

06

Aarav

09:14

Screenshot bhej diya.

07

Rohan

09:16

Transaction ID note kar lena.

08

Neha

09:19

Bank notification bhi aa gaya kya?

09

Aarav

09:21

Haan, SMS aa gaya hai.

10

Kabir

09:24

Mere phone mein bhi similar notification aaya tha kal.

11

Rohan

09:28

Aarav, abhi location share mat karna.

12

Aarav

09:32

Main station side ja raha hoon.

13

Neha

09:37

Transfer record phone mein save hai?

14

Aarav

09:40

Haan, screenshot gallery mein hai.

15

Kabir

09:43

Bhai, mujhe lagta hai record rakhna chahiye.

16

Rohan

09:46

Nahi, transfer ka screenshot delete kar do. Chat mein bhi uska reference mat rakho.

17

Aarav

09:48

Theek hai, delete kar raha hoon.

18

Neha

09:51

Deletion ke baad confirm kar dena.

19

Aarav

10:03

Screenshot delete kar diya.

20

Kabir

10:07

Maine toh kuch delete nahi kiya.

21

Rohan

10:12

Aaj shaam ko milte hain.

22

Aarav

10:18

Photo bhej raha hoon, location samajh aa jayegi.

23

Aarav

10:19

Yeh photo abhi ki hai.

24

Neha

10:23

Photo ka original file sambhal ke rakhna.

25

Rohan

10:29

Group mein transaction details dobara discuss mat karna.

3. Telephone call log (CSV)

Evidence ID: CALL-01
Source: Recovered handset call-history database
Date: 19 November 2026

csv
row,datetime,direction,number,contact_name,duration_s
1,2026-11-19 09:05:12,OUTGOING,+91-5000001001,Rohan Verma,86
2,2026-11-19 09:15:40,INCOMING,+91-5000001002,Neha Soni,124
3,2026-11-19 09:35:18,INCOMING,+91-5000001001,Rohan Verma,203
4,2026-11-19 09:44:02,OUTGOING,+91-5000001003,Kabir Jain,48
5,2026-11-19 09:50:11,INCOMING,+91-5000001002,Neha Soni,67
6,2026-11-19 10:15:33,OUTGOING,+91-5000001001,Rohan Verma,112

Investigative observation: The third call occurred shortly before the instruction to delete the transfer screenshot (chat line 16). The call log does not contain call recordings or establish what was said.

4. Photo EXIF metadata

Evidence ID: IMG-01
Filename: IMG_20261119_1019.jpg
Description: Photograph allegedly submitted by Aarav in the group.

Extracted EXIF fields

Simulated metadata

Field

	

Extracted value




File name

	

IMG_20261119_1019.jpg




DateTimeOriginal

	

2026:11:19 10:19:42




GPSLatitude

	

26° 12′ 42.0″ N




GPSLongitude

	

78° 10′ 48.0″ E




GPSLatitudeRef

	

N




GPSLongitudeRef

	

E




Time zone assumption

	

IST (UTC+5:30)




Device owner

	

Aarav Sharma (alleged)

Forensic note: EXIF timestamps and GPS fields are user-modifiable. Treat them as investigative leads, not independently verified proof of the photographer's location.

5. Candidate locations

Investigators have identified three possible locations in Gwalior for comparison against the photograph's coordinates.

 

Candidate A — Gwalior Railway Station

26.2045° N, 78.1745° E

Public transport hub.

 

Candidate B — Phool Bagh

26.2120° N, 78.1800° E

Public garden and nearby civic area.

 

Candidate C — Maharaj Bada

26.2120° N, 78.1700° E

Central commercial area.

Candidate locations and photo coordinates
Reset view
Expand map
4.0
Candidate A — Gwalior Railway Station
4.8
Candidate B — Phool Bagh
4.7
Candidate C — Maharaj Bada
© Mapbox © OpenStreetMap Improve this map
Candidate A — Gwalior Railway Station
★ 4 · Railway services
Open
Candidate B — Phool Bagh
★ 4.8 · Vegetarian restaurant
Candidate C — Maharaj Bada
★ 4.7 · Museum
EXIF coordinate
Mental health service
6. Investigation questions

Students should answer these questions using only the supplied evidence.

1. Who instructed Aarav to delete the transfer record? Identify the person and the exact chat line supporting your conclusion.

2. When was the deletion instruction given? Identify the date and time, and correlate it with the telephone call log.

3. Where was the mule (Aarav) when the photograph was taken? Identify the matching candidate location using the EXIF coordinates and explain your reasoning.

Additional critical-thinking question

Kabir appears suspicious because he asked for the transaction screenshot (line 05) and was involved in a call shortly before the deletion instruction.

Could Kabir be the person responsible? Explain why suspicion alone is insufficient to establish responsibility.

7. Answer key — Instructor edition
Suggested findings
Answer 1: Who instructed deletion?

Finding: Rohan Verma.

Evidence:

Chat line 16, 19 November 2026, 09:46: Rohan explicitly instructs Aarav to delete the transfer screenshot and avoid retaining its reference in the chat.

Chat line 17, 09:48: Aarav acknowledges the instruction.

Chat line 19, 10:03: Aarav confirms that the screenshot was deleted.

Supporting evidence: Chat lines 16, 17 and 19.

Answer 2: When was the deletion instruction given?

Finding: 19 November 2026 at 09:46 IST.

Call-log correlation:

Evidence

	

Time

	

Significance




Call-log row 3

	

09:35:18

	

Incoming call from Rohan, lasting 203 seconds




Chat line 16

	

09:46

	

Rohan issues deletion instruction




Chat line 17

	

09:48

	

Aarav acknowledges




Call-log row 5

	

09:50:11

	

Incoming call from Neha, lasting 67 seconds




Chat line 19

	

10:03

	

Aarav confirms deletion

The call from Rohan ended approximately at 09:38:41, around seven minutes before the explicit deletion instruction.

Important limitation: The call log establishes communication timing, not the content of the call. It cannot independently prove that Rohan discussed deletion during the call.

Answer 3: Where was Aarav when the photograph was taken?

Finding: Phool Bagh — Candidate B.

EXIF coordinates:

Latitude: 26° 12′ 42.0″ N = 26.211667° N

Longitude: 78° 10′ 48.0″ E = 78.180000° E

Comparison:

Candidate

	

Coordinates

	

Approximate distance from EXIF




A — Railway Station

	

26.2045, 78.1745

	

0.94 km




B — Phool Bagh

	

26.2120, 78.1800

	

37 m




C — Maharaj Bada

	

26.2120, 78.1700

	

1.0 km

Closest match: Candidate B

The EXIF coordinate is approximately 37 metres from the supplied Phool Bagh candidate coordinate.

Supporting evidence:

Chat line 22: Aarav says he is sending a photograph.

Chat line 23: Aarav says the photograph is current.

EXIF DateTimeOriginal: 10:19:42 on 19 November 2026.

Candidate B coordinate comparison.

Forensic qualification: This supports Phool Bagh as the closest candidate location, but does not prove that Aarav physically took the photograph there. Independent location evidence would be needed.

8. Suspect assessment

Person

	

Investigative role

	

Assessment




Rohan Verma

	

Primary suspect

	

Directly instructed deletion in line 16




Neha Soni

	

Operations coordinator

	

Asked about saved records and confirmed deletion




Kabir Jain

	

Plausible wrong suspect

	

Requested screenshot and contacted Aarav, but no direct deletion instruction is shown




Aarav Sharma

	

Mule account holder

	

Received funds and acknowledged deletion

Why Kabir is a plausible wrong suspect

Kabir appears suspicious because:

He requests the screenshot in line 05.

He makes a comment about transaction notifications in line 10.

He calls Aarav at 09:44:02 (call-log row 4).

He explicitly says he has not deleted anything in line 20.

However, the available evidence does not show Kabir instructing Aarav to delete the transfer record. Rohan is directly identified in line 16.

9. Suggested university marking rubric

Total: 20 marks

Assessment criterion

	

Marks




Correctly identifies Rohan

	

4




Cites exact chat line numbers

	

3




Correctly reconstructs deletion timeline

	

4




Correlates call-log rows

	

3




Converts EXIF coordinates correctly

	

2




Identifies Phool Bagh

	

2




Explains why Kabir is not conclusively implicated

	

2




Total

	

20

10. Discussion points for students

Can a WhatsApp export alone establish that a message is authentic?

What additional forensic checks would help establish whether EXIF metadata was manipulated?

Why should investigators distinguish between a call occurring before an instruction and proof that the instruction was communicated during that call?

What is the difference between being a mule account holder and being the person directing a fraud?

How should investigators preserve deleted transaction evidence while maintaining chain of custody?

Instructor's takeaway: The strongest conclusion comes from combining independent evidence sources while clearly distinguishing direct evidence, circumstantial evidence and unverified metadata. The exercise is designed to teach evidence correlation, not to treat a suspicious timeline as automatic proof of criminal responsibility.
