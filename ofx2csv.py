#!/usr/bin/env python

import sys
import os
from csv import DictWriter
from ofxparse import OfxParser

DATE_FORMAT = "%m/%d/%Y"


def write_csv(statement, out_file):
    print "Writing: " + out_file
    fields = ['date', 'payee', 'debit', 'credit', 'balance']
    with open(out_file, 'w') as f:
        writer = DictWriter(f, fieldnames=fields)
        for line in statement:
            writer.writerow(line)


def get_transactions(ofx):
    balance = ofx.account.statement.balance
    transactions = []
    for transaction in ofx.account.statement.transactions:
        credit = ""
        debit = ""
        balance = balance + transaction.amount
        if transaction.type == 'credit':
            credit = transaction.amount
        elif transaction.type == 'debit':
            debit = -transaction.amount
        else:
            raise Exception("Unknown transaction type: %s" % transaction.type)
        line = {
            'date': transaction.date.strftime(DATE_FORMAT),
            'payee': transaction.payee,
            'debit': debit,
            'credit': credit,
            'balance': balance
        }
        transactions.append(line)
    return transactions


def main(inputfiles):
    if len(inputfiles) > 0:
        for ofx_file in inputfiles:
            print 'Processing file: ', ofx_file
            try:
                fname, fext = os.path.splitext(ofx_file)
                if fext not in ['.qfx', '.qbo', '.ofx']:
                    raise Exception("Unknown files extension: %s" % fext)
                f = open(ofx_file, 'r')
                ofx = OfxParser.parse(f)
                trans = get_transactions(ofx)
                out_file = fname + ".csv"
                write_csv(trans, out_file)
            except IOError:
                print 'Error cannot open ', ofx_file
            except:
                print 'Error converting files:', sys.exc_info()[0]
    else:
        print 'ofx2csv.py <input-ofx-file> ...'


if __name__ == "__main__":
    main(sys.argv[1:])
