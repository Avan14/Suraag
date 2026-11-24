# Grader worksheet: label these by hand

Rule. **Answer correct:** the answer is what the evidence supports (a time within 2 minutes counts).
**Evidence valid:** every file the question needs has at least one cited line that contains ALL the
strings needed for the claim, and NO cited line is wrong (a line is wrong if it contains none of them,
does not exist, or is in a file this question does not use). A line with only some of the strings
neither earns nor costs. Extra lines that genuinely support the claim are fine.

Fill `label_answer_correct` and `label_citation_valid` (true/false) in eval/answers.json for each entry.

## Answer 1: case upi-ring-001 (en), Q1 (who)

Question: Who told the mule to delete the transfer record?  
Student answer: `P4`

Strings the claim needs: chat: '6:58 pm' + 'Prakash ji'; calls: '+91-57297-34908' + '18:57'

Cited lines:
- chat 13: `16/04/26, 6:58 pm - Prakash ji: Mahesh ji, delete the transfer record right now`
- calls 4: `2026-04-16T18:57:00+05:30,incoming,+91-57297-34908,Prakash ji,47`

## Answer 2: case upi-ring-001 (en), Q2 (when)

Question: When was the instruction given?  
Student answer: `6:58 pm`

Strings the claim needs: chat: '6:58 pm' + 'Prakash ji'; calls: '+91-57297-34908' + '18:57'

Cited lines:
- chat 2: `16/04/26, 6:04 pm - Ashok ji: Good evening everyone, how was work today?`
- calls 4: `2026-04-16T18:57:00+05:30,incoming,+91-57297-34908,Prakash ji,47`

## Answer 3: case upi-ring-002 (hinglish), Q2 (when)

Question: Ye instruction kab diya gaya?  
Student answer: `11:55 pm`

Strings the claim needs: chat: '8:30 pm' + 'Subhash bhai'; calls: '+91-58340-48766' + '20:29'

Cited lines:
- chat 15: `24/03/26, 8:30 pm - Subhash bhai: Deepak bhai, ye entry abhi delete kar do, kisi ko mat batana`
- calls 4: `2026-03-24T20:29:00+05:30,incoming,+91-58340-48766,Subhash bhai,123`

## Answer 4: case upi-ring-002 (hinglish), Q3 (where)

Question: Payment screenshot wali photo li gayi tab mule kahan tha?  
Student answer: `PL2`

Strings the claim needs: photo: '19.2187'; photo: '72.9781'

Cited lines:
- photo GPSLatitude: `19.2187`

## Answer 5: case upi-ring-003 (en), Q1 (who)

Question: Who told the mule to delete the transfer record?  
Student answer: `P4`

Strings the claim needs: chat: '9:37 pm' + 'Rina ji'; calls: '+91-56994-51768' + '21:36'

Cited lines:
- chat 11: `16/04/26, 9:37 pm - Rina ji: Hetal ji, delete the transfer record right now`
- calls 4: `2026-04-16T21:36:00+05:30,incoming,+91-56994-51768,Rina ji,151`
- chat 999: `None`

## Answer 6: case upi-ring-003 (en), Q2 (when)

Question: When was the instruction given?  
Student answer: `9:37 pm`

Strings the claim needs: chat: '9:37 pm' + 'Rina ji'; calls: '+91-56994-51768' + '21:36'

Cited lines:
- chat 11: `16/04/26, 9:37 pm - Rina ji: Hetal ji, delete the transfer record right now`
- calls 4: `2026-04-16T21:36:00+05:30,incoming,+91-56994-51768,Rina ji,151`
- chat 2: `16/04/26, 8:48 pm - Rina M.: Good evening everyone, did you all have dinner?`

## Answer 7: case upi-ring-004 (hinglish), Q2 (when)

Question: Ye instruction kab diya gaya?  
Student answer: `7:27 pm`

Strings the claim needs: chat: '7:27 pm' + 'Nilesh bhai'; calls: '+91-54264-35618' + '19:25'

Cited lines:
- chat 14: `13/03/26, 7:27 pm - Nilesh bhai: Mahesh bhai, wo transfer ka record delete kar dena abhi`
- calls 3: `2026-03-13T19:25:00+05:30,incoming,+91-54264-35618,Nilesh bhai,103`
- photo Make: `Redmi`

## Answer 8: case upi-ring-004 (hinglish), Q3 (where)

Question: Payment screenshot wali photo li gayi tab mule kahan tha?  
Student answer: `PL2`

Strings the claim needs: photo: '19.1139'; photo: '72.8698'

Cited lines:
- (no citations)

## Answer 9: case upi-ring-005 (en), Q1 (who)

Question: Who told the mule to delete the transfer record?  
Student answer: `P3`

Strings the claim needs: chat: '7:38 pm' + 'Pooja ji'; calls: '+91-50214-95837' + '19:37'

Cited lines:
- chat 15: `18/03/26, 7:40 pm - Pooja ji: I just reached the tea stall.`
- calls 3: `2026-03-18T19:37:00+05:30,incoming,+91-50214-95837,Pooja ji,41`

## Answer 10: case upi-ring-005 (en), Q2 (when)

Question: When was the instruction given?  
Student answer: `7:38 pm`

Strings the claim needs: chat: '7:38 pm' + 'Pooja ji'; calls: '+91-50214-95837' + '19:37'

Cited lines:
- chat 14: `18/03/26, 7:38 pm - Pooja ji: Pranab ji, delete the transfer record right now`
- calls 3: `2026-03-18T19:37:00+05:30,incoming,+91-50214-95837,Pooja ji,41`

## Answer 11: case upi-ring-006 (hinglish), Q2 (when)

Question: Ye instruction kab diya gaya?  
Student answer: `9:39 pm`

Strings the claim needs: chat: '9:39 pm' + 'Subhash bhai'; calls: '+91-58835-89397' + '21:38'

Cited lines:
- chat 11: `14/04/26, 9:39 pm - Subhash bhai: Prakash bhai, ye entry abhi delete kar do, kisi ko mat batana`
- calls 3: `2026-04-14T21:38:00+05:30,incoming,+91-58835-89397,Subhash bhai,104`

## Answer 12: case upi-ring-006 (hinglish), Q3 (where)

Question: Payment screenshot wali photo li gayi tab mule kahan tha?  
Student answer: `PL3`

Strings the claim needs: photo: '19.0723'; photo: '72.8841'

Cited lines:
- chat 2: `14/04/26, 8:32 pm - Mamta didi: Subhash bhai woh wala hisaab dekh liya kya?`
- photo GPSLatitude: `19.0723`
- photo GPSLongitude: `72.8841`

## Answer 13: case upi-ring-007 (en), Q1 (who)

Question: Who told the mule to delete the transfer record?  
Student answer: `P2`

Strings the claim needs: chat: '8:08 pm' + 'Sunil ji'; calls: '+91-59593-59399' + '20:07'

Cited lines:
- chat 14: `24/03/26, 8:08 pm - Sunil ji: Divya ji, delete the transfer record right now`
- calls 3: `2026-03-24T20:07:00+05:30,incoming,+91-59593-59399,Sunil ji,154`

## Answer 14: case upi-ring-007 (en), Q2 (when)

Question: When was the instruction given?  
Student answer: `8:08 pm`

Strings the claim needs: chat: '8:08 pm' + 'Sunil ji'; calls: '+91-59593-59399' + '20:07'

Cited lines:
- chat 14: `24/03/26, 8:08 pm - Sunil ji: Divya ji, delete the transfer record right now`

## Answer 15: case upi-ring-008 (hinglish), Q2 (when)

Question: Ye instruction kab diya gaya?  
Student answer: `8:27 pm`

Strings the claim needs: chat: '8:27 pm' + 'Vikram bhai'; calls: '+91-57424-51180' + '20:25'

Cited lines:
- chat 9: `06/03/26, 8:27 pm - Vikram bhai: Manoj bhai, ye entry abhi delete kar do, kisi ko mat batana`
- calls 3: `2026-03-06T20:25:00+05:30,incoming,+91-57424-51180,Vikram bhai,106`
- chat 999: `None`

## Answer 16: case upi-ring-008 (hinglish), Q3 (where)

Question: Payment screenshot wali photo li gayi tab mule kahan tha?  
Student answer: `PL3`

Strings the claim needs: photo: '19.0593'; photo: '72.8291'

Cited lines:
- photo GPSLatitude: `19.0593`
- photo GPSLongitude: `72.8291`
- chat 2: `06/03/26, 7:18 pm - Subhash bhai: Vikram bhai chai peene chalein shaam ko?`

## Answer 17: case upi-ring-009 (en), Q1 (who)

Question: Who told the mule to delete the transfer record?  
Student answer: `P3`

Strings the claim needs: chat: '9:26 pm' + 'Pooja ji'; calls: '+91-56285-97792' + '21:25'

Cited lines:
- chat 12: `14/03/26, 9:26 pm - Pooja ji: Kavita ji, delete the transfer record right now`
- calls 3: `2026-03-14T21:25:00+05:30,incoming,+91-56285-97792,Pooja ji,51`
- photo Make: `Realme`

## Answer 18: case upi-ring-009 (en), Q2 (when)

Question: When was the instruction given?  
Student answer: `9:26 pm`

Strings the claim needs: chat: '9:26 pm' + 'Pooja ji'; calls: '+91-56285-97792' + '21:25'

Cited lines:
- (no citations)

## Answer 19: case upi-ring-010 (hinglish), Q2 (when)

Question: Ye instruction kab diya gaya?  
Student answer: `7:39 pm`

Strings the claim needs: chat: '7:39 pm' + 'Venkat bhai'; calls: '+91-50725-76406' + '19:37'

Cited lines:
- chat 13: `24/03/26, 7:40 pm - Venkat R.: Sab log pahunch gaye kya?`
- calls 3: `2026-03-24T19:37:00+05:30,incoming,+91-50725-76406,Venkat bhai,168`

## Answer 20: case upi-ring-010 (hinglish), Q3 (where)

Question: Payment screenshot wali photo li gayi tab mule kahan tha?  
Student answer: `PL1`

Strings the claim needs: photo: '19.2303'; photo: '72.8565'

Cited lines:
- photo GPSLatitude: `19.2303`
- photo GPSLongitude: `72.8565`
