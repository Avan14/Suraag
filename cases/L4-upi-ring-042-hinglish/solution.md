# Case upi-ring-042-l4: worked solution (instructor copy)

> SYNTHETIC CASE - fictional, for teaching only. Not real data. This file contains the answers.

Level 4 · Expert. Everything from levels 2 and 3 in one longer case.

## Q1. Mule ko transfer record delete karne ko kisne kaha?

1. chat.txt:6: Pooja didi sets a code. When anyone writes "doodh ubal gaya", the payment entry is to be deleted. This line is a rule, not the order.
2. chat.txt:19: at 9:40 pm, Tanuja didi uses the code "doodh ubal gaya", so this is the actual order: "Subhash bhai, jaise abhi phone pe bola, doodh ubal gaya, samjhe?"
3. chat.txt:20: at 9:42 pm the mule replies, so the order was carried out: "Ho gaya, sab uda diya."
4. chat.txt:22 also asks to remove an entry, but it comes after that reply and is about a different list, so it is not the order.
5. The call log has no contact saved as "Tanuja didi", but the order says it follows a phone call. calls.csv:5 is the only answered call in the 2 minutes before it, from the unsaved number +91-53257-93850.
6. The brief lists +91-53257-93850 as Tanuja Sen.
7. Two suspects share the first name Tanuja, so the chat name alone cannot decide. The number does.

**Answer: Tanuja Sen.**

- Trap: matching by first name. "Tanuja I." in the call log looks like "Tanuja didi", but that number belongs to Tanuja Iyer.
- Trap: taking the latest request. chat.txt:22 came after the mule had already replied, and it points at Tanuja Iyer.

## Q2. Ye instruction kab diya gaya?

1. chat.txt:6: Pooja didi sets a code. When anyone writes "doodh ubal gaya", the payment entry is to be deleted. This line is a rule, not the order.
2. chat.txt:19: at 9:40 pm, Tanuja didi uses the code "doodh ubal gaya", so this is the actual order: "Subhash bhai, jaise abhi phone pe bola, doodh ubal gaya, samjhe?"
3. chat.txt:20: at 9:42 pm the mule replies, so the order was carried out: "Ho gaya, sab uda diya."
4. chat.txt:22 also asks to remove an entry, but it comes after that reply and is about a different list, so it is not the order.
5. calls.csv:5 at 21:38 agrees with the chat time within 2 minutes.

**Answer: 9:40 pm.**

- Trap: searching for the word "delete". The first hit, chat.txt:6 at 8:59 pm, only sets up the code.

## Q3. Payment screenshot wali photo li gayi tab mule kahan tha?

1. photo.jpg:GPSLatitude, photo.jpg:GPSLongitude: the photo's GPS reads 19.2304, 72.8570.
2. That point is 46 m from Borivali West. The next nearest place, Andheri East, is 13.1 km away.
3. chat.txt:30: the mule claims to be at Andheri East. A chat message is a claim; the GPS is written by the phone, and ModifyDate equals DateTimeOriginal, so the photo shows no sign of later editing.

**Answer: Borivali West.**

- Trap: believing the chat. chat.txt:30 names Andheri East, but the phone's GPS puts the photo elsewhere.

## Q4. Payment screenshot wali photo IST mein kitne baje li gayi?

1. photo.jpg:DateTimeOriginal: the camera clock says 2026:04:11 16:50:00.
2. photo.jpg:OffsetTimeOriginal: the offset is +00:00, so that clock was not on IST (+05:30).
3. IST is +05:30, so shift the clock by +5 h 30 min: 16:50 becomes 10:20 pm.

**Answer: 10:20 pm.**

- Trap: reading the EXIF clock as IST. That gives 4:50 pm, which is 5 h 30 min off.
