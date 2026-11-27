# Case da-arrest-103-l2: worked solution (instructor copy)

> SYNTHETIC CASE - fictional, for teaching only. Not real data. This file contains the answers.

Level 2 · Investigator. As tier 1, plus: a forwarded warning is not a demand, and an edited file need not carry a Software tag.

## Q1. Who told the victim to transfer money to the 'safe account'?

1. chat.txt:10: Prakash ji forwards a warning that quotes the same words. It is advice, not a demand.
2. chat.txt:14: at 3:17 pm, Officer Menon writes: "Abhijit, transfer your full balance to the safe account for verification now. It will be returned after checking."
3. calls.csv:4: "Officer Menon" is saved in the call log as +91-58438-90797, and that number called at 15:15, just before the message.
4. The brief lists +91-58438-90797 as Karthik Menon.

**Answer: Karthik Menon.**

- Trap: blaming the first caller. calls.csv:1 is the first call, from Mahesh Shinde, who only passed the victim on. The demand came later, from another number.
- Trap: searching for the words. The first hit, chat.txt:10, is a warning Prakash Desai forwarded, not a demand.

## Q2. When was that demand made?

1. chat.txt:14: at 3:17 pm, Officer Menon writes: "Abhijit, transfer your full balance to the safe account for verification now. It will be returned after checking."
2. calls.csv:4 at 15:15 agrees with the chat time within 2 minutes.

**Answer: 3:17 pm.**

## Q3. Was the officer's ID-card photo edited after it was taken?

1. photo.jpg:DateTimeOriginal: the picture was taken at 2026:07:08 10:15:00.
2. photo.jpg:ModifyDate: the file was last saved at 2026:07:21 14:43:00.
3. ModifyDate is later than DateTimeOriginal, so the file was saved again after it was taken: it was edited.

**Answer: yes.**

- Trap: looking only for a Software tag. There is none, yet ModifyDate is later than DateTimeOriginal, so the file was edited.
