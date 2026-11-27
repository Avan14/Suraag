# Case upi-ring-022-l2: worked solution (instructor copy)

> SYNTHETIC CASE - fictional, for teaching only. Not real data. This file contains the answers.

Level 2 · Investigator. Link a message to a phone call when the caller is not saved, and trust the phone's GPS over a claim in the chat.

## Q1. Mule ko transfer record delete karne ko kisne kaha?

1. chat.txt:15: at 7:27 pm, Kavita didi writes to the mule: "Venkat bhai, jaise abhi phone pe bola, ye entry abhi delete kar do, kisi ko mat batana"
2. The call log has no contact saved as "Kavita didi", but the order says it follows a phone call. calls.csv:5 is the only answered call in the 2 minutes before it, from the unsaved number +91-52934-72351.
3. The brief lists +91-52934-72351 as Kavita Mehta.
4. Two suspects share the first name Kavita, so the chat name alone cannot decide. The number does.

**Answer: Kavita Mehta.**

- Trap: matching by first name. "Kavita V." in the call log looks like "Kavita didi", but that number belongs to Kavita Verma.

## Q2. Ye instruction kab diya gaya?

1. chat.txt:15: at 7:27 pm, Kavita didi writes to the mule: "Venkat bhai, jaise abhi phone pe bola, ye entry abhi delete kar do, kisi ko mat batana"
2. calls.csv:5 at 19:26 agrees with the chat time within 2 minutes.

**Answer: 7:27 pm.**

## Q3. Payment screenshot wali photo li gayi tab mule kahan tha?

1. photo.jpg:GPSLatitude, photo.jpg:GPSLongitude: the photo's GPS reads 19.0724, 72.8843.
2. That point is 31 m from Kurla West. The next nearest place, Bandra West, is 5.9 km away.
3. chat.txt:19: the mule claims to be at Dadar. A chat message is a claim; the GPS is written by the phone, and ModifyDate equals DateTimeOriginal, so the photo shows no sign of later editing.

**Answer: Kurla West.**

- Trap: believing the chat. chat.txt:19 names Dadar, but the phone's GPS puts the photo elsewhere.
