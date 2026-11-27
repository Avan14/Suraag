# Case upi-ring-043-l4: worked solution (instructor copy)

> SYNTHETIC CASE - fictional, for teaching only. Not real data. This file contains the answers.

Level 4 · Expert. Everything from levels 2 and 3 in one longer case.

## Q1. Who told the mule to delete the transfer record?

1. chat.txt:6: Nilesh ji sets a code. When anyone writes "the blue kite is up", the payment entry is to be deleted. This line is a rule, not the order.
2. chat.txt:17: at 6:53 pm, Debashish ji uses the code "the blue kite is up", so this is the actual order: "Anita ji, as I said on the phone just now, the blue kite is up."
3. chat.txt:18: at 6:55 pm the mule replies, so the order was carried out: "Done. All cleared from my side."
4. chat.txt:19 also asks to remove an entry, but it comes after that reply and is about a different list, so it is not the order.
5. The call log has no contact saved as "Debashish ji", but the order says it follows a phone call. calls.csv:4 is the only answered call in the 2 minutes before it, from the unsaved number +91-58961-99000.
6. The brief lists +91-58961-99000 as Debashish Roy.
7. Two suspects share the first name Debashish, so the chat name alone cannot decide. The number does.

**Answer: Debashish Roy.**

- Trap: matching by first name. "Debashish B." in the call log looks like "Debashish ji", but that number belongs to Debashish Bose.
- Trap: taking the latest request. chat.txt:19 came after the mule had already replied, and it points at Debashish Bose.

## Q2. When was the instruction given?

1. chat.txt:6: Nilesh ji sets a code. When anyone writes "the blue kite is up", the payment entry is to be deleted. This line is a rule, not the order.
2. chat.txt:17: at 6:53 pm, Debashish ji uses the code "the blue kite is up", so this is the actual order: "Anita ji, as I said on the phone just now, the blue kite is up."
3. chat.txt:18: at 6:55 pm the mule replies, so the order was carried out: "Done. All cleared from my side."
4. chat.txt:19 also asks to remove an entry, but it comes after that reply and is about a different list, so it is not the order.
5. calls.csv:4 at 18:51 agrees with the chat time within 2 minutes.

**Answer: 6:53 pm.**

- Trap: searching for the word "delete". The first hit, chat.txt:6 at 6:15 pm, only sets up the code.

## Q3. Where was the mule when the payment screenshot photo was taken?

1. photo.jpg:GPSLatitude, photo.jpg:GPSLongitude: the photo's GPS reads 18.5077, 73.8075.
2. That point is 39 m from Kothrud. The next nearest place, Baner, is 6.1 km away.
3. chat.txt:21: the mule claims to be at Kharadi. A chat message is a claim; the GPS is written by the phone, and ModifyDate equals DateTimeOriginal, so the photo shows no sign of later editing.

**Answer: Kothrud.**

- Trap: believing the chat. chat.txt:21 names Kharadi, but the phone's GPS puts the photo elsewhere.

## Q4. At what time (IST) was the payment screenshot photo taken?

1. photo.jpg:DateTimeOriginal: the camera clock says 2026:03:25 13:42:00.
2. photo.jpg:OffsetTimeOriginal: the offset is +00:00, so that clock was not on IST (+05:30).
3. IST is +05:30, so shift the clock by +5 h 30 min: 13:42 becomes 7:12 pm.

**Answer: 7:12 pm.**

- Trap: reading the EXIF clock as IST. That gives 1:42 pm, which is 5 h 30 min off.
