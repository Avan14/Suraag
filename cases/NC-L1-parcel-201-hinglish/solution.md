# Case nc-parcel-201-l1: worked solution (instructor copy)

> SYNTHETIC CASE - fictional, for teaching only. Not real data. This file contains the answers.

Level 1 · Rookie. Report only what the files show: an unknown caller is not a culprit, and 'no one' can be the right answer.

## Q1. Victim ko 'safe account' mein paise transfer karne ko kisne kaha?

1. chat.txt:10: the unknown number +91-55651-77994 writes only: "Namaste, aapka parcel gate pe deliver ho gaya hai. Delivery ke proof ke liye photo lagayi hai."
2. calls.csv:1: the sender is not saved, so the export shows the number itself. +91-55651-77994 called at 14:36, just before the message.
3. No other line asks the victim to move money. Without such a line no one can be named.

**Answer: no one (the files hold no such instruction).**

- Trap: treating the unknown caller as the culprit. calls.csv:1 is from Debashish Banerjee, but that number only delivered a parcel and asked for nothing.

## Q2. Kya delivery wali photo li jaane ke baad edit ki gayi thi?

1. photo.jpg:DateTimeOriginal: the picture was taken at 2026:05:28 14:37:00.
2. photo.jpg:ModifyDate: the file was last saved at 2026:05:28 14:37:00.
3. ModifyDate equals DateTimeOriginal, so the file was not saved again after it was taken.

**Answer: no.**

## Q3. Delivery wali photo kahan li gayi thi?

1. photo.jpg:GPSLatitude, photo.jpg:GPSLongitude: the photo's GPS reads 19.0175, 72.8475.
2. That point is 46 m from Dadar. The next nearest place, Bandra West, is 5.0 km away.

**Answer: Dadar.**
