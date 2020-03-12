# passcard

Passcard is a low-tech password management solution inspired by a product i saw for sale online and thought "that looks like something i could make for free."

This method lets you create strong, unique passwords for every website that require both something you have (the card) and something you know (your secret) using just one card, without needing to rely on a password manager.

**Simple, easy to follow instructions:**
 * Run passcard.py to get a randomly-generated card.png like the one below.
 * Print out your card and carry it in your wallet. Probably also keep a backup somewhere, because you __really__ don't want to lose that.
 * All your passwords will start out the same with the 8-character section at the beginning.
 * Follow that with your secret password afterwards. In theory, this part could be the terrible, non-secure password you've already been using everywhere.₁
 * Use the keyboard cypher to make a unique code for the website/service the password is for and use that as the final part of the password.

![Example Passcard](/card.png)

For example, if i were making a password for GitHub with the example card above, the site code would be **H\*Ww.9** and the full password for the site might be **pcX8dh+1Last4DigitsOfMyDogH\*Ww.9**.
 
It's probably not the ideal solution for everyone, but i thought it was a clever solution that would actually work.
 
₁ Just because you *can*, that doesn't mean you *should*.

Hack-Bold.ttf comes courtesy of https://sourcefoundry.org/hack/
