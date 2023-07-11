[![Run in Postman](https://run.pstmn.io/button.svg)](https://god.gw.postman.com/run-collection/27585123-2015d56b-84bf-4fbe-8e49-a41e743ee7e9?action=collection%2Ffork&source=rip_markdown&collection-url=entityId%3D27585123-2015d56b-84bf-4fbe-8e49-a41e743ee7e9%26entityType%3Dcollection%26workspaceId%3D884e5d03-de4a-463e-928a-4e6d02e17684)

<img title="" src="assets/logo.svg" alt="s" width="838">

## Simple yet smart lists of whatever you want.

> ---
>
> **Note**
>
> I'm developing this into a fully functioning product as a learning experience.
>
> Therefore, it's gonna be usable but keep in mind there are most likely
> better alternatives both proprietary and [open source](https://github.com/btw-so/open-source-alternatives)
>
> Also, my primary project is [Bodypace](https://github.com/Bodypace) thus I'm developing this one in the free
> time and when I actually need a given function. Right now I'm already using it, but the first example below + some
> equipment and files tracking is all I need, thus other features are not implemented yet.
> 
> ---

> ---
>
> **Warning**
>
> This project is not ready yet:
> 
> - `terminal app` is unfinished
> - `web app` is unfinished
> - `data server` is unfinished
> - no `integrations` and `synchronizations` yet (e.g. automatically creating `️️📧 email` items)
> - no `Tangler Cloud` yet
> - no `web browser extension` yet
>
> This document describes what Tangler **will be** but remember it's not there yet.
>
> Build of the latest commit `web app`+`data server`<br/>
> FOR PREVIEW ONLY ("AS IS", WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND)<br/>
> is **sometimes** available at: http://tangler.space<br/>
> (you can play with it to see how the code works right now)
> 
> ---

You define the items you use!
Moreover, those items can also synchronize with external data!

What does it mean? It means that you will be able to create one place (**easly!**) where you have everything you want to keep your eye on, so no more switching between 10 different apps that do the same, but only for their niche.

#### About those lists

> todo: update this section, it's too complicated and a little bit probably incorrect

Common item types are pre-defined, optional, alterable and restorable so you don't have to do anything. 

* List can contain items of only one kind or many - you decide.
* There is a handy filter and global view where you get a list per each item type, with all items of that type.
* Every item can point to and contain items of any other item type.
* Every item type is definable and editable: its emoji (optional), its name, what fields does it have etc.
* Every item can have required and optional fields, with content (full or some part) encrypted & protected if needed.
* What kind of content is allowed where (date, check, text, number etc.) is also definable.
* Items and lists can be self updating, sync with external programs and be used interchangeably with those programs.
* Instead of syncing with external programs and services you can sync with [Tangler Cloud](https://cyber.harvard.edu/projectvrm/Privacy_Manifesto) to be sure your data is yours and only yours.

---

### Examples

E.g. you could define such items:

* **`🚀 project`** 
  * `name`, `status`: *`active` or `todo`*
* **`🎯 milestone`**
  * `name`, `category`: *`feat`* or *`maintainance`*, `due date`
* **`✅ task`**
  * `name`, `category`: *`feat`* or *`maintainance`*, `time required`, `priority`: *`p4`*, *`p3`*, *`p2`* or *`p1`*
* **`🔁 routine`**
  * `name`, `category`: *`feat`* or *`maintainance`*, `when`
* **`📜 note`**
  * `title`, (note: in Tangler every item has special `details` field)

to be able to have such "todo" list of your projects:

    ━┳━ 🚀 Homegrown vegetables                           active
     ┣━┳━ 🎯 Build greenhouse                             feat  2023-06-01
     ┃ ┣━━━ ✅ dig the ground                             feat  5 hours  p3
     ┃ ┣━┳━ ✅ install roof frame (scaffolding)           feat  3 hours  p2
     ┃ ┃ ┗━━━ ✅ buy pvc pipes for frame                  feat  1 hour   p2
     ┃ ┣━━━ ✅ lay foil over the frame as a roof          feat  1 hour   p2
     ┃ ┗━━━ 📜 add a door if entry is facing the wind
     ┗━┳━ 🎯 Harvest the first crops!                     feat  2023-09-01
       ┣━━━ 📜 salad is cheap, easy to grow and fast
       ┃       as long as you keep the snails at bay :D
       ┣━━━ ✅ sow the ground                             feat  2 hours  p2
       ┣━━━ 🔁 check everything for pests                 maintainance  at evening
       ┗━━━ 🔁 water everything                           maintainance  at evening

    ━┳━ 🚀 Become great chef                              todo
     ┣━━━ 📜 take some cooking classes?
     ┗━━━ 📜 go over every dish you can order online
             and try doing it at home

    ...

You could also use **synchronizing** items (thanks to **integrations**):

* **`🔑 account`**  
  * `name`, `username`, `email`, `password` **`(encrypt=yes)`** 
* **`👤 contact`** 
  * `name`, `phone number`, `email address`
  * sync:
    * `smartphone`: one way: read
    * `google contacts`: one way: read
* **`️️📧 email`**  
  * `title`, `content`, `date`, `status: "sent" or "received" or "draft"`, `sender`, `receiver`
  * sync:
    * `gmail`: two way: read and write
* **`🧳 equipment`**
  * `name`  
* **`📁 file`**  
  * `name`, `path`
  * sync:
    * `device storage`: one way: read
    * `cloud storage`: one way: read
* **`💲 transaction`**
  * `title`, `date`, `balance`, `account`
  * sync:
    * `bank`: one way: read

to have such lists:

    ━┳━ 🔑 Amazon                                 User89437120  myemail@mail.com  ********
     ┣━┳━ ️️📧 Account creation                     2023-05-01  received  amazom.com
     ┃ ┣━━━ 📁 Terms and Conditions               cloud://some/path
     ┃ ┗━━━ 📁 Privacy policy                     cloud://some/path
     ┣━━━ 🧳 Amazon $25 gift card                 
     ┗━┳━ 🧳 Vacuum cleaner
       ┣━━━ ️📁 User manual                        cloud://some/path
       ┗━┳━ 👤 SellerNo11235813                   +1 112 3581321 contact@goodstuff.com
         ┣━━━ ️💲 Vacuum cleaner payment           2023-05-01  -$32  IBAN 12345678910
         ┗━┳━ ️️📧 Vacuum cleaner purchase order    2023-05-01  received  amazom.com
           ┗━━━ ️📁 Payment confirmation           cloud://some/path           
           ┗━━━ ️📁 Warranty                       cloud://some/path           
           
    ━┳━ 🔑 Bolt                                   Robert  myemail@mail.com  ********
     ┣━┳━ ️️📧 Account creation                     2023-05-01  received  bolt.eu
     ┃ ┣━━━ 📁 Terms and Conditions               cloud://some/path
     ┃ ┗━━━ 📁 Privacy policy                     cloud://some/path
     ┣━━━ ️️📧 Some spam message                    2023-05-01  received  bolt.eu
     ┣━━━ ️️📧 Some spam message                    2023-05-01  received  bolt.eu
     ┣━━━ ️️📧 Some spam message                    2023-05-01  received  bolt.eu
     ┣━━━ ️️📧 Some spam message                    2023-05-01  received  bolt.eu
     ┗━━━ ️️📧 Some spam message                    2023-05-01  received  bolt.eu

    ...

With fields derived one from another you can get detailed budget overview:

* **`💲 transaction`**
  * `title`, `date`, `balance`, `account`
  * sync:
    * `bank`: one way: read
* **`🏦 loan`** 
  * `title`, `date`, `total`, `left`
* **`🔔 subscription`** 
  * `title`, `date`, `rate`, `until`, `paid`

Arbitrary fields can be calculated one from another and it's easy to setup. Again, you define what you want.
E.g. `🔔 subscription` can track all child `💲 transaction` items and show their sum as `paid` field.

    ━┳━ 🔑 Bank                                    12345678  myemail@mail.com  ********
     ┗━┳━ ️🏦 Consumer Loan no.1                    2023-01-01  +$5000  $2000
       ┣━┳━ ️️📧 Loan agreements                     2023-05-01  received  contact@bank.com             
       ┃ ┣━━━ 📁 Terms                             cloud://some/path
       ┃ ┗━━━ 📁 Payment schedule                  cloud://some/path
       ┣━━━ ️💲 Loan installment no.1               2023-02-01  -$1000  <BANK IBAN ADDRESS>
       ┣━━━ ️💲 Loan installment no.2               2023-03-01  -$1000  <BANK IBAN ADDRESS>
       ┗━━━ ️💲 Loan installment no.3               2023-04-01  -$1000  <BANK IBAN ADDRESS>

    ━┳━ 🔑 MusicApp                                Robert  myemail@mail.com  ********
     ┣━━━ ️️📧 Account confirmation                  2023-03-01  received  customers@musicapp.com
     ┗━┳━ 🔔 Standard account                      2023-03-01  $10/month  until cancelled  $30
       ┣━━━ 📁 Agreements                          cloud://some/path
       ┣━━━ ️💲 MusicApp subscription for 2023-03   2023-03-01  -$10  <MUSICAPP INC. BANK ADDRESS>
       ┣━━━ ️💲 MusicApp subscription for 2023-04   2023-04-01  -$10  <MUSICAPP INC. BANK ADDRESS>
       ┗━━━ ️💲 MusicApp subscription for 2023-05   2023-05-01  -$10  <MUSICAPP INC. BANK ADDRESS>

    ...

Here is a simple list, a journal and wishlist. Types:

* **`📒 journal`**
  * `what I did`, `date`, `mood`: *`🔥 excellent`*, *`👍 good`*, *`😐 blank`*, *`🙄 grumpy`*, *`😔 bad`*
* **`💡 idea`**
  * `what to do`, `how will I probably feel`: *`🔥 excellent`*, *`👍 good`*, *`😐 blank`*, *`🙄 grumpy`*, *`😔 bad`*

Possible result:

    ━━━ 📒 Slept until 10am                         2023-04-07  😔 bad
    ━━━ 📒 Ran 10km again                           2023-04-07  👍 good
    ━━━ 📒 Cooked my first sushi                    2023-04-07  🔥 excellent
    ━━━ 📒 Woke up at 8am                           2023-04-08  😐 blank
    ━━━ 📒 Riding dirt bike                         2023-04-08  🔥 excellent
    ━━━ 📒 Woke up at 9am                           2023-04-09  🙄 grumpy
    ━━━ 📒 Reached project A milestone              2023-04-08  🔥 excellent
    ━━━ 📒 Woke up at 5:30am                        2023-04-10  🔥 excellent
    ...
    ━━━ 💡 Go skydiving                             🔥 excellent
    ━━━ 💡 Build a birdhouse                        👍 good

    ...

Lastly, to get the point across, you can really define whatever you want and integrate it with whatever else. 
As long as Tangler provides an integration with a given 3'rd party, it will be possible and easy to setup.

Otherwise, it's still possible but only for technology savy users as users can write their own integrations/synchronization logic for items/lists but it requires programming skills (It's easy tho, Thangler is designed in a way (that's the goal) where there is little logic that clicks well together to give many functionalities thus there is not that much code to write (and it's simple)).

Thus, e.g. smart home is also possible (but for now only if you implement the synchronization yourself):

* **`📍️ place`**
  * `name`
* **`📅 measurement day`**
  * `date`
* **`🌡 temperature`**
  * `created difference`, `at location`, `outside`
* **`💧 water`** 
  * `used liters`
* **`🔋 electricity`**
  * `net watts`, `produced watts` *`(optional)`*, `consumed watts` *`(options)`*
* **`whatever else...`**


Example record of resources consumption for a given day could look like that:

    ━┳━ 📅 2023-05-01
     ┣━━━ 💧 25L
     ┣━┳━ 📍️ House
     ┃ ┣━━━ 🌡 +11'C                                24'C  13'C
     ┃ ┣━━━ 💧 20L
     ┃ ┣━━━ 🔋 +7kW                                 +30kW  -23kW
     ┃ ┣━┳━ 📍️ Home gym
     ┃ ┃ ┗━┳━ 🧳 Treadmill
     ┃ ┃   ┗━━━ 🔋 -2kW
     ┃ ┣━┳━ 📍️ Solar panels
     ┃ ┃ ┗━━━ 🔋 +30kW
     ┃ ┗━┳━ 📍️ Bathroom
     ┃   ┗━━━ 💧 12L
     ┗━┳━ 📍️ Garden
       ┗━━━ 💧 5L

That one is a little bit hard to read right? We are in charge and thus we can make **`📍️ place`** more compact! e.g.:

    ━┳━ 📅 2023-05-01             💧 -25L  🌡 +11'C (24'C - 13'C)  🔋 +7kW (+30kW -23kW)
     ┣━┳━ 📍️ House                💧 -20L  🌡 +11'C (24'C - 13'C)  🔋 +7kW (+30kW -23kW)
     ┃ ┣━┳━ 📍️ Home gym           💧  --   🌡  --                  🔋 -2kW
     ┃ ┃ ┗━┳━ 🧳 Treadmill
     ┃ ┃   ┗━━━ 🔋 -2kW
     ┃ ┣━━━ 📍️ Solar panels       💧  --   🌡  --                  🔋 +30kW
     ┃ ┗━━━ 📍️ Bathroom           💧 -12L  🌡  --                  🔋  --
     ┗━━━ 📍️ Garden               💧 -5L   🌡  --                  🔋  --

Now it's better :).

That was the last example. I hope it's clear we can note pretty much whatever we want with those lists, e.g. add **`⛏️ coal`** household usage or produced grams of **`🧃 plastic`** to the above household monitoring.

---

### What those examples mean

Looking at those examples, one can deduce that with such tool you no longer need a separate app for your shopping receipts, another one for budget planning, another one for passwords and accounts (password manager), another one for notes taking, another for todo lists, another for calendar, another for emails browsing, etc.

Everything is here, plain and simple, and that is the goal.

Tangler can sync with external data providers like gmail, cloud storage (documents, images,...) or bank so you can manage or at least read all the data that is there through Tangler.

---

## For programmers

## How to run it and see project board/roadmap

Instead of using GitHub Issues, GitHub Projects, JIRA or something else Tangler tasks, docs and everything else is managed by Tangler itself. If you want to see what is going on right now in this project or how it already looks like in action, run below. 

### clone project

```bash
git clone https://github.com/ssurrealism/Tangler
cd Tangler
```

### run webapp and server

```bash
docker compose up
# now visit localhost:9000 in your web browser
# or make curl request, e.g. http://localhost:9000/api/config
```

### install dependencies and run cli (cli is serverless)

```bash
# enter cli/server directory
cd app

# install dependencies
python -m venv .venv
source .venv/bin/activate
pip -r requirements.txt

# run some commands (help not implemented yet)
python tangler.py
python tangler.py read note
python tangler.py read task
python tangler.py create task label 'feat' due_date '2023-03-13' project 'cli' title 'implement help command'

# Tangler uses json and yaml files as database right now so you can also read those manually if you want
cat _data/_config.yaml  # this file defines all item types and how to display them
cat _data/task.json  # this file holds all items of type "task" ("task" is defined in _config.yaml)
```

## Technical details

### Parts of tangler ecosystem

* **Data directory**
  
  Directory on your computer or phone or any other device where all lists and items are stored.

* **Data server**
  
  Program that exposes data stored inside **Data directory** to the internet. Used by **PWA** and **Terminal app**.

* **Website and mobile app (PWA)**
  
  Self explanatory. Can work on any data exposed by **Data server**. Has build in support for **Tangler Cloud**.

* **Tangler Cloud**
  
  For people that just want to use **PWA** working out of the box with data synced and accessible across all of their devices. It's an instance of **Data server** managed by tangler authors. **Data directory** for each user in Tangler Cloud is fully encrypted so that nobody who has access to Tangler Cloud can access user data.

* **Terminal app**
  
  Command line app, can work on any data exposed by **Data server** or directly on **Data directory** if computer has access to it.

* **Library**
  
  Python package, used by both **Terminal app** and **Data server** to create, read, update and delete data in **Data directory**.
  Can be used to write scripts and other tools. Library also implements all build-in integrations and analytics.

### Integrations & Analytics

* **Topics**: **`Google Workspace`**, **`Banking`**, **`Crypto`**, **`eCommerce`**, **`items market`**, **`sharing and renting`**, **`Arbitrary internet service`**, ...
* **Examples**: `gmail`, `google drive`, `google contacts`, `mBank`, `Binance`, `Amazon`, `Revolut`,  `PKO`, `ING`, `BPC`, `Coinbase`, `DEGIRO`, `Exante`, `TradingView`, ...
* **Functions**: accounts automatic detection and easy+delegated management (e.g. closing, raport of what is unused (not necessary) or duplicates features),..., `progress and stagnation detection`, `financial analytics`, `projects analytics`

### API

> note: <space_name> below is not implemented yet.

Besides using firefox to access your Tangler space:

    firefox tangler.space/
    firefox tangler.space/me/
    firefox tangler.space/<space_name>
  
You can also use Tangler cli to work without any server, on your local data:

    tangler config read
    tangler config read type
    tangler config read type task
    tangler config read field task
    tangler config read field task category
    tangler read task
    tangler read task 34
  
Or with data from any server, including your own and official https://tangler.space/ server:

    tangler cloud auth login
    tangler cloud auth status
    tangler cloud auth logout

    tangler cloud config read
    tangler cloud config read type
    tangler cloud config read type task
    tangler cloud config read field task
    tangler cloud config read field task category
    tangler cloud read task
    tangler cloud read task 34

You can also use curl without anything locally installed to interact with Tangler server:

> note: for now it's tangler.space/api

    curl api.tangler.space/<space_name>/
    curl api.tangler.space/<space_name>/config
    curl api.tangler.space/<space_name>/config/types
    curl api.tangler.space/<space_name>/config/types/task
    curl api.tangler.space/<space_name>/config/fields/task/category

    curl api.tangler.space/<space_name>/data/task
    curl api.tangler.space/<space_name>/data/task/34

Above will give you your data in json format.
If you want it nicely formatted to readable lists in terminal, just like the Tangler cli does, request `cli` endpoint:

    curl cli.tangler.space/<space_name>/
    curl cli.tangler.space/<space_name>/config
    curl cli.tangler.space/<space_name>/config/types
    curl cli.tangler.space/<space_name>/config/types/task
    curl cli.tangler.space/<space_name>/config/fields/task/category

    curl cli.tangler.space/<space_name>/data/task
    curl cli.tangler.space/<space_name>/data/task/34

And the last 🍒 cherry on the 🍕 cake (83% sure it's cake :p), use `ai` command to interact with your data through "chat like" interface:

    tangler ai "I did <task>, mark it as done"
    tangler ai "what should I do now in my vegetables project?"

    curl ai.tangler.space/<space_name>  ("I did <task>, mark it as done" in requet body)
    curl ai.tangler.space/<space_name>  ("what should I do now in my vegetables project?" in request body)
