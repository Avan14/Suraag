Fictional UPI Fraud Forensic Training Case

Fictional
university
exercise
 
Digital
forensics

Case ID: UPI-FOR-2026-017
Case title: Operation Silent Ledger
Location: Gwalior, Madhya Pradesh, India
Difficulty: Intermediate
Target audience: University students studying cybercrime investigation, digital forensics, and financial fraud.

All people, phone numbers, transactions, locations, and evidence in this exercise are fictional. Phone numbers use the requested fictional +91-5 prefix.

1. Case background

A university student, Aarav Mehta, reports that ₹48,500 was transferred from his UPI account after he received a fraudulent payment-verification request.

Investigators suspect a small group coordinated the fraud using WhatsApp, telephone calls, and a mule bank account.

The suspected participants are:

Name

	

Alleged role




Rohan Verma

	

Suspected fraud coordinator




Kunal Sharma

	

Suspected mule account holder




Neha Soni

	

Group member and possible intermediary




Vikram Patel

	

Payment agent; potential wrong suspect

Investigators have recovered:

A WhatsApp-style group chat export.

A mobile call log.

One photograph with EXIF metadata.

Three candidate geographical locations.

The objective is to reconstruct the events and identify the person who instructed the mule to delete the transfer record.

2. WhatsApp-style group chat export

Group: Payment Support Team
Exported date: 23 November 2026
Timezone: IST (UTC+05:30)

Fictional evidence artifact — 25 numbered messages

text
[01] 2026-11-21 18:02:11 - Rohan: Sab log online ho? Ek payment issue discuss karna hai.

[02] 2026-11-21 18:03:24 - Kunal: Haan bhai, bolo.

[03] 2026-11-21 18:04:02 - Neha: Main bhi online hoon.

[04] 2026-11-21 18:06:18 - Rohan: Kunal, account mein payment receive hui kya?

[05] 2026-11-21 18:07:43 - Kunal: Haan, 48,500 credit hua hai.

[06] 2026-11-21 18:08:15 - Vikram: Bhai amount kaafi bada hai.

[07] 2026-11-21 18:09:51 - Rohan: Abhi kisi ko details forward mat karna.

[08] 2026-11-21 18:12:09 - Kunal: Transaction notification ka screenshot save kiya hai.

[09] 2026-11-21 18:14:32 - Neha: Screenshot group mein mat bhejna.

[10] 2026-11-21 18:17:05 - Vikram: Main toh sirf payment status check kar raha tha.

[11] 2026-11-21 18:20:41 - Rohan: Kunal, phone pe baat karo. Important hai.

[12] 2026-11-21 18:22:06 - Kunal: Theek hai, call karta hoon.

[13] 2026-11-21 18:29:17 - Kunal: Call ho gayi. Samajh gaya.

[14] 2026-11-21 18:31:50 - Neha: Transfer ka record abhi bhi gallery mein hai kya?

[15] 2026-11-21 18:32:44 - Kunal: Haan, screenshot abhi phone mein pada hai.

[16] 2026-11-21 18:35:08 - Vikram: Maine toh kisi ko delete karne ko nahi bola.

[17] 2026-11-21 18:37:26 - Rohan: Kunal, woh transfer record delete kar do.
     Group mein bhi uska screenshot mat rakhna.

[18] 2026-11-21 18:39:12 - Kunal: Okay, delete kar diya.

[19] 2026-11-21 18:41:33 - Neha: Location wali photo mil gayi kya?

[20] 2026-11-21 18:42:05 - Kunal: Haan, ek photo li thi jab main bahar tha.

[21] 2026-11-21 18:43:18 - Rohan: Original photo sambhal ke rakhna.

[22] 2026-11-21 18:45:51 - Kunal: Original mere paas hai.

[23] 2026-11-21 19:02:07 - Vikram: Mujhe is payment ke baare mein aur kuch nahi pata.

[24] 2026-11-21 19:05:39 - Neha: Kal koi naya message mat bhejna.

[25] 2026-11-21 19:08:14 - Rohan: Sab log chat normal rakho. Koi unnecessary baat nahi.
3. Mobile call log (CSV)

Source device: Kunal Sharma's fictional Android phone
Timezone: IST

csv
row,datetime,direction,number,contact_name,duration_s
1,2026-11-21 17:55:12,INCOMING,+91-5000000101,Rohan Verma,84
2,2026-11-21 18:21:03,OUTGOING,+91-5000000101,Rohan Verma,312
3,2026-11-21 18:25:40,INCOMING,+91-5000000102,Neha Soni,46
4,2026-11-21 18:34:11,INCOMING,+91-5000000103,Vikram Patel,128
5,2026-11-21 18:46:52,OUTGOING,+91-5000000101,Rohan Verma,95
6,2026-11-22 09:15:06,INCOMING,+91-5000000102,Neha Soni,63

Investigative observation: Call-log row 2 occurred shortly before chat message 13. Row 5 occurred shortly after the discussion about the photograph.

4. Recovered photograph: EXIF metadata

Evidence ID: IMG-KS-004
Filename: IMG_20261121_184215.jpg
Device owner: Kunal Sharma

EXIF metadata

Recovered

Field

	

Recorded value




DateTimeOriginal

	

2026:11:21 18:42:15




GPSLatitude

	

26° 12′ 30.0″ N




GPSLongitude

	

78° 10′ 30.0″ E




GPSLatitudeRef

	

N




GPSLongitudeRef

	

E




Image filename

	

IMG_20261121_184215.jpg

The coordinates are fictional training coordinates and are not asserted to identify an actual business or property.

5. Candidate locations

Investigators have identified three fictional candidate places within the exercise's geographical dataset.

Candidate

	

Place name

	

Latitude

	

Longitude




A

	

Central Bus Stand

	

26.2000

	

78.1500




B

	

City Garden Entrance

	

26.2083

	

78.1750




C

	

Riverside Parking Area

	

26.1750

	

78.1300

Three candidate locations
Reset view
Expand map
4.2
Central Bus Stand
4.2
City Garden Entrance
5.0
Riverside Parking Area
© Mapbox © OpenStreetMap Improve this map
Central Bus Stand
★ 4.2 · Transportation service
City Garden Entrance
★ 4.2 · Housing society
Riverside Parking Area
★ 5 · Public parking space
Open

Student task: Compare the EXIF coordinates with the candidate coordinates. Use the timestamp to establish whether the photograph was taken before or after the relevant chat messages.

6. Questions for students

Question 1 — Attribution

Who explicitly instructed Kunal to delete the transfer record?

Question 2 — Timeline reconstruction

At what exact date and time was the deletion instruction given?

Question 3 — Geolocation

Where was the mule account holder when the photograph was taken?

Select one:

A. Central Bus Stand

B. City Garden Entrance

C. Riverside Parking Area

Additional investigative challenge: Why might Vikram Patel initially appear suspicious, and what evidence weakens the case against him?

7. Answer key
Instructor copy
Answer 1: Who instructed deletion?

Rohan Verma.

Evidence:

WhatsApp chat line 17 explicitly states: "Kunal, woh transfer record delete kar do."

Chat line 18 confirms Kunal acknowledged the deletion.

Call-log row 2 shows a 312-second outgoing call from Kunal to Rohan shortly before the discussion in chat line 13.

Conclusion: Rohan is the explicitly identifiable person giving the deletion instruction.

Answer 2: When was the instruction given?

21 November 2026 at 18:37:26 IST.

Evidence:

Evidence

	

Reference

	

Timestamp




Deletion instruction

	

Chat line 17

	

18:37:26




Deletion acknowledgement

	

Chat line 18

	

18:39:12




Earlier call with Rohan

	

Call row 2

	

18:21:03




Later call with Rohan

	

Call row 5

	

18:46:52

Conclusion: The instruction was sent at 18:37:26, and the acknowledgement followed 1 minute 46 seconds later.

Answer 3: Where was the mule?
Correct answer: B

City Garden Entrance — Candidate B (fictional exercise location).

EXIF coordinates:

Latitude: 26.208333° N

Longitude: 78.175000° E

Candidate B coordinates:

Latitude: 26.2083° N

Longitude: 78.1750° E

The values match to the precision supplied.

Timeline corroboration:

Chat line 19: 18:41:33 — Neha asks about the location photograph.

Chat line 20: 18:42:05 — Kunal confirms he took a photograph.

EXIF DateTimeOriginal: 18:42:15.

The EXIF timestamp is 10 seconds after chat line 20.

Conclusion: The photograph was taken at the fictional City Garden Entrance candidate location.

Answer 4: Plausible wrong suspect

Vikram Patel is the intended wrong suspect.

Why he appears suspicious:

Chat line 6: He comments on the large payment.

Chat line 10: He mentions checking payment status.

Chat line 16: He denies telling anyone to delete records.

Call-log row 4: He has a 128-second incoming call to Kunal at 18:34:11.

Why the evidence does not establish his responsibility:

Chat line 17 explicitly identifies Rohan as the person instructing deletion.

Call-log row 2 supports direct communication between Rohan and Kunal before the deletion discussion.

Vikram's call is not sufficient evidence that he gave the deletion instruction.

Important forensic distinction: A suspicious communication pattern does not independently prove responsibility.

8. Instructor marking rubric

Assessment criterion

	

Marks




Correctly identifies Rohan

	

3




Gives exact instruction timestamp

	

2




Correctly identifies Candidate B

	

3




Cites exact chat lines and call rows

	

3




Explains the wrong-suspect hypothesis

	

2




Distinguishes evidence from inference

	

2




Total

	

15

9. Discussion points for university students

Can a WhatsApp export alone establish that a message was sent by the account owner?

What additional forensic validation would be needed before relying on EXIF GPS metadata?

Can call duration establish what was discussed during a telephone conversation?

Why should investigators preserve original device data instead of relying only on screenshots?

What is the difference between an instruction, an acknowledgement, and proof that an action actually occurred?

Instructor's final note: This case deliberately includes a plausible wrong suspect, a short sequence of events, corroborating timestamps, and a geolocation matching exercise. The intended learning outcome is evidence correlation rather than simply identifying a suspicious person.
