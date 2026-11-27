# Case da-arrest-102-l2: worked solution (instructor copy)

> SYNTHETIC CASE - fictional, for teaching only. Not real data. This file contains the answers.

Level 2 · Investigator. As tier 1, plus: a forwarded warning is not a demand, and an edited file need not carry a Software tag.

## Q1. Victim ko 'safe account' mein paise transfer karne ko kisne kaha?

1. chat.txt:15: Raju bhai forwards a warning that quotes the same words. It is advice, not a demand.
2. chat.txt:17: at 12:01 pm, Bose Sir writes: "Revathi ji, apna poora balance abhi verification ke liye safe account mein transfer karo. Checking ke baad wapas mil jayega."
3. calls.csv:4: "Bose Sir" is saved in the call log as +91-56703-70730, and that number called at 12:00, just before the message.
4. The brief lists +91-56703-70730 as Tanuja Bose.

**Answer: Tanuja Bose.**

- Trap: blaming the first caller. calls.csv:1 is the first call, from Mahesh Patil, who only passed the victim on. The demand came later, from another number.
- Trap: searching for the words. The first hit, chat.txt:15, is a warning Raju Sharma forwarded, not a demand.

## Q2. Ye demand kab ki gayi?

1. chat.txt:17: at 12:01 pm, Bose Sir writes: "Revathi ji, apna poora balance abhi verification ke liye safe account mein transfer karo. Checking ke baad wapas mil jayega."
2. calls.csv:4 at 12:00 agrees with the chat time within 2 minutes.

**Answer: 12:01 pm.**

## Q3. Kya officer ke ID card ki photo li jaane ke baad edit ki gayi thi?

1. photo.jpg:DateTimeOriginal: the picture was taken at 2026:06:26 15:18:00.
2. photo.jpg:ModifyDate: the file was last saved at 2026:07:22 11:15:00.
3. ModifyDate is later than DateTimeOriginal, so the file was saved again after it was taken: it was edited.

**Answer: yes.**

- Trap: looking only for a Software tag. There is none, yet ModifyDate is later than DateTimeOriginal, so the file was edited.
