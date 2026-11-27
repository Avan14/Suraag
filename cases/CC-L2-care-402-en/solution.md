# Case cc-care-402-l2: worked solution (instructor copy)

> SYNTHETIC CASE - fictional, for teaching only. Not real data. This file contains the answers.

Level 2 · Investigator. As tier 1, plus: a forwarded warning is not a demand.

## Q1. Who asked the victim to install the screen-sharing app?

1. chat.txt:7: Pooja ji forwards a warning that quotes the same words. It is advice, not a demand.
2. chat.txt:8: at 2:41 pm, +91-55788-74959 writes: "Raju, install the support app from the link I sent and tell me the code on your screen."
3. calls.csv:3: the sender is not saved, so the export shows the number itself. +91-55788-74959 called at 14:40, just before the message.
4. The brief lists +91-55788-74959 as Suresh Iyer.

**Answer: Suresh Iyer.**

- Trap: blaming the number the victim dialled. calls.csv:1 is the victim's call to Sanjay Mehta, who only took the complaint. The install request came from the number that called back.
- Trap: searching for the words. The first hit, chat.txt:7, is a warning Pooja Yadav forwarded, not a demand.

## Q2. When did the victim hand over control of the phone (read out the code on the screen)?

1. chat.txt:8: at 2:41 pm, +91-55788-74959 writes: "Raju, install the support app from the link I sent and tell me the code on your screen."
2. chat.txt:9: at 2:48 pm the victim reads out the code on the screen, which hands over control: "Installed. The code is 268 803."

**Answer: 2:48 pm.**

- Trap: taking the install request as the handover. chat.txt:8 at 2:41 pm only asks for the install; control passed when the victim read out the code.

## Q3. Where was the victim when the photo on their phone was taken?

1. photo.jpg:GPSLatitude, photo.jpg:GPSLongitude: the photo's GPS reads 18.5588, 73.7866.
2. That point is 31 m from Baner. The next nearest place, Kothrud, is 6.1 km away.

**Answer: Baner.**
