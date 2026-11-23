Fictional UPI Fraud Forensic Training Case

University
training
exercise
 
Entirely
fictional
data

Case ID: UPI-FOR-2026-017
Case title: Operation Split Ledger
Location: Gwalior, Madhya Pradesh, India
Difficulty: Intermediate
Topics: Digital forensics, WhatsApp evidence, call-detail analysis, EXIF metadata, timeline reconstruction, mule-account investigation.

Scenario: A university cybercrime investigation team is examining a suspected UPI fraud involving a mule account. A fraudulent transfer of ₹48,500 was received and subsequently divided into smaller transfers. Investigators suspect that someone instructed the mule to delete the transaction record from their phone. A photograph recovered from the mule's device may help establish their location.

All people, numbers, transactions, coordinates, and communications below are invented for educational use. Phone numbers are fictional and begin with the requested +91-5 prefix.

1. Suspect profiles

Name

	

Role

	

Description




Aarav Sharma

	

Mule account holder

	

Received the disputed UPI transfer




Kabir Mehta

	

Main suspect

	

Allegedly coordinated the transfer




Riya Verma

	

Possible accomplice

	

Handled communication and logistics




Dev Malhotra

	

Wrong suspect

	

Friend of Aarav; appears suspicious but may be uninvolved

2. WhatsApp-style group chat export

Group: Payment Support Team
Participants: Aarav, Kabir, Riya, Dev
Recovered file: WhatsApp_Group_Export.txt
Date range: 18 November 2026

text
[18/11/2026 09:02] Aarav: Bhai account mein payment aa gaya hai.
[18/11/2026 09:04] Kabir: Kitna amount receive hua?
[18/11/2026 09:05] Aarav: 48,500 rupaye.
[18/11/2026 09:07] Riya: Transaction ID ka screenshot save kar lena.
[18/11/2026 09:09] Dev: Bhai mujhe bhi pending payment ka issue hai.
[18/11/2026 09:11] Aarav: Bank app mein credit show ho raha hai.
[18/11/2026 09:13] Kabir: Abhi kisi ko details forward mat karna.
[18/11/2026 09:16] Riya: Screenshot gallery mein rakhna, chat mein nahi.
[18/11/2026 09:19] Aarav: Amount ka kya karna hai?
[18/11/2026 09:21] Kabir: Instructions call par dunga.
[18/11/2026 09:24] Dev: Main toh abhi college ke paas hoon.
[18/11/2026 09:27] Aarav: Kabir bhai ka call aaya tha.
[18/11/2026 09:29] Kabir: Purana transfer record delete kar do, aur screenshot bhi hata do.
[18/11/2026 09:31] Aarav: Confirm? Record delete karna hai?
[18/11/2026 09:32] Kabir: Haan, transfer history ka screenshot bhi delete karna.
[18/11/2026 09:35] Riya: Aarav, phone mein original photo rehne dena.
[18/11/2026 09:39] Aarav: Samajh gaya. Screenshot remove kar diya.
[18/11/2026 09:42] Dev: Kya hua bhai? Itne calls kyun aa rahe hain?
[18/11/2026 09:45] Kabir: Is topic par group mein aur discussion mat karo.
[18/11/2026 10:02] Aarav: Main abhi bahar ja raha hoon.
[18/11/2026 10:14] Riya: Location wali photo bhejna mat bhoolna.
[18/11/2026 10:18] Aarav: Photo click kar li hai.
[18/11/2026 10:22] Dev: Main toh ghar ja raha hoon, mujhe kuch nahi pata.
[18/11/2026 10:26] Aarav: Photo original file mein saved hai.
[18/11/2026 10:30] Kabir: Theek hai, baad mein baat karte hain.
3. Call log (CSV)

Recovered file: Call_Log.csv

csv
row,datetime,direction,number,contact_name,duration_s
1,2026-11-18 09:20:10,IN,+91-5000000101,Kabir Mehta,142
2,2026-11-18 09:26:42,IN,+91-5000000101,Kabir Mehta,96
3,2026-11-18 09:38:05,OUT,+91-5000000102,Riya Verma,58
4,2026-11-18 09:43:17,IN,+91-5000000103,Dev Malhotra,35
5,2026-11-18 10:05:22,IN,+91-5000000102,Riya Verma,112
6,2026-11-18 10:24:50,OUT,+91-5000000101,Kabir Mehta,73

Analytical note: The call log establishes communication events, but does not independently establish what was said during the calls.

4. Recovered photograph: EXIF metadata

File: IMG_20261118_101800.jpg
Device owner: Aarav Sharma
Recovery source: Mobile-device image directory

EXIF extraction report

Field

	

Extracted value




File name

	

IMG_20261118_101800.jpg




DateTimeOriginal

	

2026:11:18 10:18:00




GPSLatitude

	

26°13′48.0″ N




GPSLongitude

	

78°10′48.0″ E




GPSLatitudeRef

	

N




GPSLongitudeRef

	

E




Camera model

	

Fictional Android Device X




Image format

	

JPEG

Coordinates converted to decimal degrees: 26.230000, 78.180000.

 

Illustrative scene only; this is not the recovered photograph and is not evidence of the actual location.

5. Candidate locations

Investigators have identified three candidate locations in Gwalior.

Candidate

	

Place

	

Latitude

	

Longitude




A

	

Gwalior Railway Station

	

26.2155

	

78.1775




B

	

Maharaj Bada

	

26.2038

	

78.1574




C

	

Phool Bagh

	

26.2300

	

78.1800

Candidate locations in Gwalior
Reset view
Expand map
4.0
Gwalior Railway Station
4.7
Maharaj Bada
4.3
Phool Bagh
© Mapbox © OpenStreetMap Improve this map
Gwalior Railway Station
★ 4 · Railway services
Open
Maharaj Bada
★ 4.7 · Museum
Phool Bagh
★ 4.3 · Park

Important: The candidate coordinates are fictionalized training data. The EXIF coordinates are deliberately aligned with one candidate to allow students to practice location correlation.

6. Student investigation questions

Submit your answers with supporting evidence.

Who instructed Aarav to delete the UPI transfer record? Identify the person and cite the relevant WhatsApp message.

When was the instruction given? Identify the exact date and time. Correlate the WhatsApp export with the call log.

Where was the mule (Aarav) when the photograph was taken? Identify the correct candidate location using DateTimeOriginal and GPS coordinates.

Additional challenge

Which suspect is a plausible but potentially incorrect lead?

Does the call log independently prove that Kabir instructed Aarav to delete the record?

Why should investigators preserve the original photograph rather than rely solely on a screenshot?

7. Answer key (instructor use)
Instructor reference
Answer 1: Who instructed the deletion?

Kabir Mehta.

Evidence:

Chat line 13: Kabir tells Aarav to delete the old transfer record and screenshot.

Chat line 14: Aarav asks for confirmation.

Chat line 15: Kabir explicitly confirms that the transfer-history screenshot should also be deleted.

Call-log row 2: Incoming call from Kabir at 09:26:42, lasting 96 seconds.

Call-log row 1: Earlier incoming call from Kabir at 09:20:10, lasting 142 seconds.

The messages and calls together support the conclusion that Kabir was directing Aarav.

Answer 2: When was the instruction given?

18 November 2026, at 09:29 AM.

Evidence:

Chat line 13 — 09:29: Kabir gives the deletion instruction.

Chat line 14 — 09:31: Aarav asks for confirmation.

Chat line 15 — 09:32: Kabir confirms the instruction.

Call-log row 2 — 09:26:42: Incoming call from Kabir shortly before the written instruction.

The call is useful contextual evidence, while the chat provides the exact written instruction time.

Answer 3: Where was the mule when the photograph was taken?
Correct answer: Candidate C

Phool Bagh, Gwalior, Madhya Pradesh.

Evidence:

Chat line 22: Aarav reports taking the photograph at 10:18.

EXIF DateTimeOriginal: 2026:11:18 10:18:00.

EXIF GPS: 26.230000, 78.180000.

Candidate C coordinates: 26.2300, 78.1800.

The coordinates match Candidate C exactly in this fictional exercise.

Answer key evidence matrix

Finding

	

Chat evidence

	

Call-log evidence

	

Other evidence




Deletion instruction by Kabir

	

Lines 13–15

	

Rows 1, 2

	

—




Instruction time

	

Lines 13–15

	

Row 2

	

—




Photograph location

	

Line 22

	

—

	

EXIF + Candidate C

Plausible wrong suspect: Dev Malhotra

Dev is a deliberately misleading suspect.

Reasons students might initially suspect him:

Chat line 9: He discusses a pending payment issue.

Chat line 12: He says he is near the college.

Chat line 19: He asks why so many calls are occurring.

Chat line 23: He claims he knows nothing about the incident.

Call-log row 4: He calls Aarav at 09:43:17.

However, the available evidence does not show Dev instructing Aarav to delete the transaction record. Kabir's written messages provide the direct evidence of that instruction.

8. Suggested university assessment rubric

Assessment criterion

	

Marks




Correct suspect identification

	

2




Correct instruction timestamp

	

2




Correct EXIF interpretation

	

2




Chat and call-log correlation

	

2




Distinguishing evidence from assumptions

	

2




Total

	

10

9. Instructor discussion: forensic limitations

Students should understand the following:

WhatsApp evidence: A displayed sender and timestamp are not, by themselves, proof of message authenticity. Investigators should preserve the original device and corroborate exported records.

Call logs: A call record establishes that a call was logged, not its spoken contents.

EXIF metadata: GPS and timestamps can be altered. They should be corroborated against other evidence.

Location inference: A coordinate match supports a candidate location but does not conclusively establish who held the device.

Evidence preservation: Original files, forensic hashes, acquisition records, and chain-of-custody documentation are important.

Teaching takeaway: Strong digital forensic conclusions come from correlating independent evidence sources, identifying inconsistencies, and distinguishing what the evidence proves from what it merely suggests.
