# Case families

Suraag began with one crime: a UPI-fraud ring, seen from a money mule's phone. The case families add four
more, each seen from the **victim's** phone. They are modelled on how Indian authorities describe these frauds
in public advisories. The description stays at the level of evidence a phone would hold, so a student learns
to read it. It is not a guide to running a scam. Everything in the cases is synthetic: people, numbers
(`+91-5xxxx-xxxxx`, never a valid mobile number), places and amounts.

Each family uses the same machinery as the UPI levels. Code writes every evidence line verbatim, and an LLM
writes only harmless family small talk between those lines. A rule-based solver reads only the files and the
student brief, and must reproduce the answer key before a case ships. Every trap is a named shortcut that the
depth check runs, and the case fails unless that shortcut gives a real wrong answer. Hints and worked solutions
are built in code. The code is in `suraag/families.py`.

The files are the same in every family:

- `chat.txt`: the victim's WhatsApp messages from that day, all chats in one file and in time order. A sender
  the victim never saved shows up as a phone number, as it does in a real export.
- `calls.csv`: the victim's call log.
- `photo.jpg`: one photo, either received by the victim or taken on their phone. It is a CC0 stock scene
  (credits in `suraag/data/photos/CREDITS.md`) with the case's own EXIF and a visible SYNTHETIC mark.

Every family has two tiers. Tier 1 sets one or two traps, and tier 2 adds more. Case folders are named
`<FAMILY>-L<tier>-...`, for example `cases/DA-L2-arrest-102-hinglish`.

## Digital arrest (DA)

**How it works.** A call that sounds routine, often about a parcel or a KYC check, turns into an accusation:
the victim's name is said to be linked to drugs, money laundering or another serious crime. The caller passes
the victim to someone posing as an officer of the police, CBI, ED, customs or another agency. That "officer"
keeps the victim on a video call, sends fake documents or ID cards to look genuine, and tells the victim to
speak to no one. Finally the victim is told to move money, as a "fine", a "security deposit" or into an
account for "verification", and the money is gone. Real agencies do not arrest anyone over a video call.

**What the victim's phone holds.** A first call from an unknown number, then calls from the "officer". A
chat with that officer, containing the ID card photo and the line that demands the transfer. Missed calls
from family while the victim was told to stay on the line. Sometimes a family member forwards an official
warning about exactly this scam.

**What the case teaches.** How to link the demand to a phone number through the call log, and how to look
past the first caller. It also teaches the tamper question: **was the officer's ID-card photo edited after it
was taken?** The answer comes from EXIF. If `ModifyDate` is later than `DateTimeOriginal`, the file was saved
again after capture. The ID card is drawn by code, plainly marked SAMPLE / FICTIONAL, with no emblem, logo,
seal or real officer's name.

**Questions.** Who demanded the transfer, when, and was the ID photo edited (yes/no).

**Traps.**

| Tier | Trap | Shortcut, and where it leads |
|---|---|---|
| 1, 2 | handover | Blame the first unknown caller: that is the person who passed the victim on, not the one who made the demand. |
| 1 | camera_original | Trust `DateTimeOriginal` and answer "not edited". It shows when the picture was taken, not when the file was last saved. |
| 2 | forwarded | Search for "safe account" and take the first hit, which is a warning a relative forwarded. |
| 2 | software_tag | Look only for a `Software` tag. There is none, but `ModifyDate` still shows the edit. |

## Nothing happened: the control case (NC)

**Why it exists.** A real investigator has to say "the files do not show that" as often as they name
someone. In this case a courier calls from an unknown number, delivers a parcel and sends a delivery photo.
Later a relative forwards a warning about parcel scams, and the worried victim reports the day. No line asks
the victim to move any money.

**What the case teaches.** Report only what the files show. The student answer form always offers "No one:
there is no such instruction", on every case, so the option never gives the control case away. The photo
question has the opposite answer to digital arrest: the delivery photo was **not** edited.

**Questions.** Who told the victim to move money to a safe account (the answer is no one), was the delivery
photo edited (no), and where was it taken.

**Traps.**

| Tier | Trap | Shortcut, and where it leads |
|---|---|---|
| 1, 2 | stranger_call | Treat the unknown caller as the culprit, which names the courier. |
| 2 | forwarded | Search for "safe account": the only hit is the relative's forwarded warning, which names the relative. |
| 2 | software_tag | Treat any `Software` tag as an editor. Here it holds the phone's own camera firmware, and `ModifyDate` equals `DateTimeOriginal`. |

## Job / task scam (TS)

**How it works.** An advert or message offers part-time work from home ("ghar baithe job"): like videos, or
rate hotels and map listings. An agent makes contact on WhatsApp or Telegram. The first tasks pay a small
commission, which builds trust. Then come "prepaid" tasks: the victim must deposit money to unlock each one,
the amounts climb, and a final demand (a "tax" or "fee" before withdrawal) is the point where the victim stops
or runs out. Once a larger sum is in, it is frozen and lost.

**What the victim's phone holds.** The job offer from an unknown number. Messages from a "mentor" announcing
commissions credited, then demands to deposit escalating amounts. The victim's own "Paid Rs ..." replies,
the final demand the victim cannot pay, and a call from the mentor around the first demand.

**What the case teaches.** The **amount** question: how much did the victim deposit in total? Only the
victim's own payment lines count. The answer needs every deposit line cited.

**Questions.** Who asked for the deposits, and the total deposited (amount); plus where a photo was taken.

**Traps.**

| Tier | Trap | Shortcut, and where it leads |
|---|---|---|
| 1, 2 | payout | Add the commission credits too. They were paid **to** the victim as bait. |
| 1, 2 | escalation | Add every demand, including the last one the victim never paid. |
| 2 | handover | Blame the recruiter who called first, not the mentor who asked for the deposits. |

## Fake customer care / remote access (CC)

**How it works.** A customer searches online for a bank's or company's helpline and calls a number that
fraudsters have placed in the search results. The "desk" registers a complaint and promises a callback. A
"technician" then calls and asks the customer to install a screen-sharing or remote-access app and read out
the code it shows. That code hands over control of the phone. Real helplines are not mobile numbers, and they
do not ask for this.

**What the victim's phone holds.** An outgoing call to the number found online, a message from that number,
an incoming call from a different number, the install request, and the victim's own message reading out the
code.

**What the case teaches.** A timeline: which call led to the install, and when control was actually handed
over. That moment is when the code was read out, not when the install was requested.

**Questions.** Who asked for the install, when control was handed over, and where a photo was taken.

**Traps.**

| Tier | Trap | Shortcut, and where it leads |
|---|---|---|
| 1, 2 | callback | Blame the number the victim dialled, not the one that called back with the install request. |
| 1, 2 | install_vs_control | Take the time of the install request as the handover. |
| 2 | forwarded | Search for "install ... app": the first hit is a relative's forwarded warning. |

## Not built

SIM swap / OTP theft (it would need an `sms.csv`) was the stretch goal and is not built.

## Sources

- Ministry of Home Affairs alert on blackmail and "digital arrest" by impersonators of police, CBI, NCB, RBI
  and ED, with victims kept on Skype or other video calls, staged studios and uniforms (14 May 2024), as
  reported by All India Radio:
  <https://newsonair.gov.in/home-ministry-warns-against-fraudsters-posing-as-government-officials-for-intimidation-and-extortion>
- I4C public advisory: CBI, police, customs, ED and judges do not arrest people over video calls; report to
  1930 or cybercrime.gov.in (October 2024), as reported by ThePrint:
  <https://theprint.in/india/cbi-ed-police-dont-arrest-people-through-video-calls-indian-cyber-crime-coordination-centre/2299608>
- PIB, Ministry of Home Affairs, "Digital Arrest Scam" (10 December 2024):
  <https://www.pib.gov.in/PressReleasePage.aspx?PRID=2082761>
- PIB, Ministry of Home Affairs, "Incidents of Digital Arrest" (25 March 2025). I4C had blocked more than
  3,962 Skype IDs and 83,668 WhatsApp accounts used for digital arrest. Helpline 1930 and
  cybercrime.gov.in: <https://www.pib.gov.in/PressReleasePage.aspx?PRID=2114750>
- NITI Aayog, "Digital Arrest: The Modern-Day Cyber Scam" (Maj. Sadhna Singh, published April 2025). It covers
  the stages from an innocent-seeming parcel or KYC call, through fake documents and warrants and the
  instruction not to involve family, to payment of a "security deposit" or "fine":
  <https://www.niti.gov.in/sites/default/files/2025-04/Digital_Arrest_The_Modern_Day_Cyber_Scam.pdf>
- PIB, Ministry of Home Affairs: I4C identified, and MeitY blocked, over 100 websites running task-based
  part-time job and illegal investment frauds (6 December 2023):
  <https://pib.gov.in/PressReleasePage.aspx?PRID=1982936>
- The News Minute, "Govt blocks 100 websites involved in job scams, illegal investments" (6 December 2023).
  It describes the steps: "ghar baithe job" ads, WhatsApp or Telegram agents, liking videos or rating
  listings, a small first commission, then larger deposits that are frozen:
  <https://www.thenewsminute.com/news/govt-blocks-100-websites-involved-in-job-scams-illegal-investments>
- Reserve Bank of India, "BE(A)WARE", a booklet on the modus operandi of financial fraudsters (7 March 2022).
  It covers fake customer-care numbers in search results, screen-sharing apps, and the fact that helplines
  are never mobile numbers: <https://website.rbi.org.in/documents/87730/39016390/BEAWARE07032022.pdf>
- Reserve Bank of India press release, "Consumer Awareness - Cyber Threats and Frauds" (28 January 2022):
  <https://www.rbi.org.in/scripts/BS_PressReleaseDisplay.aspx?prid=53185>
