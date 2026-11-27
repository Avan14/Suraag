# Case ts-task-302-l2: worked solution (instructor copy)

> SYNTHETIC CASE - fictional, for teaching only. Not real data. This file contains the answers.

Level 2 · Investigator. As tier 1, plus: the recruiter who called first is not the one who asked for the deposits.

## Q1. Victim ko deposit karne ko kisne kaha?

1. chat.txt:11: at 11:00 am, Mentor Prakash writes: "Task 3 prepaid task hai: unlock karne ke liye Rs 1,500 deposit karo. Commission ke saath wapas milega."
2. calls.csv:3: "Mentor Prakash" is saved in the call log as +91-51891-20637, and that number called at 10:58, just before the message.
3. The brief lists +91-51891-20637 as Prakash Kulkarni.

**Answer: Prakash Kulkarni.**

- Trap: blaming the first caller. calls.csv:1 is the first call, from Vikram Gupta, who only passed the victim on. The demand came later, from another number.

## Q2. Victim ne kul kitne rupaye deposit kiye?

1. chat.txt:12: at 11:05 am the victim writes that Rs 1,500 was paid.
2. chat.txt:15: at 11:17 am the victim writes that Rs 4,000 was paid.
3. chat.txt:17: at 11:28 am the victim writes that Rs 12,000 was paid.
4. chat.txt:19: at 11:40 am the victim writes that Rs 20,000 was paid.
5. chat.txt:21 asks for Rs 30,000 more, but chat.txt:22 shows the victim did not pay it.
6. Add the deposits: Rs 1,500 + Rs 4,000 + Rs 12,000 + Rs 20,000 = Rs 37,500.

**Answer: Rs 37,500.**

- Trap: adding the commission credits too. Those were paid to the victim as bait; counting them gives Rs 38,100.
- Trap: adding every demand. The last demand, chat.txt:21, was never paid; adding it gives Rs 67,500.

## Q3. Phone wali photo li gayi tab victim kahan tha?

1. photo.jpg:GPSLatitude, photo.jpg:GPSLongitude: the photo's GPS reads 19.0726, 72.8848.
2. That point is 32 m from Kurla West. The next nearest place, Dadar, is 7.2 km away.

**Answer: Kurla West.**
