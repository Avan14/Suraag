# Case nc-parcel-202-l2: worked solution (instructor copy)

> SYNTHETIC CASE - fictional, for teaching only. Not real data. This file contains the answers.

Level 2 · Investigator. As tier 1, plus: a forwarded warning is not a demand, and a phone's own firmware in the Software tag is not an edit.

## Q1. Who told the victim to transfer money to a 'safe account'?

1. chat.txt:19: Subhash ji forwards a warning that quotes the same words. It is advice, not a demand.
2. chat.txt:12: the unknown number +91-55750-39441 writes only: "Hello, your parcel is delivered at the gate. Photo attached as proof of delivery."
3. calls.csv:1: the sender is not saved, so the export shows the number itself. +91-55750-39441 called at 14:39, just before the message.
4. No other line asks the victim to move money. Without such a line no one can be named.

**Answer: no one (the files hold no such instruction).**

- Trap: treating the unknown caller as the culprit. calls.csv:1 is from Abhijit Roy, but that number only delivered a parcel and asked for nothing.
- Trap: searching for the words. The first hit, chat.txt:19, is a warning Subhash Sen forwarded, not a demand.

## Q2. Was the delivery photo edited after it was taken?

1. photo.jpg:DateTimeOriginal: the picture was taken at 2026:08:29 14:39:00.
2. photo.jpg:ModifyDate: the file was last saved at 2026:08:29 14:39:00.
3. photo.jpg:Software: the Software tag reads "Vivo camera firmware 13.9.12".
4. ModifyDate equals DateTimeOriginal, so the file was not saved again after it was taken.

**Answer: no.**

- Trap: treating any Software tag as an editor. "Vivo camera firmware 13.9.12" is the phone's own camera firmware, and ModifyDate equals DateTimeOriginal.

## Q3. Where was the delivery photo taken?

1. photo.jpg:GPSLatitude, photo.jpg:GPSLongitude: the photo's GPS reads 18.5088, 73.9263.
2. That point is 34 m from Hadapsar. The next nearest place, Kharadi, is 5.2 km away.

**Answer: Hadapsar.**
