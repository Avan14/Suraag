# Case upi-ring-031-l3: worked solution (instructor copy)

> SYNTHETIC CASE - fictional, for teaching only. Not real data. This file contains the answers.

Level 3 · Inspector. Decode a code word set up earlier, find the order that was actually carried out, and convert a camera clock to IST.

## Q1. Mule ko transfer record delete karne ko kisne kaha?

1. chat.txt:7: Divya didi sets a code. When anyone writes "doodh ubal gaya", the payment entry is to be deleted. This line is a rule, not the order.
2. chat.txt:21: at 9:53 pm, Lakshmi didi uses the code "doodh ubal gaya", so this is the actual order: "Vikram bhai, doodh ubal gaya, samjhe?"
3. chat.txt:22: at 9:55 pm the mule replies, so the order was carried out: "Ho gaya, sab uda diya."
4. chat.txt:26 also asks to remove an entry, but it comes after that reply and is about a different list, so it is not the order.
5. calls.csv:3: "Lakshmi didi" is saved in the call log as +91-55824-17660 and called at 21:52, just before the order.
6. The brief lists +91-55824-17660 as Lakshmi Iyer.
7. Two suspects share the first name Lakshmi, so the chat name alone cannot decide. The number does.

**Answer: Lakshmi Iyer.**

- Trap: taking the latest request. chat.txt:26 came after the mule had already replied, and it points at Lakshmi Sen.

## Q2. Ye instruction kab diya gaya?

1. chat.txt:7: Divya didi sets a code. When anyone writes "doodh ubal gaya", the payment entry is to be deleted. This line is a rule, not the order.
2. chat.txt:21: at 9:53 pm, Lakshmi didi uses the code "doodh ubal gaya", so this is the actual order: "Vikram bhai, doodh ubal gaya, samjhe?"
3. chat.txt:22: at 9:55 pm the mule replies, so the order was carried out: "Ho gaya, sab uda diya."
4. chat.txt:26 also asks to remove an entry, but it comes after that reply and is about a different list, so it is not the order.
5. calls.csv:3 at 21:52 agrees with the chat time within 2 minutes.

**Answer: 9:53 pm.**

- Trap: searching for the word "delete". The first hit, chat.txt:7 at 9:02 pm, only sets up the code.

## Q3. Payment screenshot wali photo li gayi tab mule kahan tha?

1. photo.jpg:GPSLatitude, photo.jpg:GPSLongitude: the photo's GPS reads 19.0179, 72.8478.
2. That point is 11 m from Dadar. The next nearest place, Andheri East, is 10.9 km away.

**Answer: Dadar.**

## Q4. Payment screenshot wali photo IST mein kitne baje li gayi?

1. photo.jpg:DateTimeOriginal: the camera clock says 2026:03:06 17:03:00.
2. photo.jpg:OffsetTimeOriginal: the offset is +00:00, so that clock was not on IST (+05:30).
3. IST is +05:30, so shift the clock by +5 h 30 min: 17:03 becomes 10:33 pm.

**Answer: 10:33 pm.**

- Trap: reading the EXIF clock as IST. That gives 5:03 pm, which is 5 h 30 min off.
