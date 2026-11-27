# Case upi-ring-033-l3: worked solution (instructor copy)

> SYNTHETIC CASE - fictional, for teaching only. Not real data. This file contains the answers.

Level 3 · Inspector. Decode a code word set up earlier, find the order that was actually carried out, and convert a camera clock to IST.

## Q1. Mule ko transfer record delete karne ko kisne kaha?

1. chat.txt:6: Abhijit bhai sets a code. When anyone writes "mehmaan chale gaye", the payment entry is to be deleted. This line is a rule, not the order.
2. chat.txt:15: at 7:21 pm, Mahesh bhai uses the code "mehmaan chale gaye", so this is the actual order: "Karthik bhai, mehmaan chale gaye."
3. chat.txt:16: at 7:24 pm the mule replies, so the order was carried out: "Ho gaya bhai, saaf kar diya. Ab koi nahi dekhega."
4. chat.txt:20 also asks to remove an entry, but it comes after that reply and is about a different list, so it is not the order.
5. calls.csv:4: "Mahesh bhai" is saved in the call log as +91-59103-89306 and called at 19:19, just before the order.
6. The brief lists +91-59103-89306 as Mahesh Desai.
7. Two suspects share the first name Mahesh, so the chat name alone cannot decide. The number does.

**Answer: Mahesh Desai.**

- Trap: taking the latest request. chat.txt:20 came after the mule had already replied, and it points at Mahesh Sen.

## Q2. Ye instruction kab diya gaya?

1. chat.txt:6: Abhijit bhai sets a code. When anyone writes "mehmaan chale gaye", the payment entry is to be deleted. This line is a rule, not the order.
2. chat.txt:15: at 7:21 pm, Mahesh bhai uses the code "mehmaan chale gaye", so this is the actual order: "Karthik bhai, mehmaan chale gaye."
3. chat.txt:16: at 7:24 pm the mule replies, so the order was carried out: "Ho gaya bhai, saaf kar diya. Ab koi nahi dekhega."
4. chat.txt:20 also asks to remove an entry, but it comes after that reply and is about a different list, so it is not the order.
5. calls.csv:4 at 19:19 agrees with the chat time within 2 minutes.

**Answer: 7:21 pm.**

- Trap: searching for the word "delete". The first hit, chat.txt:6 at 6:45 pm, only sets up the code.

## Q3. Payment screenshot wali photo li gayi tab mule kahan tha?

1. photo.jpg:GPSLatitude, photo.jpg:GPSLongitude: the photo's GPS reads 19.0175, 72.8475.
2. That point is 46 m from Dadar. The next nearest place, Vashi, is 17.2 km away.

**Answer: Dadar.**

## Q4. Payment screenshot wali photo IST mein kitne baje li gayi?

1. photo.jpg:DateTimeOriginal: the camera clock says 2026:04:27 14:30:00.
2. photo.jpg:OffsetTimeOriginal: the offset is +00:00, so that clock was not on IST (+05:30).
3. IST is +05:30, so shift the clock by +5 h 30 min: 14:30 becomes 8:00 pm.

**Answer: 8:00 pm.**

- Trap: reading the EXIF clock as IST. That gives 2:30 pm, which is 5 h 30 min off.
