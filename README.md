[![Run in Postman](https://run.pstmn.io/button.svg)](https://god.gw.postman.com/run-collection/27585123-2015d56b-84bf-4fbe-8e49-a41e743ee7e9?action=collection%2Ffork&source=rip_markdown&collection-url=entityId%3D27585123-2015d56b-84bf-4fbe-8e49-a41e743ee7e9%26entityType%3Dcollection%26workspaceId%3D884e5d03-de4a-463e-928a-4e6d02e17684)

<img title="" src="docs/logo.svg" alt="s" width="838">

> **Note**
>
> This project is not ready for general use:
> 
> - `terminal app` is unfinished
> - `data server` is unfinished
> - `web app` is unfinished
> - no `Tangler Cloud` yet
> - no `web browser extension` yet
>
> Build of the latest commit `web app`+`data server`<br/>
> FOR PREVIEW ONLY ("AS IS", WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND)<br/>
> is available at: http://tangler.space<br/>
> (you can play with it to see how the code works right now)

---

#### Simple yet smart lists of whatever you want

You, the user, defines what kinds of items there are.

Common item types are pre-defined, optional, alterable and restorable so you don't have to do anything. 

E.g. you can define such items to use in your lists :

* **`✉️ email`**  --  *(btw. Tangler can sync with your email or just replace it, if you want)*
* **`👤 contact`**
* **`📁 file`**  --  *(btw. Tangler can sync with your local storage as well as cloud, if you want)*
* **`✅ task`**
* **`🔁 routine`**
* **`✍️ note`**
* **`📅 goal`**
* **`🔑 account`**  --  *(btw. Tangler browser plugin can handle your online accounts, if you want)*
* **`🧳 equipment`**
* **`💲 transaction`**
* **`🏦 loan`**
* **`🗺️ place`**
* **`📒 journal`**
* `🔢 some arbitrary metric`  --  *(e.g. smart home combined state or single measurement)*
* ...

#### About those lists

* List can contain items of only one kind or many - you decide.
* There is a handy filter and global view where you get a list per each item type, with all items of that type.
* Every item can point to and contain items of any other item type.
* Every item type is definable and editable: its emoji (optional), its name, what fields does it have etc.
* Every item can have required and optional fields, with content (full or some part) encrypted & protected if needed.
* What kind of content is allowed where (date, check, text, number etc.) is also definable.
* Items and lists can be self updating, sync with external programs and be used interchangeably with those programs.
* Instead of syncing with external programs and services you can sync with [Tangler Cloud](https://cyber.harvard.edu/projectvrm/Privacy_Manifesto) to be sure your data is yours and only yours.

#### Example use cases

* User can define **`🧳 equipment`** and **`📁 file`**, then scan or take a pic of any equipment related documents such as purchase receipts, warranties, instructions and repair reports. Those files can be linked as children of a given equipment.
* **`📁 Document`** such as signed `Terms and Conditions` or `Privacy Policy` can be stored under **`🔑 account`** items to not lose it and for easy access.

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

#### Parts of tangler ecosystem

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

#### Integrations & Analytics

* **Topics**: **`Google Workspace`**, **`Banking`**, **`Crypto`**, **`eCommerce`**, **`items market`**, **`sharing and renting`**, **`Arbitrary internet service`**, ...
* **Examples**: `gmail`, `google drive`, `google contacts`, `mBank`, `Binance`, `Amazon`, `Revolut`,  `PKO`, `ING`, `BPC`, `Coinbase`, `DEGIRO`, `Exante`, `TradingView`, ...
* **Functions**: accounts automatic detection and easy+delegated management (e.g. closing, raport of what is unused (not necessary) or duplicates features),..., `progress and stagnation detection`, `financial analytics`, `projects analytics`

# 
