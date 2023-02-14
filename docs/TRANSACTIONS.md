## Spending brainstorm

#### transaction types

- **done single purchase**   
  
  - `grupy` `oszczednosci (odlozone pieniadze)` `prognozy` `inflacja` `categories summary` `zaplanowany budzet` `kategorie powtarzalne`

- **planned single purchase**
  
  - `spoznienie` `kary za opuznienie` `odsetki` `rate change` `przedplata` `under/partial pay` `overpay` `remaining to pay` `zaplanowane wydatki`

- **planned repeat purchase infinite *(subskrypcja)***
  
  - `rata mieszkanie` `silownia` `mobile app` `ZUS` `US` `wynagrodzenie` `zaplanowany poczatek w przyszlosci`

- **planned repeat purchase capped *(kredyt)***
  
  - `mbank kredyt` `medirata kredyt`

#### transaction fields

- **date**: `full` `missing year` `missing year + month` `in future`

- **date_start**: `missing day` `missing day + month`

- **paid**: *actually paid amount*

- ***paid_planned***: *planned/expected payment amount*

- ***paid_late_rate***: *punishment rate for leftover*

- *paid_left*: *dynamically calculated, amount still missing*

- **title**: *person or company name*

- **address**: *account id of other party (sender or receiver depending on if amount is + or -)*

- **account**: *my account involved in this transaction*

- **method** 

- **location** 

- ***category***: *purely informational, arbitrary text user defined categories/groups/buckets*

- ***group***: *loan or subscription name*

- ***group_fluid***: `bool` *is group spilling or not*

- ***links***: *partial/early/late pays of planned transaction* 

#### mbank

- **input**:
  
  > `date` `opis` `account` `category`  `paid`

- **input parsed**: 
  
  > `date` ~~`opis`~~ `account` `category` `paid`
  > 
  > `title` `method` `address` `location`

- **target**:
  
  > **`account`** **`address (weak)`** **`method`** **`location (weak)`**
  > 
  > **`date`** `start`
  > 
  > **`title`**  **`category (weak)`**
  > 
  > **`paid`** `planned` `rate` *`=left`*
  > 
  > `group` `links` *(group can be  fluid or not)*

#### Examples

> today is 01.01.2023

- **kredyt** -- *15'tego*
  
  > **date**: `15.12.2022` `null`
  > 
  > **paid**: `500 PLN` `1100 PLN` `10` *`=3032 PLN left (600 * 5.05 [10%^17])`*
  > 
  > **title**: `kredyt` `=mbank`

- **ziomek**
  
  > **date**: `24.12.2022` `null`
  > 
  > **paid**: `200 PLN` `400 PLN` `0` *`=200 PLN left`*
  > 
  > **title**: `ziomek`

- **biedronka**
  
  > **date**: `today` `null`
  > 
  > **paid**: `100 PLN` `0 PLN` `0`
  > 
  > **title**: `biedronka`

- **spodnie** -- *za 1 tydzien*
  
  > **date**: `07.01.2023` `null`
  > 
  > **paid**: `0 PLN` `100 PLN` `0`
  > 
  > **title**: `spodnie`

- **ziomek** -- *za 2 tygodnie*
  
  > **date**: `14.01.2023` `null`
  > 
  > **paid**: `0 PLN` `1000 PLN` `0`
  > 
  > **title**: `ziomek`

- **aplikacja** -- *za 3 tygodnie*
  
  > **date**: `21.` `null`
  > 
  > **paid**: `0 PLN` `30 PLN` `0`
  > 
  > **title**: `apka`

- **kredyt** -- *15'tego*
  
  > **date**: `15.01.2023` `null`
  > 
  > **paid**: `0 PLN` `1100 PLN` `10`
  > 
  > **title**: `kredyt` `=mbank`

- **mieszkanie** -- *10'tego lutego*
  
  > **date**: `10.` `.02.2023`
  > 
  > **paid**: `0 PLN` `2900 PLN` `0`
  > 
  > **title**: `mieszkanie` `=obrzezna`
