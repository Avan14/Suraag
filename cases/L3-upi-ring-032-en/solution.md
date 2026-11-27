# Case upi-ring-032-l3: worked solution (instructor copy)

> SYNTHETIC CASE - fictional, for teaching only. Not real data. This file contains the answers.

Level 3 · Inspector. Decode a code word set up earlier, find the order that was actually carried out, and convert a camera clock to IST.

## Q1. Who told the mule to delete the transfer record?

1. chat.txt:6: Rina ji sets a code. When anyone writes "the mangoes are ripe", the payment entry is to be deleted. This line is a rule, not the order.
2. chat.txt:16: at 7:24 pm, Sanjay ji uses the code "the mangoes are ripe", so this is the actual order: "Revathi ji, the mangoes are ripe."
3. chat.txt:17: at 7:26 pm the mule replies, so the order was carried out: "Done, it's gone. Nobody will see it now."
4. chat.txt:19 also asks to remove an entry, but it comes after that reply and is about a different list, so it is not the order.
5. calls.csv:4: "Sanjay ji" is saved in the call log as +91-52071-68768 and called at 19:23, just before the order.
6. The brief lists +91-52071-68768 as Sanjay Mehta.
7. Two suspects share the first name Sanjay, so the chat name alone cannot decide. The number does.

**Answer: Sanjay Mehta.**

- Trap: taking the latest request. chat.txt:19 came after the mule had already replied, and it points at Sanjay Ghosh.

## Q2. When was the instruction given?

1. chat.txt:6: Rina ji sets a code. When anyone writes "the mangoes are ripe", the payment entry is to be deleted. This line is a rule, not the order.
2. chat.txt:16: at 7:24 pm, Sanjay ji uses the code "the mangoes are ripe", so this is the actual order: "Revathi ji, the mangoes are ripe."
3. chat.txt:17: at 7:26 pm the mule replies, so the order was carried out: "Done, it's gone. Nobody will see it now."
4. chat.txt:19 also asks to remove an entry, but it comes after that reply and is about a different list, so it is not the order.
5. calls.csv:4 at 19:23 agrees with the chat time within 2 minutes.

**Answer: 7:24 pm.**

- Trap: searching for the word "delete". The first hit, chat.txt:6 at 6:46 pm, only sets up the code.

## Q3. Where was the mule when the payment screenshot photo was taken?

1. photo.jpg:GPSLatitude, photo.jpg:GPSLongitude: the photo's GPS reads 18.5072, 73.8077.
2. That point is 22 m from Kothrud. The next nearest place, Shivajinagar, is 4.9 km away.

**Answer: Kothrud.**

## Q4. At what time (IST) was the payment screenshot photo taken?

1. photo.jpg:DateTimeOriginal: the camera clock says 2026:04:16 14:19:00.
2. photo.jpg:OffsetTimeOriginal: the offset is +00:00, so that clock was not on IST (+05:30).
3. IST is +05:30, so shift the clock by +5 h 30 min: 14:19 becomes 7:49 pm.

**Answer: 7:49 pm.**

- Trap: reading the EXIF clock as IST. That gives 2:19 pm, which is 5 h 30 min off.
