# Case upi-ring-023-l2: worked solution (instructor copy)

> SYNTHETIC CASE - fictional, for teaching only. Not real data. This file contains the answers.

Level 2 · Investigator. Link a message to a phone call when the caller is not saved, and trust the phone's GPS over a claim in the chat.

## Q1. Who told the mule to delete the transfer record?

1. chat.txt:15: at 9:44 pm, Venkat ji writes to the mule: "Lakshmi ji, as I said on the phone just now, delete the transfer record right now"
2. The call log has no contact saved as "Venkat ji", but the order says it follows a phone call. calls.csv:5 is the only answered call in the 2 minutes before it, from the unsaved number +91-50230-28972.
3. The brief lists +91-50230-28972 as Venkat Nair.
4. Two suspects share the first name Venkat, so the chat name alone cannot decide. The number does.

**Answer: Venkat Nair.**

- Trap: matching by first name. "Venkat G." in the call log looks like "Venkat ji", but that number belongs to Venkat Ghosh.

## Q2. When was the instruction given?

1. chat.txt:15: at 9:44 pm, Venkat ji writes to the mule: "Lakshmi ji, as I said on the phone just now, delete the transfer record right now"
2. calls.csv:5 at 21:43 agrees with the chat time within 2 minutes.

**Answer: 9:44 pm.**

## Q3. Where was the mule when the payment screenshot photo was taken?

1. photo.jpg:GPSLatitude, photo.jpg:GPSLongitude: the photo's GPS reads 18.5591, 73.7867.
2. That point is 15 m from Baner. The next nearest place, Viman Nagar, is 13.5 km away.
3. chat.txt:23: the mule claims to be at Kharadi. A chat message is a claim; the GPS is written by the phone, and ModifyDate equals DateTimeOriginal, so the photo shows no sign of later editing.

**Answer: Baner.**

- Trap: believing the chat. chat.txt:23 names Kharadi, but the phone's GPS puts the photo elsewhere.
