# Case da-arrest-101-l1: worked solution (instructor copy)

> SYNTHETIC CASE - fictional, for teaching only. Not real data. This file contains the answers.

Level 1 · Rookie. Link a demand to a phone number, see past the first caller, and tell from EXIF dates whether a photo was edited.

## Q1. Who told the victim to transfer money to the 'safe account'?

1. chat.txt:15: at 11:38 am, Officer Ghosh writes: "Hetal, transfer your full balance to the safe account for verification now. It will be returned after checking."
2. calls.csv:3: "Officer Ghosh" is saved in the call log as +91-59083-50355, and that number called at 11:36, just before the message.
3. The brief lists +91-59083-50355 as Rina Ghosh.

**Answer: Rina Ghosh.**

- Trap: blaming the first caller. calls.csv:1 is the first call, from Nilesh Kulkarni, who only passed the victim on. The demand came later, from another number.

## Q2. When was that demand made?

1. chat.txt:15: at 11:38 am, Officer Ghosh writes: "Hetal, transfer your full balance to the safe account for verification now. It will be returned after checking."
2. calls.csv:3 at 11:36 agrees with the chat time within 2 minutes.

**Answer: 11:38 am.**

## Q3. Was the officer's ID-card photo edited after it was taken?

1. photo.jpg:DateTimeOriginal: the picture was taken at 2026:03:20 18:15:00.
2. photo.jpg:ModifyDate: the file was last saved at 2026:04:16 10:56:00.
3. photo.jpg:Software: the Software tag reads "Generic Photo Editor 2.1".
4. ModifyDate is later than DateTimeOriginal, so the file was saved again after it was taken: it was edited.

**Answer: yes.**

- Trap: trusting DateTimeOriginal alone. It still shows when the picture was first taken; only ModifyDate shows the later save.
