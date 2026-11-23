University Forensic Training Case: The Vanishing UPI Transfer

Fictional
forensic
simulation
 
Intermediate
difficulty

Case ID: UPI-FOR-2026-017
Subject: Suspected UPI fraud, mule-account coordination, evidence deletion and digital geolocation
Intended audience: University students studying cyber forensics, digital investigation and financial crime.

All names, telephone numbers, transactions, coordinates and events below are fictional. The phone numbers use the requested +91-5 prefix and are simulated identifiers, not verified subscriber numbers.

1. Case background

On 21 November 2026, a student named Aarav Mehta reported that ₹18,750 had been transferred from his UPI account after he interacted with someone claiming to represent a university scholarship office.

The receiving account belonged to a person named Rohan Sethi, who is suspected of acting as a money mule.

Investigators recovered:

A WhatsApp-style group chat export.

A six-entry call log from a seized training-device image.

One photograph with EXIF metadata.

Three candidate locations associated with the investigation.

The central investigative questions concern who ordered the deletion of the transfer record, when the instruction was given, and where the suspected mule was when a photograph was captured.

2. WhatsApp-style group chat export

Group: Scholarship Help – Internal
Date range: 21–22 November 2026
Recovered device: Simulated device belonging to Rohan Sethi.

Line

	

Date and time

	

Sender

	

Message




01

	

21-11-2026 18:02

	

Rohan

	

Bhai scholarship wala payment aa gaya kya?




02

	

21-11-2026 18:04

	

Kabir

	

Haan, ek student se 18,750 receive hua hai.




03

	

21-11-2026 18:05

	

Rohan

	

Mere account mein show ho raha hai.




04

	

21-11-2026 18:07

	

Nisha

	

Student ko scholarship verification bola tha na?




05

	

21-11-2026 18:08

	

Kabir

	

Haan, usko official process hi laga.




06

	

21-11-2026 18:11

	

Rohan

	

Ab next kya karna hai?




07

	

21-11-2026 18:13

	

Dev

	

Group mein transaction details mat bhejna.




08

	

21-11-2026 18:15

	

Kabir

	

Rohan, transfer ka screenshot save kiya hai?




09

	

21-11-2026 18:16

	

Rohan

	

Haan, gallery mein hai.




10

	

21-11-2026 18:20

	

Nisha

	

Bhai, tension mat le. Sab manage ho jayega.




11

	

21-11-2026 18:24

	

Rohan

	

Unknown number se call aa raha hai.




12

	

21-11-2026 18:26

	

Dev

	

Abhi kisi ko transaction ka detail mat dena.




13

	

21-11-2026 18:32

	

Kabir

	

Payment ka record phone mein rehne dena filhaal.




14

	

21-11-2026 18:41

	

Rohan

	

Ek missed call bhi aaya tha.




15

	

21-11-2026 18:45

	

Nisha

	

Main toh is matter mein involved nahi hoon.




16

	

21-11-2026 19:03

	

Rohan

	

Dev bhai, aapka call aaya tha kya?




17

	

21-11-2026 19:05

	

Dev

	

Haan, baat karni hai. Call karo.




18

	

21-11-2026 19:12

	

Rohan

	

Call kar liya. Samajh gaya.




19

	

21-11-2026 19:16

	

Rohan

	

Screenshot gallery se hata diya.




20

	

21-11-2026 19:18

	

Kabir

	

Kisne bola delete karne ko?




21

	

21-11-2026 19:19

	

Rohan

	

Dev bhai ne kaha tha, transfer record delete kar de.




22

	

21-11-2026 19:21

	

Dev

	

Group mein is baare mein aur discussion mat karo.




23

	

22-11-2026 08:14

	

Rohan

	

Kal wali photo phone mein abhi bhi hai.




24

	

22-11-2026 08:17

	

Kabir

	

Location wali photo?




25

	

22-11-2026 08:19

	

Rohan

	

Haan, station ke paas wali.

3. Call log (CSV)

Source: Simulated mobile-device call-log extraction.

csv
row,datetime,direction,number,contact_name,duration_s
1,2026-11-21 18:24:10,INCOMING,+91-5000000101,Unknown Caller,42
2,2026-11-21 18:41:05,MISSED,+91-5000000102,Unknown Number,0
3,2026-11-21 19:03:12,OUTGOING,+91-5000000103,Dev Malhotra,186
4,2026-11-21 19:27:44,INCOMING,+91-5000000104,Kabir Rao,73
5,2026-11-22 08:05:21,OUTGOING,+91-5000000103,Dev Malhotra,94
6,2026-11-22 08:22:09,INCOMING,+91-5000000105,Unknown Caller,31

Investigation note: Row 3 records an outgoing call to Dev at 19:03, shortly before Rohan's acknowledgement in chat line 18 and deletion statement in line 19.

4. Recovered photo: EXIF metadata

File name: IMG_20261121_190845.jpg

 

Illustrative photograph only. It is not the actual evidence image.

Extracted metadata:

text
FileName: IMG_20261121_190845.jpg
DateTimeOriginal: 2026:11:21 18:08:45
GPSLatitude: 26 deg 13' 12.00" N
GPSLatitudeRef: N
GPSLongitude: 78 deg 10' 48.00" E
GPSLongitudeRef: E

Converted decimal coordinates:

Latitude: 26.220000

Longitude: 78.180000

Forensic observation: The photo was captured before the 19:03 call to Dev. Its GPS coordinates are the principal location evidence for this exercise.

5. Candidate places

Investigators identified three candidate locations in the vicinity of the fictional incident.

Reset view
Expand map
4.0
Candidate A – Gwalior Railway Station
3.4
Candidate B – City Bus Stand
5.0
Candidate C – University Main Gate
© Mapbox © OpenStreetMap Improve this map
Candidate A – Gwalior Railway Station
★ 4 · Railway services
Open
Candidate B – City Bus Stand
★ 3.4 · Bus depot
Candidate C – University Main Gate
★ 5 · Boys' hostel
Open

Candidate

	

Place

	

Latitude

	

Longitude




A

	

Gwalior Railway Station

	

26.220000

	

78.180000




B

	

City Bus Stand

	

26.218300

	

78.160500




C

	

University Main Gate

	

26.205500

	

78.192000

The candidate names and coordinates are fictional training data.

6. Student investigation questions

Answer using only the evidence supplied.

Question 1. Who instructed Rohan to delete the transfer record?

Identify the individual and cite the supporting chat evidence.

Question 2. When was the deletion instruction most likely communicated?

Determine the likely time using both the WhatsApp export and call log. Distinguish the time of the instruction from the time the deletion was acknowledged.

Question 3. Where was the suspected mule when the photograph was taken?

Identify the most likely candidate location using the EXIF coordinates.

7. Plausible wrong suspect

Kabir Rao is an intentionally plausible alternative suspect.

Reasons for suspicion:

He asks about the incoming payment (line 02).

He asks whether Rohan saved the screenshot (line 08).

He questions who instructed the deletion (line 20).

He has a phone call with Rohan at 19:27 (call-log row 4).

However, these facts do not establish that Kabir ordered the deletion.

Students should distinguish suspicious behaviour from evidence directly linking a person to an instruction.

8. Instructor answer key
Instructor copy
Answer 1: Who instructed the deletion?

Answer: Dev Malhotra.

Evidence:

Chat line 17: Dev tells Rohan to call him.

Chat line 18: Rohan confirms that the call took place.

Chat line 19: Rohan reports that he removed the screenshot.

Chat line 21: Rohan explicitly states: "Dev bhai ne kaha tha, transfer record delete kar de."

Call-log row 3: An outgoing call to Dev is recorded at 19:03:12, lasting 186 seconds.

Reasoning: The strongest direct attribution is chat line 21. Call-log row 3 independently supports the timing of contact between Rohan and Dev.

Answer 2: When was the instruction given?

Answer: Most likely around 19:03–19:06 on 21 November 2026.

Evidence:

Evidence

	

Time

	

Significance




Chat line 17

	

19:05

	

Dev requests a call




Call-log row 3

	

19:03:12

	

Rohan calls Dev




Call-log row 3

	

19:03:12–19:06:18

	

Call duration is 186 seconds




Chat line 18

	

19:12

	

Rohan confirms the call




Chat line 19

	

19:16

	

Rohan confirms screenshot removal




Chat line 21

	

19:19

	

Rohan attributes the deletion instruction to Dev

Reasoning: The call lasted approximately three minutes and ended at 19:06:18. The evidence supports the inference that the instruction was communicated during this call.

The exact spoken instruction time cannot be established from the call log alone.

Answer 3: Where was the mule when the photograph was taken?

Answer: Candidate A – Gwalior Railway Station.

EXIF evidence:

DateTimeOriginal: 21 November 2026, 18:08:45.

GPS: 26.220000° N, 78.180000° E.

Comparison:

Candidate

	

Coordinates

	

Assessment




A – Railway Station

	

26.220000, 78.180000

	

Exact
coordinate
match




B – City Bus Stand

	

26.218300, 78.160500

	

Does not match




C – University Main Gate

	

26.205500, 78.192000

	

Does not match

Reasoning: The EXIF coordinates exactly match Candidate A's supplied coordinates.

This establishes the photograph's recorded location within the simulation, not necessarily the photographer's identity or the authenticity of the metadata.

9. Evidence correlation matrix

Finding

	

Chat evidence

	

Call-log evidence

	

Metadata




Dev instructed deletion

	

Lines 17, 18, 21

	

Row 3

	

—




Instruction likely during call

	

Lines 17–19

	

Row 3

	

—




Screenshot subsequently deleted

	

Lines 19, 21

	

Row 3

	

—




Photo location

	

Lines 23–25

	

—

	

EXIF GPS




Photo capture time

	

Lines 23–25 (context only)

	

—

	

DateTimeOriginal

10. Suggested university marking rubric

Total: 20 marks

Assessment criterion

	

Marks




Correct identification of Dev

	

4




Correct citation of chat lines 17–21

	

4




Correct interpretation of call-log row 3

	

4




Correct distinction between instruction and deletion times

	

3




Correct EXIF coordinate interpretation

	

3




Recognition of Kabir as an unproven alternative suspect

	

2




Total

	

20

11. Instructor discussion: forensic limitations

Students should also understand the following:

WhatsApp evidence: A chat export can be edited or incomplete. Its integrity should be assessed against the original device and available database evidence.

Call logs: A call record establishes a recorded communication event, not what was said during the call.

EXIF metadata: GPS and timestamps can be altered. Investigators should verify them against original files, device records and independent evidence.

Deletion evidence: A message claiming that a screenshot was deleted does not independently prove secure erasure. Recoverability requires separate forensic examination.

Suspect attribution: Possession of a mule account or participation in a conversation does not automatically establish criminal intent.

Final instructor conclusion: The simulated evidence points to Dev Malhotra as the person who instructed Rohan to delete the transfer record, most likely during their 19:03–19:06 call on 21 November 2026. The photograph's recorded GPS coordinates place the mule at Candidate A, Gwalior Railway Station.

Teaching note: This is a fictional evidence-correlation exercise, not a real criminal investigation or proof of guilt.
