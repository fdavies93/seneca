<a href="https://www.buymeacoffee.com/fdavies93k" target="_blank"><img src="https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png" alt="Buy Me A Coffee" style="height: 41px !important;width: 174px !important;box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;-webkit-box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;" ></a>

# Seneca

*A script to import from Wise (formerly Transferwise) CSVs to [beancount](https://github.com/beancount/beancount) format. Named after Seneca the Younger, a stoic philosopher who became wealthy by pioneering commodities trading and finance. I.e. a Wise Beancounter.*

The script can successfully log multi-legged outbound transactions including currency transfers. I use it for my own small business accounting needs.

Imports from [Wise Transfers](https://wise.com/help/articles/2489458/how-do-i-download-a-list-of-my-transfers) CSV format. Note that this is a relatively new format and **doesn't include card transactions before 2023-10-27**. For that you'll need to use the older and less rich [Wise Statement](https://wise.com/help/articles/2736049/how-do-i-download-a-statement) format, which this tool doesn't support as of 2024-02-28.

If you'd like me to support additional formats, add more options, or notice any errors, please file an issue and consider [buying me a coffee](https://www.buymeacoffee.com/fdavies93k).

The project is **open for pull requests**.

## Quickstart

Git clone this repo and navigate to the folder.

```sh
python3 -m venv venv
. ./venv/bin/activate
pip install -r requirements.txt 
python seneca.py --input wise_transactions.csv --map categories.json
```

## Options

Note that the script prints to `stdout`. This is by design so that you can use `>` and `>>` to pipe into different files.

### `--input`

The Wise transactions CSV file to import from. E.g. `input/business-wise.csv`

### `--map`

A JSON file. This lets you automatically set the category of both inbound and outbound transactions to this account, which is very helpful when processing a large number of transactions. It uses the `target_name` and `source_name` columns from the Wise CSV as the key and your desired category as the key. For example:

```json
{
  "Spotify": "Expenses:Subscriptions",
  "Acme Corp": "Income:Salary"
}
```

If there's no category found then the script will allocate `Income:Unassigned` or `Expenses:Unassigned` to your transactions.

### `--sort`

A switch to decide the order in which transactions are sorted, by date. If the value is `desc`, outputs in descending order (most recent date first). For all other values, and by default, outputs in ascending order by date.

```text
python seneca.py -i input/transactions.csv --sort desc
```
