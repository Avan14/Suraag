# Case ts-task-301-l1: worked solution (instructor copy)

> SYNTHETIC CASE - fictional, for teaching only. Not real data. This file contains the answers.

Level 1 · Rookie. Add up only what the victim paid: commission credits and an unpaid demand are not deposits.

## Q1. Who asked the victim to make the deposits?

1. chat.txt:10: at 3:36 pm, Mentor Mamta writes: "Task 3 is a prepaid task: deposit Rs 2,000 to unlock it. You get it back with commission."
2. calls.csv:1: "Mentor Mamta" is saved in the call log as +91-56160-29384, and that number called at 15:35, just before the message.
3. The brief lists +91-56160-29384 as Mamta Sen.

**Answer: Mamta Sen.**

## Q2. How much money did the victim deposit in total, in rupees?

1. chat.txt:11: at 3:41 pm the victim writes that Rs 2,000 was paid.
2. chat.txt:13: at 3:52 pm the victim writes that Rs 5,000 was paid.
3. chat.txt:16: at 4:04 pm the victim writes that Rs 8,000 was paid.
4. chat.txt:17 asks for Rs 40,000 more, but chat.txt:18 shows the victim did not pay it.
5. Add the deposits: Rs 2,000 + Rs 5,000 + Rs 8,000 = Rs 15,000.

**Answer: Rs 15,000.**

- Trap: adding the commission credits too. Those were paid to the victim as bait; counting them gives Rs 15,360.
- Trap: adding every demand. The last demand, chat.txt:17, was never paid; adding it gives Rs 55,000.

## Q3. Where was the victim when the photo on their phone was taken?

1. photo.jpg:GPSLatitude, photo.jpg:GPSLongitude: the photo's GPS reads 18.5679, 73.9139.
2. That point is 42 m from Viman Nagar. The next nearest place, Hadapsar, is 6.7 km away.

**Answer: Viman Nagar.**
