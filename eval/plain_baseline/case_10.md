Fictional UPI Fraud Forensic Training Case

Fictional
academic
simulation
 
University
forensic
exercise

Case ID: UPI-FOR-2026-017
Case title: Operation Split Ledger
Location: Gwalior, Madhya Pradesh, India
Investigation type: Digital forensics, timeline reconstruction, communication analysis and geolocation.

All people, phone numbers, transactions, messages, and locations in this exercise are fictional. Phone numbers are synthetic identifiers and are not intended to represent real subscribers.

1. Case background

On 18 November 2026, a university cybercrime research team received a simulated complaint involving an unauthorized UPI transfer of ₹48,500.

The investigation identified three individuals:

Aarav Sharma: Alleged mule account holder who received the transferred funds.

Riya Verma: Group administrator and suspected coordinator.

Kabir Khan: A person who communicated with Aarav shortly before the transfer record was deleted. He is also a plausible but potentially innocent suspect.

Investigators recovered:

A WhatsApp-style group chat export.

A simulated mobile call log.

EXIF metadata from a recovered photograph.

Three candidate geographical locations.

The objective is to reconstruct the events and identify the person responsible for instructing deletion of the transfer record.

2. WhatsApp-style group chat export

Group: UPI Support Team (Fictional)
Export date: 19 November 2026
Timezone: IST (UTC+05:30)

25 numbered forensic message records

text
[01] 18-11-2026 09:02 - Riya: Good morning sabko, aaj ka settlement pending hai.

[02] 18-11-2026 09:04 - Aarav: Haan, mera account ready hai.

[03] 18-11-2026 09:07 - Kabir: Bhai kal wala transaction clear hua kya?

[04] 18-11-2026 09:10 - Aarav: Abhi tak credit show ho raha hai.

[05] 18-11-2026 09:13 - Riya: Screenshot group mein mat bhejna.

[06] 18-11-2026 09:18 - Aarav: 48,500 ka transfer record mere paas hai.

[07] 18-11-2026 09:22 - Kabir: Mujhe bhi bank ka SMS aaya tha.

[08] 18-11-2026 09:25 - Riya: Kabir, tum apne kaam se kaam rakho.

[09] 18-11-2026 09:31 - Aarav: Riya, transfer ka reference number save kar liya hai.

[10] 18-11-2026 09:36 - Riya: Achha, phone ka backup bhi check kar lena.

[11] 18-11-2026 09:42 - Kabir: Main toh abhi college mein hoon, baad mein call karunga.

[12] 18-11-2026 09:47 - Aarav: Mujhe unknown number se call aaya tha.

[13] 18-11-2026 09:50 - Riya: Kisne kiya?

[14] 18-11-2026 09:53 - Aarav: Number save nahi hai, 2 minute baat hui.

[15] 18-11-2026 10:01 - Riya: Aarav, transfer record delete kar do. Abhi. Phone aur gallery dono check karna.

[16] 18-11-2026 10:03 - Aarav: Theek hai, delete kar diya.

[17] 18-11-2026 10:05 - Kabir: Kya delete kar diya? Main toh kuch nahi bola.

[18] 18-11-2026 10:11 - Aarav: Main photo lene bahar aaya hoon.

[19] 18-11-2026 10:16 - Riya: Location group mein share mat karna.

[20] 18-11-2026 10:24 - Aarav: Photo click ho gayi. GPS on tha shayad.

[21] 18-11-2026 10:29 - Kabir: Main library mein hoon, proof chahiye toh attendance dekh lena.

[22] 18-11-2026 10:35 - Riya: Sab log purani baatein bhool jao.

[23] 18-11-2026 10:42 - Aarav: Mujhe ab thoda tension ho raha hai.

[24] 18-11-2026 10:50 - Riya: Kisi ko bhi original screenshot forward mat karna.

[25] 18-11-2026 11:02 - Aarav: Samajh gaya. Main ab ghar ja raha hoon.
3. Call log (CSV)

Evidence source: Simulated Android call-history extraction
Device owner: Aarav Sharma

csv
row,datetime,direction,number,contact_name,duration_s
1,2026-11-18 09:20:14,IN,+91-5000000101,Riya Verma,184
2,2026-11-18 09:40:08,OUT,+91-5000000102,Kabir Khan,96
3,2026-11-18 09:48:32,IN,+91-5000000199,Unknown Caller,121
4,2026-11-18 09:57:45,IN,+91-5000000101,Riya Verma,238
5,2026-11-18 10:07:19,OUT,+91-5000000102,Kabir Khan,42
6,2026-11-18 10:32:51,IN,+91-5000000101,Riya Verma,67

Forensic observation: Riya had two calls with Aarav before the deletion message and another call shortly afterward. Kabir also communicated with Aarav, making him a potential alternative suspect.

4. EXIF metadata of recovered photograph

Evidence ID: IMG_20261118_1024.jpg
Source: Simulated mobile photograph recovered from Aarav's device.

EXIF field

	

Extracted value




File name

	

IMG_20261118_1024.jpg




Make

	

Samsung




Model

	

Galaxy A54 (fictional evidence attribution)




DateTimeOriginal

	

2026:11:18 10:24:16




GPSLatitude

	

26°13′48.0″ N




GPSLongitude

	

78°10′12.0″ E




GPSLatitudeRef

	

N




GPSLongitudeRef

	

E

Coordinate conversion:

Latitude: 26.230000

Longitude: 78.170000

Coordinates are fictionalized evidence for this classroom exercise.

5. Candidate locations

Investigators have identified three possible locations in the simulated investigation area.

Reset view
Expand map
Candidate A – Railway Station Area
Candidate B – University Library Area
3.9
Candidate C – City Bus Stand Area
© Mapbox © OpenStreetMap Improve this map
Candidate A – Railway Station Area
Police station
Candidate B – University Library Area
Point
Candidate C – City Bus Stand Area
★ 3.9 · Bus tour agency

Candidate

	

Location

	

Latitude

	

Longitude




A

	

Railway Station Area

	

26.230000

	

78.170000




B

	

University Library Area

	

26.218000

	

78.165000




C

	

City Bus Stand Area

	

26.204000

	

78.175000

The EXIF coordinates should be compared against all three candidates.

6. Questions for students

Question 1 – Instruction attribution

Who instructed Aarav to delete the UPI transfer record?

Question 2 – Timeline reconstruction

At what exact date and time was Aarav instructed to delete the transfer record?

Question 3 – Geolocation analysis

Where was the suspected mule (Aarav) when the photograph was taken?

Students should support their conclusions using the chat export, call log, and EXIF metadata.

7. Answer key
Instructor reference
Answer 1: Who instructed deletion?

Answer: Riya Verma.

Supporting evidence:

Chat line 15 explicitly states: "Aarav, transfer record delete kar do. Abhi."

Chat line 16 records Aarav acknowledging the deletion.

Call-log row 4 shows an incoming call from Riya at 09:57:45, shortly before the instruction at 10:01.

Conclusion: Riya is the person explicitly instructing Aarav to delete the transfer record.

Answer 2: When was the instruction given?

Answer: 18 November 2026, at 10:01 IST.

Supporting evidence:

Chat line 15: 10:01 – Riya instructs Aarav to delete the record.

Chat line 16: 10:03 – Aarav confirms deletion.

Call-log row 4: 09:57:45 – Incoming call from Riya.

Call-log row 6: 10:32:51 – Another incoming call from Riya.

Conclusion: The instruction was documented at 10:01 IST, with acknowledgment two minutes later.

Answer 3: Where was the mule when the photograph was taken?

Answer: Candidate A – Railway Station Area.

Supporting evidence:

EXIF DateTimeOriginal: 10:24:16 on 18 November 2026.

EXIF GPS: 26.230000° N, 78.170000° E.

Candidate A has exactly matching coordinates.

Chat line 20 records Aarav confirming that he took a photograph at 10:24.

Conclusion: The photograph places Aarav at Candidate A, according to the simulated EXIF evidence.

8. Suspect comparison

Suspect

	

Evidence

	

Assessment




Riya Verma

	

Direct deletion instruction in line 15; calls in rows 1, 4 and 6

	

Primary suspect




Aarav Sharma

	

Account holder, acknowledged deletion in line 16

	

Mule/account holder; participant




Kabir Khan

	

Calls in rows 2 and 5; questioned the deletion in line 17

	

Plausible wrong suspect

Why Kabir is a plausible wrong suspect:

He communicated with Aarav before the deletion.

He received and discussed transaction-related information.

His calls might initially appear suspicious.

However, line 17 shows him questioning the deletion rather than instructing it.

His claim of being at the library (line 21) is not independently verified by this dataset.

9. Suggested university assessment rubric

Assessment criterion

	

Marks




Correct identification of deletion instructor

	

5




Accurate timestamp reconstruction

	

5




Correct EXIF coordinate interpretation

	

5




Correct chat and call-log cross-referencing

	

5




Identification and evaluation of wrong suspect

	

5




Total

	

25

10. Discussion: Forensic limitations

Students should recognize that:

A WhatsApp-style export does not independently establish message authenticity.

Call logs establish recorded communication events, not the actual conversation contents.

EXIF GPS metadata can be altered and should be corroborated with original files and other evidence.

A matching coordinate identifies a location, not necessarily the identity of the photographer.

Temporal proximity between a phone call and a message does not prove that the call contained the instruction.

Final learning objective: Students should distinguish between direct evidence, circumstantial evidence, corroboration, and unsupported assumptions when reconstructing a digital-fraud incident.
