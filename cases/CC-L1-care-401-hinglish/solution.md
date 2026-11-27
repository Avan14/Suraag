# Case cc-care-401-l1: worked solution (instructor copy)

> SYNTHETIC CASE - fictional, for teaching only. Not real data. This file contains the answers.

Level 1 · Rookie. Build a timeline: which call led to the install, and when control of the phone passed.

## Q1. Victim ko screen-sharing app install karne ko kisne kaha?

1. chat.txt:7: at 4:59 pm, +91-59607-25532 writes: "Mamta ji, maine jo link bheja usse support app install karo aur screen pe jo code aaye wo batao."
2. calls.csv:2: the sender is not saved, so the export shows the number itself. +91-59607-25532 called at 16:57, just before the message.
3. The brief lists +91-59607-25532 as Nilesh Shinde.

**Answer: Nilesh Shinde.**

- Trap: blaming the number the victim dialled. calls.csv:1 is the victim's call to Tanuja Banerjee, who only took the complaint. The install request came from the number that called back.

## Q2. Victim ne phone ka control kab saunpa (screen ka code kab bataya)?

1. chat.txt:7: at 4:59 pm, +91-59607-25532 writes: "Mamta ji, maine jo link bheja usse support app install karo aur screen pe jo code aaye wo batao."
2. chat.txt:8: at 5:06 pm the victim reads out the code on the screen, which hands over control: "Install ho gaya. Code hai 946 930."

**Answer: 5:06 pm.**

- Trap: taking the install request as the handover. chat.txt:7 at 4:59 pm only asks for the install; control passed when the victim read out the code.

## Q3. Phone wali photo li gayi tab victim kahan tha?

1. photo.jpg:GPSLatitude, photo.jpg:GPSLongitude: the photo's GPS reads 19.0597, 72.8298.
2. That point is 33 m from Bandra West. The next nearest place, Kurla West, is 5.9 km away.

**Answer: Bandra West.**
