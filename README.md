Currently (2020-02) this repo just provides a library that can read and parse
Excel workbooks representing share sales as downloaded from StockPlanConnect. In
other words, it's currently only useful to coders.

PLEASE PAY ATTENTION TO THE _LICENSE_ FILE. Particularly the bits about
correctness and liability. _I_ use this, but _I_ might be doing it wrong :-)
However _you_ use this is not my responsibility.

### Prerequisites

You will need:

* Python 3.7
* pipenv

### Installation

Clone this repo:

```bash
git clone git@github.com:bgillespie/mssb_spc.git
```

`cd` into the cloned folder and install the dependencies.

```bash
cd mssb_spc
pipenv install --dev
```

### Getting the workbooks

As far as I'm aware there's no API for SPC, so this bit has been manual.

They can be found in StockPlanConnect by going to _Company Overview > Activity >
All plans_ and filtering by type _Sale_. You can choose a date range of sales to
show using the _Change date_ link on the right above the table.

Clicking one of the dates in the leftmost column of the table will show details
of that sale. To the right, above the table of details, a _Download_ link makes
XLS and PDF files available. Obviously the XLS is the one we're after.
