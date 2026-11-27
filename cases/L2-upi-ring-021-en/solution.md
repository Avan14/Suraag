# Case upi-ring-021-l2: worked solution (instructor copy)

> SYNTHETIC CASE - fictional, for teaching only. Not real data. This file contains the answers.

Level 2 · Investigator. Link a message to a phone call when the caller is not saved, and trust the phone's GPS over a claim in the chat.

## Q1. Who told the mule to delete the transfer record?

1. chat.txt:17: at 9:08 pm, Debashish ji writes to the mule: "Sanjay ji, as I said on the phone just now, please delete that entry now and tell nobody"
2. The call log has no contact saved as "Debashish ji", but the order says it follows a phone call. calls.csv:5 is the only answered call in the 2 minutes before it, from the unsaved number +91-57239-04465.
3. The brief lists +91-57239-04465 as Debashish Bose.
4. Two suspects share the first name Debashish, so the chat name alone cannot decide. The number does.

**Answer: Debashish Bose.**

- Trap: matching by first name. "Debashish V." in the call log looks like "Debashish ji", but that number belongs to Debashish Verma.

## Q2. When was the instruction given?

1. chat.txt:17: at 9:08 pm, Debashish ji writes to the mule: "Sanjay ji, as I said on the phone just now, please delete that entry now and tell nobody"
2. calls.csv:5 at 21:07 agrees with the chat time within 2 minutes.

**Answer: 9:08 pm.**

## Q3. Where was the mule when the payment screenshot photo was taken?

1. photo.jpg:GPSLatitude, photo.jpg:GPSLongitude: the photo's GPS reads 18.5308, 73.8478.
2. That point is 32 m from Shivajinagar. The next nearest place, Hadapsar, is 8.6 km away.
3. chat.txt:20: the mule claims to be at Hadapsar. A chat message is a claim; the GPS is written by the phone, and ModifyDate equals DateTimeOriginal, so the photo shows no sign of later editing.

**Answer: Shivajinagar.**

- Trap: believing the chat. chat.txt:20 names Hadapsar, but the phone's GPS puts the photo elsewhere.
