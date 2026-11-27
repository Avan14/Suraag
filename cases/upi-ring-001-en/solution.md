# Case upi-ring-001: worked solution (instructor copy)

> SYNTHETIC CASE - fictional, for teaching only. Not real data. This file contains the answers.

Level 1 · Rookie. Read a chat line, match a saved contact to its number, place a GPS point.

## Q1. Who told the mule to delete the transfer record?

1. chat.txt:13: at 6:58 pm, Prakash ji writes to the mule: "Mahesh ji, delete the transfer record right now"
2. calls.csv:4: "Prakash ji" is saved in the call log as +91-57297-34908 and called at 18:57, just before the order.
3. The brief lists +91-57297-34908 as Prakash Joshi.

**Answer: Prakash Joshi.**

## Q2. When was the instruction given?

1. chat.txt:13: at 6:58 pm, Prakash ji writes to the mule: "Mahesh ji, delete the transfer record right now"
2. calls.csv:4 at 18:57 agrees with the chat time within 2 minutes.

**Answer: 6:58 pm.**

## Q3. Where was the mule when the payment screenshot photo was taken?

1. photo.jpg:GPSLatitude, photo.jpg:GPSLongitude: the photo's GPS reads 18.5589, 73.7869.
2. That point is 15 m from Baner. The next nearest place, Shivajinagar, is 7.1 km away.

**Answer: Baner.**
