# Case upi-ring-041-l4: worked solution (instructor copy)

> SYNTHETIC CASE - fictional, for teaching only. Not real data. This file contains the answers.

Level 4 · Expert. Everything from levels 2 and 3 in one longer case.

## Q1. Who told the mule to delete the transfer record?

1. chat.txt:7: Karthik ji sets a code. When anyone writes "the blue kite is up", the payment entry is to be deleted. This line is a rule, not the order.
2. chat.txt:19: at 8:51 pm, Prakash ji uses the code "the blue kite is up", so this is the actual order: "Jignesh ji, as I said on the phone just now, the blue kite is up, understood?"
3. chat.txt:20: at 8:53 pm the mule replies, so the order was carried out: "Done. All cleared from my side."
4. chat.txt:25 also asks to remove an entry, but it comes after that reply and is about a different list, so it is not the order.
5. The call log has no contact saved as "Prakash ji", but the order says it follows a phone call. calls.csv:4 is the only answered call in the 2 minutes before it, from the unsaved number +91-54219-85806.
6. The brief lists +91-54219-85806 as Prakash Mehta.
7. Two suspects share the first name Prakash, so the chat name alone cannot decide. The number does.

**Answer: Prakash Mehta.**

- Trap: matching by first name. "Prakash C." in the call log looks like "Prakash ji", but that number belongs to Prakash Chauhan.
- Trap: taking the latest request. chat.txt:25 came after the mule had already replied, and it points at Prakash Chauhan.

## Q2. When was the instruction given?

1. chat.txt:7: Karthik ji sets a code. When anyone writes "the blue kite is up", the payment entry is to be deleted. This line is a rule, not the order.
2. chat.txt:19: at 8:51 pm, Prakash ji uses the code "the blue kite is up", so this is the actual order: "Jignesh ji, as I said on the phone just now, the blue kite is up, understood?"
3. chat.txt:20: at 8:53 pm the mule replies, so the order was carried out: "Done. All cleared from my side."
4. chat.txt:25 also asks to remove an entry, but it comes after that reply and is about a different list, so it is not the order.
5. calls.csv:4 at 20:50 agrees with the chat time within 2 minutes.

**Answer: 8:51 pm.**

- Trap: searching for the word "delete". The first hit, chat.txt:7 at 8:14 pm, only sets up the code.

## Q3. Where was the mule when the payment screenshot photo was taken?

1. photo.jpg:GPSLatitude, photo.jpg:GPSLongitude: the photo's GPS reads 18.5592, 73.7872.
2. That point is 48 m from Baner. The next nearest place, Kothrud, is 6.2 km away.
3. chat.txt:27: the mule claims to be at Kharadi. A chat message is a claim; the GPS is written by the phone, and ModifyDate equals DateTimeOriginal, so the photo shows no sign of later editing.

**Answer: Baner.**

- Trap: believing the chat. chat.txt:27 names Kharadi, but the phone's GPS puts the photo elsewhere.

## Q4. At what time (IST) was the payment screenshot photo taken?

1. photo.jpg:DateTimeOriginal: the camera clock says 2026:04:14 15:49:00.
2. photo.jpg:OffsetTimeOriginal: the offset is +00:00, so that clock was not on IST (+05:30).
3. IST is +05:30, so shift the clock by +5 h 30 min: 15:49 becomes 9:19 pm.

**Answer: 9:19 pm.**

- Trap: reading the EXIF clock as IST. That gives 3:49 pm, which is 5 h 30 min off.
