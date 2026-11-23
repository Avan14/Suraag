University Forensic Training Case: Operation QR-Dhoka

Fictional
educational
case
 
UPI
fraud
investigation
 
Intermediate
difficulty

Case ID: UPI-2026-047
Location: Gwalior, Madhya Pradesh, India
Incident date: 18 November 2026
Investigation type: Digital forensics, timeline reconstruction, communication analysis and mule-account identification.

All people, phone numbers, transactions, locations and evidence in this exercise are fictional. The coordinates are illustrative training coordinates, not verified real-world suspect locations.

1. Case background

A university student, Aarav Mehta, reports that ₹18,500 was transferred from his UPI account after he received a WhatsApp message promising a university scholarship refund.

The money was transferred into a mule account allegedly operated by Rohan Saini.

Investigators recover:

A WhatsApp-style group chat export.

A six-entry mobile call log.

One photograph recovered from a device associated with the mule.

Three candidate locations.

The investigation team suspects that someone instructed the mule to delete the UPI transfer record before the transaction could be investigated.

There are four fictional persons of interest:

Person

	

Role




Rohan Saini

	

Suspected mule account holder




Kabir Verma

	

Group administrator and suspected coordinator




Neha Tomar

	

Group member, possible intermediary




Dev Malhotra

	

Group member and plausible wrong suspect

All telephone numbers below are fictional and use the requested +91-5 prefix.

2. Evidence A — WhatsApp-style group chat export

Group: Scholarship Help Desk 2026
Exported from: Recovered device belonging to Rohan Saini
Date: 18 November 2026

The following is a fictional reconstructed chat transcript.

text
[01] 18/11/2026 09:02 - Kabir: Good morning guys, refund ka kaam aaj complete karna hai.
[02] 18/11/2026 09:04 - Rohan: Haan bhai, mera account ready hai.
[03] 18/11/2026 09:07 - Neha: Student ko amount aur UPI ID bhej di hai.
[04] 18/11/2026 09:10 - Dev: Payment aane ke baad mujhe update kar dena.
[05] 18/11/2026 09:14 - Rohan: Abhi tak payment nahi aaya.
[06] 18/11/2026 09:18 - Kabir: Phone paas rakhna, notification miss mat karna.
[07] 18/11/2026 09:26 - Neha: Aarav ne bola transfer kar diya.
[08] 18/11/2026 09:28 - Rohan: Mere phone pe credit notification aa gaya.
[09] 18/11/2026 09:29 - Dev: Screenshot bhejo, confirmation dekhna hai.
[10] 18/11/2026 09:31 - Rohan: ₹18,500 received show ho raha hai.
[11] 18/11/2026 09:33 - Kabir: Transaction ID ka screenshot kisi ko forward mat karna.
[12] 18/11/2026 09:36 - Neha: Ab next step kya hai?
[13] 18/11/2026 09:39 - Rohan: Bank app mein entry dikh rahi hai.
[14] 18/11/2026 09:42 - Dev: Bhai, mujhe ismein mat ghaseetna. Main sirf update pooch raha tha.
[15] 18/11/2026 09:46 - Kabir: Rohan, transfer record delete kar do. Gallery aur chat mein bhi screenshot mat rehne dena.
[16] 18/11/2026 09:48 - Rohan: Theek hai, abhi kar deta hoon.
[17] 18/11/2026 09:51 - Neha: Call pe baat kar lo, group mein details mat likho.
[18] 18/11/2026 09:54 - Kabir: Rohan, old bus stand side pahunch kar message karna.
[19] 18/11/2026 10:03 - Rohan: Main nikal gaya hoon.
[20] 18/11/2026 10:17 - Rohan: Photo bhej raha hoon, location confirm kar lo.
[21] 18/11/2026 10:18 - Neha: Background mein bus stand ka board dikh raha hai kya?
[22] 18/11/2026 10:19 - Rohan: Haan, photo mein board visible hai.
[23] 18/11/2026 10:24 - Dev: Main toh college mein hoon, mujhe location ka kuch nahi pata.
[24] 18/11/2026 10:31 - Kabir: Phone silent rakho aur group se abhi exit mat karna.
[25] 18/11/2026 10:38 - Rohan: Photo aur original payment screenshot alag folder mein the.
3. Evidence B — Mobile call log

Source: Recovered device associated with Rohan Saini.

CSV export:

csv
row,datetime,direction,number,contact_name,duration_s
1,2026-11-18 09:20:14,IN,+91-5123400011,Kabir Verma,84
2,2026-11-18 09:34:05,IN,+91-5123400011,Kabir Verma,126
3,2026-11-18 09:44:32,OUT,+91-5987600022,Neha Tomar,53
4,2026-11-18 09:50:11,IN,+91-5123400011,Kabir Verma,112
5,2026-11-18 10:12:40,OUT,+91-5987600022,Neha Tomar,67
6,2026-11-18 10:26:03,IN,+91-5345600033,Dev Malhotra,39

Investigator's note:

Kabir called Rohan three times.

The third Kabir call occurred shortly before the instruction to delete the transfer record.

Neha also communicated with Rohan, making her a potential intermediary.

Dev's call occurred after the photograph was sent.

Call timing alone does not establish the content of any conversation.

4. Evidence C — Recovered photograph EXIF metadata

Filename: IMG_20261118_101722.jpg

Extracted EXIF fields

Metadata recovered

Field

	

Value




DateTimeOriginal

	

2026:11:18 10:17:22




GPSLatitude

	

26°13'12.0"N




GPSLatitudeRef

	

N




GPSLongitude

	

78°10'48.0"E




GPSLongitudeRef

	

E




Device owner

	

Rohan Saini




Image filename

	

IMG_20261118_101722.jpg

Important forensic distinction: EXIF records the timestamp and GPS metadata associated with the photograph. It does not independently prove who held the device or whether the metadata was altered.

5. Evidence D — Three candidate locations

Investigators have identified three fictional candidate locations for the exercise.

 

Location A — Old Bus Stand

26.220000° N, 78.180000° E

Mentioned in chat line 18.

 

Location B — Railway Station Entrance

26.215000° N, 78.170000° E

Alternative candidate location.

 

Location C — University Main Gate

26.200000° N, 78.165000° E

Plausible location associated with the university context.

Coordinate comparison

Coordinates are fictionalized candidate points. EXIF coordinates are the supplied forensic evidence.

Evidence

	

Latitude

	

Longitude




Photograph EXIF

	

26.220000

	

78.180000




Location A

	

26.220000

	

78.180000




Location B

	

26.215000

	

78.170000




Location C

	

26.200000

	

78.165000

Exact
coordinate
match
 Location A.

6. Student investigation questions

Answer the following using only the supplied evidence.

Question 1 — Instruction attribution

Who instructed Rohan to delete the UPI transfer record?

Question 2 — Timeline reconstruction

At what date and time was the instruction to delete the transfer record issued?

Question 3 — Geolocation

Where was the suspected mule, Rohan Saini, when the photograph was taken?

For each answer, provide:

Relevant WhatsApp line number(s).

Relevant call-log row(s), where applicable.

Supporting timestamps.

A brief explanation of how the evidence supports the conclusion.

7. Answer key — Instructor copy
Reveal after student submission
Answer 1: Who instructed the deletion?

Kabir Verma.

Supporting evidence:

Chat line 15: Kabir explicitly tells Rohan to delete the transfer record and remove screenshots.

Chat line 16: Rohan acknowledges the instruction.

Call-log row 4: Kabir called Rohan at 09:50:11, shortly before the instruction at 09:46?

Correction to timeline interpretation: Row 4 is at 09:50:11, which is after the 09:46 instruction. The earlier call in row 2 occurred at 09:34:05, before it. Therefore, row 4 cannot be treated as the call that preceded the instruction.

The strongest direct evidence is chat line 15, not the call log.

Answer 2: When was the deletion instruction issued?

18 November 2026 at 09:46.

Supporting evidence:

Chat line 15: Timestamp 09:46.

Chat line 16: Timestamp 09:48, confirming Rohan's acknowledgment.

Call-log row 2: 09:34:05, Kabir's earlier incoming call.

Call-log row 4: 09:50:11, Kabir's subsequent incoming call.

The sequence is consistent with a direct instruction followed by acknowledgment and subsequent communication.

Answer 3: Where was Rohan when the photograph was taken?

Location A — Old Bus Stand.

Supporting evidence:

EXIF DateTimeOriginal: 10:17:22.

EXIF GPS: 26.220000° N, 78.180000° E.

Chat line 18: Kabir directs Rohan toward the Old Bus Stand.

Chat line 19: Rohan confirms he has departed.

Chat line 20: Rohan says he is sending a photograph.

Chat line 21: Neha asks whether the bus stand sign is visible.

Chat line 22: Rohan confirms it is.

The photograph coordinates exactly match candidate Location A.

Evidence correlation matrix

Question

	

Chat evidence

	

Call-log evidence

	

Conclusion




Who ordered deletion?

	

Lines 15–16

	

Rows 2, 4 (context only)

	

Kabir




When?

	

Lines 15–16

	

Rows 2, 4 (context only)

	

09:46, 18 Nov




Where was the mule?

	

Lines 18–22

	

Row 5 (context only)

	

Old Bus Stand

8. Plausible wrong suspect: Dev Malhotra

Dev is deliberately included as a misleading suspect.

Reasons students might suspect him:

Line 4: He asks to be updated after payment.

Line 9: He requests a screenshot.

Line 14: He distances himself from the transaction.

Call-log row 6: He contacts Rohan at 10:26:03.

However:

No chat line shows Dev instructing deletion.

His call occurs 40 minutes after the deletion instruction.

His statements do not directly establish that he coordinated the fraud.

Forensic conclusion: Dev is a person of interest, but the supplied evidence does not establish that he ordered the deletion.

9. Suggested university marking rubric

Total: 20 marks

Assessment criterion

	

Marks




Correct identification of Kabir

	

4




Correct identification of deletion timestamp

	

4




Correct EXIF coordinate interpretation

	

4




Correct identification of Location A

	

3




Accurate chat-line citations

	

2




Accurate call-log row references

	

2




Recognition of Dev as an unproven suspect

	

1




Total

	

20

10. Instructor discussion points

Use these questions for a classroom discussion after students finish:

Why is a direct chat instruction stronger evidence of deletion attribution than a call occurring around the same time?

Can EXIF GPS metadata alone prove the physical location of a person?

Why should investigators distinguish between a device owner and the actual device user?

What additional evidence would help establish whether the transaction record was actually deleted?

Why should investigators preserve original device data and document the chain of custody?

Learning outcome: Students should demonstrate that reliable digital-forensic conclusions require correlation across communication records, timestamps, metadata and independent evidence—not simply choosing the person who appears most suspicious.
